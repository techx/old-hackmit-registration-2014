from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flask_wtf.csrf import CsrfProtect

from models import db, Account, Hacker, Team
from forms import LoginForm, RegistrationForm, LotteryForm
from errors import AuthenticationError


app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.dev.DevelopmentConfig')

# Secure the app with CsrfProtect
csrf = CsrfProtect(app)

# All pages protected by CSRF, if validation fails, render csrf_error page
@csrf.error_handler
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400

app.secret_key = app.config['SECRET_KEY'] # For Flask

db.init_app(app)

# TODO: Separate All of these things! Router, Other classes, etc.

# Register the error handler so it's not an internal server error
@app.errorhandler(AuthenticationError)
def handle_authentication_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

# TODO: move all static files to nginx and use uWSGI to hook into Flask

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sponsor')
def sponsors():
    app.send_static_file('assets/docs/HackMIT2014Sponsorship.pdf')

@app.route('/register')
def get_registration_page():
    if current_user.is_authenticated():
        return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')

@app.route('/accounts', methods=['POST'])
def register_user():
    form = RegistrationForm()
    role = form.role.data
    email_address = form.email.data
    hashed_password = form.hashedPassword.data

    if not form.validate_on_submit():
        #Need to generalize this error
        raise AuthenticationError('Your data is bad and you should feel bad.', status_code=403)

    if Account.query.filter_by(email_address=email_address).first() != None:
        # Send back an error saying that this account already exists
        raise AuthenticationError('This account already exists!', status_code=420)

    newAccount = Account(email_address, hashed_password)
    db.session.add(newAccount)
    if role=="hacker": #TODO Move away from this hardcoded string and turn into a table lookup
        newHacker= Hacker(newAccount.id)
        db.session.add(newHacker)
    db.session.commit()
    
    # Return a message of success
    return jsonify({'message': 'Successfully Registered!'})

@app.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route('/sessions', methods=['POST'])
def sessions():
    form = LoginForm()

    if not form.validate_on_submit():
        raise AuthenticationError("Your data is bad and you should feel bad. What did you do?", status_code=403)
    
    email_address  = form.email.data
    hashed_password = form.hashedPassword.data

    stored_account = Account.query.filter_by(email_address=email_address).first()
    if stored_account == None:
        raise AuthenticationError("Sorry, it doesn't look like you have an account.", status_code=401)

    if not stored_account.check_password(hashed_password):
        raise AuthenticationError("Your username or password do not match.", status_code=402)
    login_user(stored_account)
    return jsonify({ 'url' : url_for('dashboard')})


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/lottery')
@login_required
def lottery():
    hacker = Hacker.query.filter_by(id=current_user.id).first().get_hacker_details()
    return render_template('lottery.html', hacker=hacker)

@app.route('/team')
@login_required
def team():
    hacker = Hacker.query.filter_by(id=current_user.id).first()
    if hacker == None:
        # TODO: This account isn't a hacker! Maybe a company rep or something?
        raise NotImplementedError()
    team_id = hacker.team_id
    if team_id == None:
        team = None
    else:
        team = {}
        team.users = [hacker.email for hacker in Hacker.query.filter_by(team_id=team_id).all()]
        team.inviteCode = Team.query.filter_by(id=team_id).first().invite_code
    return render_template('team.html', team=team)

@app.route('/teams', methods=['POST'])
@login_required
def teams():
    hacker = Hacker.query.filter_by(id=current_user.id).first()
    if hacker == None:
        # TODO: This account isn't a hacker! Maybe a company rep or something?
        raise NotImplementedError()
    team = Team(app)
    db.session.add(team)
    hacker.team_id = team.id    
    db.session.commit()
    # TODO: Need to return a response
    return None

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/hackers', methods=['POST'])
@login_required
def hackers():
    form = LotteryForm()
    # First find the hacker if they already exist
    hacker = Hacker.query.filter_by(id=current_user.id).first()

    hacker.name = form.name.data
    hacker.gender = form.gender.data
    hacker.school_id = form.school_id.data
    hacker.school = form.school.data
    hacker.adult = form.adult.data
    hacker.location = form.location.data
    hacker.inviteCode = form.inviteCode.data

    db.session.commit()

    return jsonify({'message': "Successfully Updated!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug = app.config['DEBUG']
    app.run(debug=debug)
