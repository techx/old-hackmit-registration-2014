from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeSerializer

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    __bind_key__ = 'local'
    __tablename__ = 'accounts'

    # TODO: Need to update this to match the SQL
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(320), unique=True)
    hashed_password = db.Column(db.String(146)) # Total length of hashed, salted password

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256:5000', salt_length=62) #Note salt_length is number of characters, 62 matches the length of the password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class Hacker(db.Model):
    __bind_key__ = 'local'
    __tablename__ = 'hackers'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id')) # Need to add lottery fields.

    def __init__(self, account_id):
        self.account_id = account_id

class Team(db.Model):
   __bind_key__ = 'local'
   __tablename__ = 'teams'

   id = db.Column(db.Integer, primary_key=True)
   inviteCode = db.Column(db.String(100), unique=True)
   #TODO: need to figure out max size of digest for inviteCode

   def __init__(self, app):
       self.inviteCode = URLSafeSerializer(app.config['SECRET_KEY']).dumps(self.id)
