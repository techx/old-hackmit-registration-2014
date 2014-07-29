from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Optional, Length, Regexp

class CompanyForm(Form):
    name = TextField(validators=[InputRequired(), Length(max=50)])
    logo_url = TextField()
    tshirt_logo_url = TextField()
    blurb = TextField(validators=[InputRequired(), Length(max=500)])
    api_slide_url = TextField()
    mentors = TextField()
    recruiters = TextField()
    check_box = TextField()
    prizes = TextField()
    swag = TextField()
    