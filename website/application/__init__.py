from os import environ

from flask import Flask, render_template, jsonify, abort
from flask_sslify import SSLify
from flask_wtf.csrf import CsrfProtect

application = Flask(__name__, instance_relative_config=True)

# For AWS
app = application

try:
    configuration_module_name = environ['HACKMIT_FLASK_CONFIG_MODULE']
except KeyError:
    configuration_module_name = 'application.config.dev.DevelopmentConfig'
app.config.from_object(configuration_module_name)

from .emails import mail
from .errors import DatabaseError
from .models import db

# Redirect all requests to HTTPS
#sslify = SSLify(app, subdomains=True, permanent=True)

# Secure the app with CsrfProtect
csrf = CsrfProtect(app)

# All pages protected by CSRF, if validation fails, render csrf_error page
@csrf.error_handler
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400

app.secret_key = app.config['SECRET_KEY'] # For Flask

db.init_app(app)
mail.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('server_message.html', header="404", subheader="Whoa, you must be lost.")

@app.errorhandler(405)
def method_not_allowed(error):
    # 405 is method not allowed; just pretend the endpoint doesn't exist
     return render_template('server_message.html', header="404", subheader="Whoa, you must be lost.")

@app.errorhandler(DatabaseError)
def handle_database_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

from .core import bp as core
from .auth import bp as auth
from .hackers import bp as hackers
from .util import bp as util

app.register_blueprint(core)
app.register_blueprint(auth)
app.register_blueprint(hackers)
app.register_blueprint(util)
