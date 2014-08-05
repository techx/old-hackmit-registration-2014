from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Length, Regexp, AnyOf

class AttendeeForm(Form):
    badge = TextField(validators=[InputRequired(), Length(max=50)])
    phone = TextField(validators=[InputRequired(), Length(min=10, max=15), Regexp("^[0-9]{10,15}$")])
    shirt = TextField(validators=[InputRequired(), Length(max=6), AnyOf(['xsmall', 'small', 'medium', 'large', 'xlarge'])])

