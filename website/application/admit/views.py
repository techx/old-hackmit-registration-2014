from functools import wraps

from flask import render_template, jsonify
from flask.ext.login import current_user

from ..errors import BadDataError
from ..models import db_safety

from ..attendee.models import Attendee
from ..hackers.views import hackers_only

from . import bp
from .forms import ConfirmationForm
from .models import Admit

def dashboard(): #TODO
    admit = Admit.lookup_from_account_id(current_user.id)
    deadline = admit.get_deadline()
    return {'name':'admit_dashboard.html', 'context':{'deadline':deadline}}

# Implies the @login_required, @email_confirmed, and @hackers_only decorators
def admits_only(function):
    @hackers_only
    @wraps(function)
    def wrapped_admits_only_function(*args, **kwargs):
        admit = Admit.lookup_from_account_id(current_user.id)
        if not admit:
            return render_template('server_message.html', header="You need to be admitted to access this!", subheader="Sorry about that.")
        else:
            return function(*args, **kwargs)
    return wrapped_admits_only_function

@bp.route('/confirmation')
@admits_only
def confirmation():
    attendee = Attendee.lookup_from_account_id(current_user.id).get_attendee_data()
    if attendee['badge_name'] is None:
        attendee['badge_name'] = current_user.get_name()
    admit = Admit.lookup_from_account_id(current_user.id).get_admit_data()
    return render_template('confirmation.html', attendee=attendee, admit=admit)

@bp.route('/admits', methods=['PUT'])
@admits_only
def update_confirmation():
    form = ConfirmationForm()
    # First find the hacker if they already exist
    if not form.validate_on_submit():
        raise BadDataError()

    attendee = Attendee.lookup_from_account_id(current_user.id)
    admit = Admit.lookup_from_account_id(current_user.id)
    
    with db_safety() as session:
        attendee.update_attendee_data(session, form.badge.data, form.shirt.data, form.phone.data)
        admit.update_admit_data(session, form.diet.data)

    return jsonify({'message': "Successfully Updated!"})

