from datetime import timedelta, datetime

from ..models import db
from ..util.dates import dates, has_passed
from ..util.timezones import utc, eastern

from ..auth.models import Role

# [Yale, Brown, Waterloo, Toronto, Columbia, NYU, Princeton, Tufts, Wellesley, Brandeis]
buses = [130794, 217156, 900001, 900003, 190150, 193900, 186131, 168148, 168218, 165015]

class Admit(db.Model, Role):
    __bind_key__ = 'local'
    __tablename__ = 'admits'

    creation = db.Column(db.DateTime())
    graduation = db.Column(db.String(4))
    meng = db.Column(db.Boolean)
    dietary_restriction = db.Column(db.String(6))
    legal_waiver = db.Column(db.String(50))
    photo_release = db.Column(db.String(50))
    resume_opt_out = db.Column(db.Boolean)
    resume = db.Column(db.Boolean)
    github = db.Column(db.String(39)) # Max is 39 as per their signup page
    travel = db.Column(db.Boolean)
    likelihood = db.Column(db.String(10))
    confirmed = db.Column(db.Boolean)

    @staticmethod
    def role_name():
        return 'admit'

    @staticmethod
    def implied_roles():
        return ['attendee', 'hacker']

    def perms(self):
        permissions = []
        if self.confirmed and not has_passed(dates['profile_update_closing']):
            permissions.append('update')
        if not has_passed(self.get_deadline()):
            permissions.append('valid')
            if not self.confirmed:
                permissions.append('pending')
        else:
            if self.graduation is not None:
                permissions.append('valid')
        return permissions
    
    def get_admit_data(self):
        data = {}

        data['graduation'] = self.graduation
        data['meng'] = self.meng
        data['dietary_restriction'] = self.dietary_restriction
        data['legal_waiver'] = self.legal_waiver
        data['photo_release'] = self.photo_release
        data['resume_opt_out'] = self.resume_opt_out
        data['resume'] = self.resume
        data['github'] = self.github
        data['travel'] = self.travel
        data['likelihood'] = self.likelihood

        return data

    def is_confirmed(self):
        return self.confirmed

    def get_deadline(self):
        deadline = Deadline.query.get(self.id)
        if deadline is not None:
            if deadline.deadline is not None:
                return deadline.deadline.replace(tzinfo=utc)
        # Always store in UTC but used Eastern for math
        return (self.creation + timedelta(10)).replace(tzinfo=utc).astimezone(eastern).replace(hour=23, minute=59, second=59, microsecond=999999).astimezone(utc)

    def update_admit_data(self, session, graduation, meng, dietary_restriction, legal_waiver, photo_release, resume_opt_out, resume, github, travel, likelihood):
        self.graduation = graduation
        self.meng = meng
        self.dietary_restriction = dietary_restriction
        self.legal_waiver=legal_waiver
        self.photo_release=photo_release
        self.resume_opt_out = resume_opt_out
        self.resume = resume
        self.github = github
        self.travel = travel
        self.likelihood = likelihood

    def update_profile_data(self, session, resume_opt_out, resume, github):
        self.resume_opt_out = resume_opt_out
        self.resume = resume
        self.github = github

    def confirm_admit(self, session):
        self.confirmed = True

    def __init__(self, account_id):
        self.account_id = account_id
        self.creation = datetime.utcnow()
        self.confirmed = False

class Deadline(db.Model):
    __bind_key__ = 'local'
    __tablename__ = 'admit_confirmation_extended_deadlines'

    admit_id = db.Column(db.Integer, db.ForeignKey('admits.id'), primary_key=True)
    deadline = db.Column(db.DateTime())

    @staticmethod
    def create(session, admit_id, deadline=None):
        new_deadline = Deadline(admit_id)
        if deadline is not None:
            new_deadline.update_deadline(session, deadline)
        session.add(new_deadline)

    def update_deadline(self, session, deadline):
        # Require timezone aware datetime
        if deadline.tzinfo is not None:
            # Require UTC timezone
            # But must store as naive datetime
            self.deadline = deadline.astimezone(utc).replace(tzinfo=None)

    def __init__(self, admit_id):
        self.admit_id = admit_id

class Profile(db.Model):
    __bind_key__ = 'local'
    __tablename__ = 'profiles'

    admit_id = db.Column(db.Integer, db.ForeignKey('admits.id'), primary_key=True)
    mit_host = db.Column(db.String(50))
    non_smoking = db.Column(db.Boolean)
    pets = db.Column(db.Boolean)
    considerations = db.Column(db.String(400))
    address = db.Column(db.String(150))

    @staticmethod
    def lookup_from_admit_id(admit_id):
        return Profile.query.get(admit_id)

    def get_profile_data(self):
        data = {}

        data['mit_host'] = self.mit_host
        data['non_smoking'] = self.non_smoking
        data['pets'] = self.pets
        data['considerations'] = self.considerations
        data['address'] = self.address

        return data

    def update_hosting_data(self, session, mit_host, non_smoking, pets, considerations):
        self.mit_host = mit_host
        self.non_smoking = non_smoking
        self.pets = pets
        self.considerations = considerations

    def update_address_data(self, session, address):
        self.address = address

    @staticmethod
    def create(session, admit_id):
        new_profile = Profile(admit_id)
        session.add(new_profile)
        session.flush()

    def __init__(self, admit_id):
        self.admit_id = admit_id
