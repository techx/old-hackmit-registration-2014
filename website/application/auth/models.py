from sqlalchemy import func
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash as werkzeug_generate_password_hash, check_password_hash
from ..models import db

def generate_password_hash(password):
        # Parameters: salt_length is number of characters, 62 matches the length of the password
        return werkzeug_generate_password_hash(password, method='pbkdf2:sha256:5000', salt_length=62)

class Account(db.Model, UserMixin):
    __bind_key__ = 'local'
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(320), unique=True)
    hashed_password = db.Column(db.String(146)) # Total length of hashed, salted password
    confirmed = db.Column(db.Boolean, default=False)

    @staticmethod
    def lookup_from_email(email):
        return Account.query.filter(func.lower(Account.email_address) == func.lower(email)).first()

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def email_confirmed(self):
        return self.confirmed

    @staticmethod
    def create(session, email_address, hashed_password):
        new_account = Account(email_address, hashed_password)
        session.add(new_account)
        session.flush()
        return new_account.id

    def confirm_email(self, session):
        self.confirmed = True

    def update_password(self, session, password):
        self.hashed_password = generate_password_hash(password)

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.hashed_password = generate_password_hash(password)

class Role:

    # All functionality must be in methods to avoid spurious db fields
    # All methods must be overriden in subclasses

    @staticmethod
    def is_registrable():
        raise NotImplementedError

    @staticmethod
    def lookup_from_account_id(account_id):
        raise NotImplementedError

