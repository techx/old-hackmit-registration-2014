from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Email, Regexp

class RegistrationForm(Form):
    role = TextField()
    email = TextField(validators=[DataRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.+-]+\.edu$")])
    hashedPassword = TextField()

class LoginForm(Form):
    email = TextField(validators=[DataRequired(), Email()])
    hashedPassword = TextField()
