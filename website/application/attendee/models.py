from ..models import db

from ..auth.models import Role

class Attendee(db.Model, Role):
    __bind_key__ = 'local'
    __tablename__ = 'attendees'

    badge_name = db.Column(db.String(50))
    shirt_size = db.Column(db.String(6)) # (Implied t-shirts)
    phone_number = db.Column(db.String(16)) # Store as string of digits, 10-15 chars (leave extra space for future E164 compatibility)
    
    @staticmethod
    def is_registrable():
        return False

    @staticmethod
    def role_name():
        return 'attendee'

    @staticmethod
    def implied_roles():
        return []

    def get_attendee_data(self):
       data = {}

       data['badge_name'] = self.badge_name
       data['shirt_size'] = self.shirt_size
       data['phone_number'] = self.phone_number
       
       return data 

    def update_attendee_data(self, session, badge_name, shirt_size, phone_number):
        self.badge_name = badge_name
        self.shirt_size = shirt_size
        self.phone_number = phone_number

    def __init__(self, account_id):
        self.account_id = account_id
