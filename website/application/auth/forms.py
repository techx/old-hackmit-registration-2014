from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Length, Email, Regexp

class RegistrationForm(Form):
    role = TextField(validators=[InputRequired(), Regexp("^[a-z]+$")])
    email = TextField(validators=[InputRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+$")])
    hashedPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class LoginForm(Form):
    email = TextField(validators=[InputRequired(), Email()])
    hashedPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class ResetForm(Form):
    email = TextField(validators=[InputRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$")])
    oldPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])
    newPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])

class ForgotForm(Form):
    email = TextField(validators=[InputRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$")])

class ForgotResetForm(Form):
    newPassword = TextField(validators=[InputRequired(), Length(min=62, max=62), Regexp("^[a-z0-9]+$")])
