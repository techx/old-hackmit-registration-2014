from flask import Blueprint

from ..auth import register_role
from .models import Hacker

blueprint_name = 'hackers'

bp = Blueprint(blueprint_name, __name__, static_folder='static', static_url_path='/' + blueprint_name + '/static', template_folder='templates')

from . import views

register_role('hacker', Hacker, views.dashboard)
