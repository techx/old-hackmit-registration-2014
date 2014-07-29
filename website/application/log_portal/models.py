from random import randrange

from ..models import db

from ..auth.models import Role

class Company(db.Model, Role):
    __bind_key__ = 'local'
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    name = db.Column(db.String(50))
    logo_url = db.Column(db.String(50))
    tshirt_logo_url = db.Column(db.String(50))
    blurb = db.Column(db.String(500))
    api_slide_url = db.Column(db.String(50))
    mentors = db.Column(db.Integer, foreign_key = "mentors.company_id")
    recruiters = db.Column(db.Integer, foreign_key = "mentors.company_id")
    parking_spot_check_box = db.Column(db.Boolean)
    prizes = db.Column(db.String(200))
    swag = db.Column(db.String(200))

    @staticmethod
    def implied_roles():
        return []

    @staticmethod
    def lookup_from_account_id(account_id):
        return Company.query.filter_by(account_id=company_account_id).first()


class Mentor(db.Model, Role):
    __bind_key__ = 'local'
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    mentor_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(50))
    email_address = db.Column(db.String(50))
    food_restrictions = db.Column(db.String(200))
    tshirt_size = db.Column(db.Integer) # XS=1, S=2, M=3, L=4, XL=5, XXL=6
    phone_number = db.Column(db.Integer)
    twitter_handle = db.Column(db.String(50))
    
    @staticmethod
    def implied_roles():
        return ['Attendee']

    @staticmethod
    def lookup_from_account_id(account_id):
        return Mentor.query.filter_by(account_id=mentor_account_id).first()

    @staticmethod
    def lookup_from_company_id(company_id):
        return Company.query.filter_by(company_id=company_id).all()


class Recruiter(db.Model, Role):
    __bind_key__ = 'local'
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    recruiter_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(50))
    email_address = db.Column(db.String(50))
    food_restrictions = db.Column(db.String(200))
    tshirt_size = db.Column(db.Integer) # XS=1, S=2, M=3, L=4, XL=5, XXL=6
    phone_number = db.Column(db.Integer)
    twitter_handle = db.Column(db.String(50))
    
    @staticmethod
    def implied_roles():
        return ['Attendee']

    @staticmethod
    def lookup_from_account_id(account_id):
        return Recruiter.query.filter_by(account_id=recruiter_account_id).first()

    @staticmethod
    def lookup_from_company_id(company_id):
        return Company.query.filter_by(company_id=company_id).all()

