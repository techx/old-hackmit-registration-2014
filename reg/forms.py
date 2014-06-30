from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Optional, Length, Email, Regexp

class RegistrationForm(Form):
    role = TextField(validators=[DataRequired(), Regexp("^[a-z]+$")])
    email = TextField(validators=[DataRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$")])
    hashedPassword = TextField(validators=[DataRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class LoginForm(Form):
    email = TextField(validators=[DataRequired(), Email()])
    hashedPassword = TextField(validators=[DataRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class LotteryForm(Form):
    name = TextField(validators=[DataRequired()])
    gender = TextField(validators=[DataRequired()])
    school_id = TextField(validators=[DataRequired()])
    school = TextField(validators=[DataRequired()])
    adult = TextField(validators=[DataRequired()])
    location = TextField(validators=[Optional()])
    inviteCode = TextField(validators=[Optional()])
