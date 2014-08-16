from datetime import timedelta, datetime

from ..models import db
from ..util.dates import has_passed
from ..util.timezones import utc, pacific

from ..auth.models import Role

# [Rutgers, UPenn, Yale, Brown, Waterloo, Toronto, Columbia, NYU, Princeton, Tufts, Wellesley, Brandeis]
buses = [186380, 215062, 130794, 217156, 900001, 900003, 190150, 193900, 186131, 168148, 168218, 165015]

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
        # Always store in UTC but used Eastern for math
        return (self.creation + timedelta(11)).replace(tzinfo=utc).astimezone(pacific).replace(hour=23, minute=59, second=59, microsecond=999999).astimezone(utc)

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

    def confirm_admit(self, session):
        self.confirmed = True

    def __init__(self, account_id):
        self.account_id = account_id
        self.creation = datetime.utcnow()
        self.confirmed = False
