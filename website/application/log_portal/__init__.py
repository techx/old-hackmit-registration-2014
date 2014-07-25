from flask import Blueprint

from ..auth import register_role
from .models import Company

blueprint_name = 'log_portal'

bp = Blueprint(blueprint_name, __name__, static_folder='static', static_url_path='/' + blueprint_name + '/static', template_folder='templates')

from . import views

register_role('company', Company, views.dashboard)
register_role('mentor', Mentor, views.dashboard)