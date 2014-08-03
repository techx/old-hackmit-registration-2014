from flask import Blueprint

blueprint_name = 'util'

bp = Blueprint(blueprint_name, __name__, static_folder='static', static_url_path='/' + blueprint_name + '/static', template_folder='templates')

# Util module only: exported functions
from .toposort import toposort, toposorted
from .s3_upload import s3_config, register_policy_route

