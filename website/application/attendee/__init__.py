from flask import Blueprint

from ..auth import register_role
from .models import Attendee

blueprint_name = 'attendee'

bp = Blueprint(blueprint_name, __name__, template_folder='templates')

register_role(Attendee, None)
