from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Optional, Length, Email, Regexp, AnyOf

class RegistrationForm(Form):
    role = TextField(validators=[InputRequired(), Regexp("^[a-z]+$")])
    email = TextField(validators=[InputRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$")])
    hashedPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class LoginForm(Form):
    email = TextField(validators=[InputRequired(), Email()])
    hashedPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class LotteryForm(Form):
    name = TextField(validators=[InputRequired(), Length(max=50)])
    gender = TextField(validators=[InputRequired(), Length(max=8), Regexp("^[a-z]+$")])
    school_id = TextField(validators=[InputRequired(), Length(min=1, max=6), Regexp("^(0)|([0-9]{6})$")])
    school = TextField(validators=[InputRequired(), Length(max=120)])
    adult = TextField(validators=[InputRequired(), AnyOf(['true', 'false'])])
    location = TextField(validators=[Optional(), Length(max=120)])
    inviteCode = TextField(validators=[Optional()])

class ResetForm(Form):
    email = TextField(validators=[DataRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$")])
    oldPassword = TextField(validators=[DataRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])
    newPassword = TextField(validators=[DataRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])
