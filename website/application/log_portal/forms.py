from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Optional, Length, Regexp

class CompanyForm(Form):
    name = TextField(validators=[InputRequired(), Length(max=50)])
    
    blurb = TextField(validators=[InputRequired(), Length(max=500)])

    ## NEED TO ADD URLS

    mentors = TextField()
    check_box = TextField()
    prizes = TextField()
    swag = TextField()
    