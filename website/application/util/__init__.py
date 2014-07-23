from flask import Blueprint

from ..auth import register_role
from .models import Attendee

blueprint_name = 'util'

bp = Blueprint(blueprint_name, __name__)

register_role('attendee', Attendee, None)
