from random import randrange

from flask.ext.login import current_user # For migration

from ..models import db

from ..auth.models import Role

class Hacker(db.Model, Role):
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
    interests = db.Column(db.String(1000))

    @staticmethod
    def is_registrable():
        return True

    @staticmethod
    def implied_roles():
        return []

    @staticmethod
    def lookup_from_account_id(account_id):
        return Hacker.query.filter_by(account_id=account_id).first()

    # Automatically truncates codes to 8 characters for comparison
    @staticmethod
    def lookup_from_invite_code(invite_code):
        return Hacker.query.filter_by(invite_code=invite_code[:8]).first()

    @staticmethod
    def lookup_from_team_id(team_id):
        return Hacker.query.filter_by(team_id=team_id).all()

    def lottery_submitted(self):
        return self.interests is not None and self.interests != ""

    def get_hacker_data(self):
        data = {}

        data['gender'] = self.gender
        data['account_id'] = self.account_id
        data['school'] = self.school
        data['school_id'] = self.school_id
        data['adult'] = self.adult
        data['location'] = self.location
        data['invite_code'] = self.invite_code[:8] if self.invite_code is not None else None
        data['interests'] = self.interests

        return data

    @staticmethod
    def create(session, account_id):
        session.add(Hacker(account_id))

    def update_lottery_data(self, session, gender, school_id, school, adult, location, invite_code, interests):
        self.gender = gender
        self.school_id = school_id
        self.school = school
        self.location = location
        self.invite_code = invite_code
        self.adult = adult
        self.interests = interests

    def join_team(self, session, team_id):
        self.team_id = team_id

    def __init__(self, account_id):
        self.account_id = account_id

class Team(db.Model):
    __bind_key__ = 'local'
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_invite_code = db.Column(db.String(20), unique=True)

    @staticmethod
    def create(session):
        new_team = Team()
        session.add(new_team)
        session.flush()
        return new_team.id

    def __init__(self):
        self.team_invite_code = '%020x' % randrange(16**20)
