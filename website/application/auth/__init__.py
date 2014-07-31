from flask import Blueprint, current_app

from flask.ext.login import LoginManager
from flask.ext.principal import Principal

from .. import app

from .models import Role

blueprint_name = 'auth'

bp = Blueprint(blueprint_name, __name__, static_folder='static', static_url_path='/' + blueprint_name + '/static', template_folder='templates')

roles = {}

def register_role(model, dashboard_view_context_func):
    if not issubclass(model, Role):
        raise TypeError("Can only register subclasses of auth.models.Role!")
    # Allow roles to be overriden by later registrations
    roles[model.role_name()] = {'model': model, 'dashboard': dashboard_view_context_func}

login_manager = LoginManager()
with app.app_context():
    login_manager.init_app(current_app)

    # Must be initialized after LoginManager
    # Don't use sessions as goal is to have the Flask end be a stateless API
    # Skip static as it shouldn't have anything sensitive
    principal = Principal(current_app, use_sessions=False, skip_static=True)

# For some bizarre reason this isn't getting set properly, even though there is no 'LOGIN_REQUIRED' config variable, so do it manually
login_manager._login_disabled = False

from . import views
