from wtforms import TextField
from wtforms.validators import Optional, InputRequired, Length, Regexp, AnyOf

from ..attendee.forms import AttendeeForm

class ConfirmationForm(AttendeeForm):
    graduation = TextField(validators=[InputRequired(), Length(min=4, max=4), AnyOf(['2015', '2016', '2017', '2018'])])
    meng = TextField()
    diet = TextField(validators=[InputRequired(), Length(max=6), AnyOf(['none', 'veg', 'vegan', 'kosher', 'halal', 'other'])])
    resumeOptOut = TextField()
    resume = TextField()
    github = TextField(validators=[InputRequired(), Length(min=1,max=39), Regexp("^[a-zA-Z0-9][-a-zA-Z0-9]{0,38}")])
    travel = TextField()
    likelihood = TextField(validators=[InputRequired(), Length(min=4, max=10), AnyOf(['li_maybe', 'li_likely', 'li_yes'])])
