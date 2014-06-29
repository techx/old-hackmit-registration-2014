from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    # TODO: Need to update this to match the SQL
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(320), unique=True)
    # TODO: Need to update stored password length, salt size to match output of generate, input password
    hashed_password = db.Column(db.String(120))

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256:5000', salt_length=8) #Note salt_length is number of characters

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

