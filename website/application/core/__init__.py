from flask import Blueprint

blueprint_name = 'core'

bp = Blueprint(blueprint_name, __name__, static_folder='static', static_url_path='/' + blueprint_name + '/static', template_folder='templates')

from . import views
