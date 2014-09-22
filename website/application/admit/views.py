from functools import wraps

from flask import jsonify
from flask.ext.login import current_user
from flask.ext.principal import Permission, RoleNeed

from .. import render_full_template

from ..errors import BadDataError
from ..models import db_safety

from ..auth.models import AttributeNeed
from ..attendee.models import Attendee
from ..hackers.models import Hacker
from ..util.dates import dates, has_passed
from ..util.datetime_format import format_utc_datetime
from ..util.timezones import eastern
from ..util.s3_upload import s3_config, register_policy_route

from . import bp
from .forms import ConfirmationForm, UpdateForm
from .models import Admit, buses, Profile

def dashboard():
    admit = Admit.lookup_from_account_id(current_user.id)
    deadline = admit.get_deadline()
    too_late = has_passed(deadline)
    completed = admit.get_admit_data()['graduation'] is not None
    confirmed = admit.is_confirmed()
    profile_deadline = dates['profile_update_closing']
    hacker = Hacker.lookup_from_account_id(current_user.id)
    mit = (hacker.school_id == 166683)
    travel = admit.travel
    return {'name':'admit_dashboard.html', 'context':{'deadline':format_utc_datetime(deadline, eastern), 'completed':completed, 'confirmed':confirmed, 'too_late':too_late, 'profile_update_deadline':format_utc_datetime(profile_deadline, eastern), 'mit':mit, 'travel':travel}}

ConfirmationPermission = Permission(AttributeNeed('admit', 'pending'))

UpdatePermission = Permission(AttributeNeed('admit', 'update'))

ResumePermission = ConfirmationPermission.union(UpdatePermission)

register_policy_route('/accounts/<int:account_id>/resume/policy', 'resume', ResumePermission, lambda kwargs: 'accounts/' + str(kwargs['account_id']) + '/resume.pdf')

register_policy_route('/accounts/<int:account_id>/travel/policy', 'travel', ConfirmationPermission, lambda kwargs: 'accounts/' + str(kwargs['account_id']) + '/travel.pdf')

@bp.route('/confirmation')
@ConfirmationPermission.require()
def confirmation():
    attendee = Attendee.lookup_from_account_id(current_user.id).get_attendee_data()
    if attendee['badge_name'] is None:
        attendee['badge_name'] = current_user.get_name()
    admit = Admit.lookup_from_account_id(current_user.id).get_admit_data()

    admit['deadline'] = format_utc_datetime(Admit.lookup_from_account_id(current_user.id).get_deadline(), eastern)

    resume= {}
    resume['policy_endpoint'] = '/accounts/' + str(current_user.id) + '/resume/policy'
    resume['resource_name'] = "PDF"

    hacker = Hacker.lookup_from_account_id(current_user.id)
    bus = (hacker.school_id in buses)
    mit = (hacker.school_id == 166683)

    travel= {}
    travel['policy_endpoint'] = '/accounts/' + str(current_user.id) + '/travel/policy'
    travel['resource_name'] = "Travel Confirmation"

    return render_full_template('confirmation.html', attendee=attendee, admit=admit, s3=s3_config(), resume=resume, bus=bus, mit=mit, travel_reimbursement=travel)

@bp.route('/admits', methods=['PUT'])
@ConfirmationPermission.require()
def update_confirmation():
    form = ConfirmationForm()
    # First find the hacker if they already exist
    if not form.validate_on_submit():
        raise BadDataError()

    hacker = Hacker.lookup_from_account_id(current_user.id)

    if form.resumeOptOut.data is False and form.resume.data is False:
        raise BadDataError()

    if hacker.school_id!=166683 and form.meng.data is True:
        raise BadDataError()

    attendee = Attendee.lookup_from_account_id(current_user.id)
    admit = Admit.lookup_from_account_id(current_user.id)
    
    with db_safety() as session:
        attendee.update_attendee_data(session, form.badge.data, form.shirt.data, form.phone.data)
        admit.update_admit_data(session, form.graduation.data, form.meng.data, form.diet.data, form.waiver.data, form.photoRelease.data, form.resumeOptOut.data, form.resume.data, form.github.data, form.travel.data, form.likelihood.data)
    return jsonify({'message': "Successfully Updated!"})

@bp.route('/update')
@UpdatePermission.require()
def profile():
    admit = Admit.lookup_from_account_id(current_user.id)
    admit_id = admit.id
    admit_data = admit.get_admit_data()
    resume= {}
    resume['policy_endpoint'] = '/accounts/' + str(current_user.id) + '/resume/policy'
    resume['resource_name'] = "PDF"

    hacker = Hacker.lookup_from_account_id(current_user.id)
    mit = (hacker.school_id == 166683)

    profile = Profile.lookup_from_admit_id(admit_id)
    if profile is None:
        with db_safety() as session:
          Profile.create(session, admit_id)
        profile = Profile.lookup_from_admit_id(admit_id)
    profile_data = profile.get_profile_data()

    return render_full_template('update.html', admit=admit_data, profile=profile_data, s3=s3_config(), resume=resume, mit=mit)

@bp.route('/profiles', methods=['PUT'])
@UpdatePermission.require()
def update_profile():
    form = UpdateForm()
    if not form.validate_on_submit():
        raise BadDataError()
    if form.resumeOptOut.data is not False or form.resume.data is not True:
        raise BadDataError()

    hacker = Hacker.lookup_from_account_id(current_user.id)
    mit = (hacker.school_id == 166683)
    admit = Admit.lookup_from_account_id(current_user.id)
    profile = Profile.lookup_from_admit_id(admit.id)
     # != is xor for boolean values, == is xnor for boolean values

    if mit == (form.pets.data is not None):
        raise BadDataError()

    if admit.travel == ('' == form.address.data):
        raise BadDataError()

    with db_safety() as session:
        admit.update_profile_data(session, form.resumeOptOut.data, form.resume.data, form.github.data)
        if form.pets.data is not None:
            profile.update_hosting_data(session, form.mitHost.data, form.nonSmoking.data, form.pets.data, form.considerations.data)
        if '' != form.address.data:
            profile.update_address_data(session, form.address.data)
    return jsonify({'message': "Successfully Updated!"})
