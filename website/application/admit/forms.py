from wtforms import TextField
from wtforms.validators import InputRequired, Length, Regexp

from ..attendee.forms import AttendeeForm

class ConfirmationForm(AttendeeForm):
    diet = TextField(validators=[InputRequired(), Length(max=6)])
    #travel = 
    #resume =

