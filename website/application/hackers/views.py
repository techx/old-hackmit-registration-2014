from functools import wraps

from flask import render_template, jsonify
from flask.ext.login import current_user

from ..models import db_safety

from ..errors import BadDataError

from ..auth.models import Account
from ..auth.views import email_confirmed

from . import bp
from .forms import LotteryForm
from .models import Hacker, Team

MAX_TEAM_SIZE = 4

def dashboard():
    lottery_complete = False # Lottery is complete, also show teams
    hacker = Hacker.lookup_from_account_id(current_user.id)
    if hacker.lottery_submitted():
        lottery_complete = True
    return {'name':'hacker_dashboard.html', 'context':{'lottery_complete':lottery_complete}}

# Implies the @login_required and @email_confirmed decorators
def hackers_only(function):
    @email_confirmed
    @wraps(function)
    def wrapped_hackers_only_function(*args, **kwargs):
        hacker = Hacker.lookup_from_account_id(current_user.id)
        if not hacker:
            return render_template('server_message.html', header="You need to be a hacker to access this!", subheader="This ain't a UNIX file system.")
        else:
            return function(*args, **kwargs)
    return wrapped_hackers_only_function

# Implies the @login_required, @email_confirmed, and @hackers_only decorators
def lottery_submitted(function):
    @hackers_only
    @wraps(function)
    def wrapped_lottery_submitted_function(*args, **kwargs):
        hacker = Hacker.lookup_from_account_id(current_user.id)
        if not hacker.lottery_submitted():
            return render_template('server_message.html', header="You need to submit the lottery form to do that!", subheader="Hope you're feeling lucky.")
        else:
            return function(*args, **kwargs)
    return wrapped_lottery_submitted_function


@bp.route('/hackers', methods=['POST'])
@hackers_only
def hackers():
    form = LotteryForm()
    # First find the hacker if they already exist
    if not form.validate_on_submit():
        raise BadDataError()

    if form.school_id.data != "166683" and form.adult.data is not True:
        raise BadDataError("Sorry, you need to be 18+ at the time of HackMIT to attend. Maybe next year?")

    previous_hacker_with_code = Hacker.lookup_from_invite_code(form.inviteCode.data)

    if form.inviteCode.data != "" and previous_hacker_with_code is not None and previous_hacker_with_code.account_id != current_user.id:
        raise BadDataError("Somebody beat you to it! That code has already been used. Try again or submit without a code to save your data.")

    hacker = Hacker.lookup_from_account_id(current_user.id)
    
    with db_safety() as session:
        current_user.update_name(session, form.name.data)
        hacker.update_lottery_data(session, form.gender.data, form.school_id.data, form.school.data, form.adult.data, form.location.data, form.inviteCode.data, form.interests.data)

    return jsonify({'message': "Successfully Updated!"})

@bp.route('/lottery')
@hackers_only
def lottery():
    name = current_user.get_name()
    hacker = Hacker.lookup_from_account_id(current_user.id).get_hacker_data()
    return render_template('lottery.html', name=name, hacker=hacker)

@bp.route('/team')
@lottery_submitted
def team():
    hacker = Hacker.lookup_from_account_id(current_user.id)
    team_id = hacker.team_id
    team = None

    if team_id:
        team = {}
        teammateAccounts = [
            {
                "id": hacker.account_id,
                "name": hacker.name
            }
            for hacker in Hacker.lookup_from_team_id(team_id)
        ]
        teammates = [
            {
                "name": account["name"],
                "email": Account.query.get(int(account["id"])).email_address
            }
            for account in teammateAccounts
        ]
        team["teammates"] = teammates
        team["teamInviteCode"] = Team.query.get(int(team_id)).team_invite_code

    return render_template('team.html', team=team)

@bp.route('/team/leave', methods=['POST'])
@lottery_submitted
def leave_team():
    hacker = Hacker.lookup_from_account_id(current_user.id)

    with db_safety() as session:
        hacker.join_team(session, None)

    return jsonify({'message': "It's been real, see ya!"})

@bp.route('/teams', methods=['POST'])
@lottery_submitted
def teams():
    hacker = Hacker.lookup_from_account_id(current_user.id)

    with db_safety() as session:
        team_id = Team.create(session)
        hacker.join_team(session, team_id)

    return jsonify({'message': "Team successfully created"})

@bp.route('/teams/<team_invite_code>', methods=['POST'])
@lottery_submitted
def join_team(team_invite_code):

    # Find the team associated with the invite code
    team = Team.query.filter_by(team_invite_code=team_invite_code).first()

    if team is None:
        raise BadDataError("Aww. That doesn't seem to be a valid invite code.")

    members = Hacker.lookup_from_team_id(team.id)

    if len(members) >= MAX_TEAM_SIZE:
        raise BadDataError("Aww. There are too many people on this team!")

    # Get the current hacker
    hacker = Hacker.lookup_from_account_id(current_user.id)

    with db_safety() as session:
        hacker.join_team(session, team.id)

    return jsonify({'message': "Hacking is better with friends!"})

