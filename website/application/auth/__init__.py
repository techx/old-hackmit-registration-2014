from flask import Blueprint, current_app

from flask.ext.login import LoginManager

from .. import app

from .models import Role

blueprint_name = 'auth'

bp = Blueprint(blueprint_name, __name__, static_folder='static', static_url_path='/' + blueprint_name + '/static', template_folder='templates')

roles = {}

def register_role(role, model, dashboard):
    if type(role) != str:
        raise TypeError("Need a string to identify the role.")
    if model == Role or not issubclass(model, Role):
        raise TypeError("Can only register subclasses of auth.models.Role!")
    # Allow roles to be overriden by later registrations
    roles[role] = {'model': model, 'dashboard': dashboard}

login_manager = LoginManager()
with app.app_context():
    login_manager.init_app(current_app)

# For some bizarre reason this isn't getting set properly, even though there is no 'LOGIN_REQUIRED' config variable, so do it manually
login_manager._login_disabled = False

from . import views
