from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Optional, Length, Regexp

class LotteryForm(Form):
    name = TextField(validators=[InputRequired(), Length(max=50)])
    gender = TextField(validators=[InputRequired(), Length(max=8), Regexp("^[a-z]+$")])
    school_id = TextField(validators=[InputRequired(), Length(min=1, max=6), Regexp("^(0)|([0-9]{6})$")])
    school = TextField(validators=[InputRequired(), Length(max=120)])
    adult = TextField()
    location = TextField(validators=[Optional(), Length(max=120)])
    inviteCode = TextField(validators=[Optional()])
    interests = TextField(validators=[InputRequired(), Length(max=1000)])
