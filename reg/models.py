from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from random import randrange

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    __bind_key__ = 'local'
    __tablename__ = 'accounts'

    # TODO: Need to update this to match the SQL
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(320), unique=True)
    hashed_password = db.Column(db.String(146)) # Total length of hashed, salted password
    confirmed = db.Column(db.Boolean, default = False)

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256:5000', salt_length=62) #Note salt_length is number of characters, 62 matches the length of the password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def update_password(self, password):
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256:5000', salt_length=62) #Note salt_length is number of characters, 62 matches the length of the password

    def email_confirmed(self):
        return self.confirmed

    def confirm_email(self):
        self.confirmed = True

class Hacker(db.Model):
    __bind_key__ = 'local'
    __tablename__ = 'hackers'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    name = db.Column(db.String(50))
    gender = db.Column(db.String(8))
    school_id = db.Column(db.Integer)
    school = db.Column(db.String(120))
    adult = db.Column(db.Boolean)
    location = db.Column(db.String(120))
    invite_code = db.Column(db.String(8))

    def __init__(self, account_id):
        self.account_id = account_id

    def get_hacker_details(self):
        details = {}

        details["name"] = self.name
        details["gender"] = self.gender
        details["account_id"] = self.account_id
        details["school"] = self.school
        details["school_id"] = self.school_id
        details["adult"] = self.adult
        details["location"] = self.location
        details["invite_code"] = self.invite_code

        return details
    
    def update_lottery_info(self, name, gender, school_id, school, adult, location, invite_code):
        self.name=name
        self.gender=gender
        self.school_id=school_id
        self.school=school
        self.location=location
        self.invite_code=invite_code
        self.adult=adult
        

    def lottery_submitted(self):
        return self.name is not None and self.name!= ""

class Team(db.Model):
    __bind_key__ = 'local'
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_invite_code = db.Column(db.String(20), unique=True)

    def __init__(self, app):
        self.team_invite_code = '%020x' % randrange(16**20)
