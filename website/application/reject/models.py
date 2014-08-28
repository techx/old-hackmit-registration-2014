from ..models import db

from ..auth.models import Role

class Reject(db.Model, Role):
    __bind_key__ = 'local'
    __tablename__ = 'rejects'

    @staticmethod
    def role_name():
        return 'reject'

    @staticmethod
    def implied_roles():
        return ['hacker']

    def __init__(self, account_id):
        self.account_id = account_id
