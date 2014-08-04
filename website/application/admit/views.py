from functools import wraps

from flask import render_template, jsonify
from flask.ext.login import current_user
from flask.ext.principal import Permission, RoleNeed

from ..errors import BadDataError
from ..models import db_safety

from ..attendee.models import Attendee
from ..hackers.models import Hacker
from ..util.datetime_format import format_utc_datetime
from ..util.timezones import eastern
from ..util.s3_upload import s3_config, register_policy_route

from . import bp
from .forms import ConfirmationForm
from .models import Admit, buses

def dashboard(): #TODO
    admit = Admit.lookup_from_account_id(current_user.id)
    deadline = admit.get_deadline()
    return {'name':'admit_dashboard.html', 'context':{'deadline':format_utc_datetime(deadline, eastern)}}

AdmitPermission = Permission(RoleNeed('admit'))

register_policy_route('/accounts/<int:account_id>/resume/policy', 'resume', AdmitPermission, lambda kwargs: 'accounts/' + str(kwargs['account_id']) + '/resume.pdf')

register_policy_route('/accounts/<int:account_id>/travel/policy', 'travel', AdmitPermission, lambda kwargs: 'accounts/' + str(kwargs['account_id']) + '/travel.pdf')

@bp.route('/confirmation')
@AdmitPermission.require()
def confirmation():
    attendee = Attendee.lookup_from_account_id(current_user.id).get_attendee_data()
    if attendee['badge_name'] is None:
        attendee['badge_name'] = current_user.get_name()
    admit = Admit.lookup_from_account_id(current_user.id).get_admit_data()

    resume= {}
    resume['policy_endpoint'] = '/accounts/' + str(current_user.id) + '/resume/policy'
    resume['resource_name'] = "PDF" #need to be value

    hacker = Hacker.lookup_from_account_id(current_user.id)
    bus = (hacker.school_id in buses)
    mit = (hacker.school_id == 166683)

    travel= {}
    travel['policy_endpoint'] = '/accounts/' + str(current_user.id) + '/travel/policy'
    travel['resource_name'] = "Travel Confirmation"


    return render_template('confirmation.html', attendee=attendee, admit=admit, s3=s3_config(), resume=resume, bus=bus, mit=mit, travel_reimbursement=travel)

@bp.route('/admits', methods=['PUT'])
@AdmitPermission.require()
def update_confirmation():
    form = ConfirmationForm()
    # First find the hacker if they already exist
    if not form.validate_on_submit():
        raise BadDataError()

    if form.data.resumeOptOut is False and form.data.resume is None:
        raise BadDataError()

    attendee = Attendee.lookup_from_account_id(current_user.id)
    admit = Admit.lookup_from_account_id(current_user.id)
    
    with db_safety() as session:
        attendee.update_attendee_data(session, form.badge.data, form.shirt.data, form.phone.data)
        admit.update_admit_data(session, form.diet.data, form.resumeOptOut.data, form.resume.data, form.travel.data)
    return jsonify({'message': "Successfully Updated!"})

