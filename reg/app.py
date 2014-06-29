from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config.test.TestingConfig')

# Secure the app with CsrfProtect
csrf = CsrfProtect(app)

# All pages protected by CSRF, if validation fails, render csrf_error page
@csrf.error_handler
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400

app.secret_key = app.config['SECRET_KEY'] # For Flask
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

# TODO: Separate All of these things! Router, Other classes, etc.
# -------------------------------------------------
# Error Handling for Authentication Errors
# -------------------------------------------------
class AuthenticationError(Exception):
    # Status codes and what they mean:
    # 420: User already exists. What, did you forget?

    status_code = 420

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# Register the error handler so it's not an internal server error
@app.errorhandler(AuthenticationError)
def handle_authentication_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
# ---------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

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
    json = request.json
    user_type = json['type']
    email_address  = json['email']
    hashed_password = json['hashedPassword']

    if not email_address.endswith(".edu"):
        raise AuthenticationError('Nice try, but use your .edu email.')

    if Account.query.filter_by(email_address=email_address).first() != None:
        # Send back an error saying that this account already exists
        raise AuthenticationError('This account already exists!', status_code=420)

    newAccount = Account(email_address, hashed_password)
    db.session.add(newAccount)
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
    json = request.json
    email_address  = json['email']
    hashed_password = json['hashedPassword']

    stored_account = Account.query.filter_by(email_address=email_address).first()
    if stored_account == None:
        raise AuthenticationError("Sorry, it doesn't look like you have an account.", status_code=401)
    stored_password = stored_account.hashed_password
    if not check_password_hash(stored_password, hashed_password):
        raise AuthenticationError("Your username or password do not match.", status_code=402)
    login_user(stored_account)
    return jsonify({ 'url' : url_for('dashboard')})

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    debug = app.config['DEBUG']
    app.run(debug=debug)
