from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import TextField

class RegistrationForm(Form):
    #type = TextField() Need to change name of field
    email = TextField()
    hashedPassword = TextField()

class LoginForm(Form):
    email = TextField(validators=[])
    hashedPassword = TextField()
