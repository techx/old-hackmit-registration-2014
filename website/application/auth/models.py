from functools import partial
from collections import deque
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.login import UserMixin
from flask.ext.principal import ItemNeed
from werkzeug.security import generate_password_hash as werkzeug_generate_password_hash, check_password_hash
from ..models import db, db_safety

AttributeNeed = partial(ItemNeed, 'attribute')

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

    def get_name(self):
        # Hard-coded dependency due to impending EOL
        from ..hackers.models import Hacker
        hacker = Hacker.lookup_from_account_id(self.id)
        if hacker is None:
            return None
        return hacker.name

    @staticmethod
    def create(session, email_address, hashed_password, initial_role):
        new_account = Account(email_address, hashed_password)
        session.add(new_account)
        session.flush()

        new_account.add_role(session, initial_role)

        return new_account.id

    def confirm_email(self, session):
        self.confirmed = True

    def update_password(self, session, password):
        self.hashed_password = generate_password_hash(password)

    def update_name(self, session, new_name):
        # Hard-coded dependency due to impending EOL
        from ..hackers.models import Hacker
        hacker = Hacker.lookup_from_account_id(self.id)
        if hacker is None:
            # Should raise but this is EOL so let's swallow
            pass
        hacker.name = new_name

    def add_role(self, session, role):
        from . import roles
        roles_queue = deque()
        roles_queue.append(role)
        while len(roles_queue):
            role_model = roles[roles_queue.popleft()]['model']
            if role_model.lookup_from_account_id(self.id) is None: # Don't add rows for roles that already exist
                role_model.create(session, self.id)
                session.flush()
                roles_queue.extend(role_model.implied_roles())

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.hashed_password = generate_password_hash(password)

class Role:

    id = db.Column(db.Integer, primary_key=True)
    @declared_attr
    def account_id(cls):
        return db.Column('account_id', db.Integer, db.ForeignKey('accounts.id'))

    @staticmethod
    def is_registrable():
        return False

    @staticmethod
    def role_name():
        raise NotImplementedError

    @staticmethod
    def implied_roles():
        return []

    @classmethod
    def lookup_from_account_id(cls, account_id):
        return cls.query.filter_by(account_id=account_id).first()

    @classmethod
    def create(cls, session, account_id):
        session.add(cls(account_id))

    def needs(self):
        return [partial(AttributeNeed, self.role_name())(perm) for perm in self.perms()]

    def perms(self):
        return []
