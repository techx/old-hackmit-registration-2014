from flask import Flask, render_template, request, redirect, url_for
from flask.ext.login import LoginManager, login_required, UserMixin, login_user
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import Form
from wtforms import TextField

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.dev.DevConfig')
app.secret_key = app.config['SECRET_KEY'] # For Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # TODO: Need to change location
db = SQLAlchemy(app)

class Account(db.Model, UserMixin):
    # TODO: Need to update this to match the SQL
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(320), unique=True)
    # TODO: Nned to update stored password length, salt size to match output of generate, input password
    hashed_password = db.Column(db.String(120))

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256:5000', salt_length=8) #Note salt_length is number of characters 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

class LoginForm(Form):
    email = TextField('email')
    hashedPassword = TextField('hashedPassword')

# TODO: move all staic files to nginx and use uWSGI to hook into Flask

@app.route('/')
def index():
    return app.send_static_file('assets/index.html')

@app.route('/sponsor')
def sponsors():
	return app.send_static_file('assets/HackMIT2014Sponsorship.pdf')

@app.route('/register')
def get_registration_page():
	return render_template('register')

@app.route('/accounts', methods=['POST'])
def register_user():
    json = request.get_json()
    user_type = json['type']
    email_address  = json['email']
    hashed_password = json['hashedPassword']
    if Account.query.filter_by(email_address=email_address).first() != None:
        # Need to tell them that they already exist in db
        raise NotImplementedError()
    newAccount = Account(email_address, hashed_password)
    db.session.add(newAccount)
    db.session.commit()

#i TODO: Need to add CSRF protection to /login and /sessions 

@app.route('/login')
def login():
    return render_template('login')
    #raise NotImplementedError("csrf token")

@app.route('/sessions', methods=['POST'])
def sessions():
    form = LoginForm(csrf_enabled=False) # TODO: remove csrf_enabled=False
    if form.validate_on_submit():
        email_address = form.email.data
        stored_account = Account.query.filter_by(email_address=email_address).first() 
        if stored_account == None:
            print 'DEBUGGG: Account does not exist'
            # TODO: Need to tell them that they already exist in db
            raise NotImplementedError()
        stored_password = stored_account.hashed_password
        hashed_password = form.hashedPassword.data
        if not check_password_hash(stored_password, hashed_password):
            print 'DEBUGGG: Password does not match'
            # TODO: need to tell them it's wrong
            raise NotImplementedError()
        print 'all good to go!'         
        login_user(stored_account)
        # TODO: Do you want to use flash() to show the logged-in notification, use ajax somehow, or just use the redirect?
        #flash('logged in successfully')
        return redirect(url_for('dashboard'))
    else:
        raise NotImplementedError('invalid login at POST to /sessions')

@app.route('/dashboard')
@login_required
def dashboard():
    # TODO: show the dashboard
    return render_template('dashboard', csrf_token=None)

if __name__ == '__main__':
    debug = app.config['DEBUG']
    app.run(debug=debug)
