from functools import wraps

from flask import render_template, request, redirect, url_for, jsonify, current_app
from flask.ext.login import login_required, login_user, current_user, logout_user
from itsdangerous import BadSignature, URLSafeTimedSerializer, SignatureExpired

from ..util.toposort import toposort

from ..errors import ServerError, BadDataError
from ..models import db_safety

from . import bp, roles, login_manager
from .emails import send_account_confirmation_email, send_forgot_password_email, send_password_reset_email
from .errors import AuthenticationError
from .forms import LoginForm, RegistrationForm, ResetForm, ForgotForm, ForgotResetForm
from .models import Account

def roles_with_context(view_name):
    roles_for_view = []

    for role in roles:
        if roles[role]['model'].lookup_from_account_id(current_user.id) is not None:
            if roles[role][view_name] is not None:
                roles_for_view.append(role)

    toposort(roles_for_view, lambda collection, item: roles[item]['model'].implied_roles())

    return [(role, roles[role][view_name]()) for role in roles_for_view]

# Implies the @login_required decorator
def email_confirmed(function):
    @login_required
    @wraps(function)
    def wrapped_email_confirmed_function(**kwargs):
        if not current_user.email_confirmed():
            return render_template('server_message.html', header="You need to verify your email to get here!", subheader="You can resend the confirmation email from the dashboard.")
        else:
            return function(**kwargs)
    return wrapped_email_confirmed_function

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login')) # Use auth.login (full form) so this works correctly when invoked from some other blueprint

@bp.route('/register')
def get_registration_page():
    if current_user.is_authenticated():
        return redirect(url_for('.dashboard'))
    else:
        return render_template('register.html')

@bp.route('/accounts', methods=['POST'])
def register_user():
    form = RegistrationForm()
    role = form.role.data
    email_address = form.email.data
    hashed_password = form.hashedPassword.data

    if not (form.validate_on_submit() and role in roles and roles[role]['model'].is_registrable()):
        raise BadDataError()

    if Account.lookup_from_email(email_address) != None:
        raise ServerError('This account already exists!', status_code=409)

    with db_safety() as session:
        account_id = Account.create(session, email_address, hashed_password, role)

    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    confirm = s.dumps(account_id)

    send_account_confirmation_email(email_address, confirm=confirm)

    return jsonify({'message': 'Successfully Registered!'})

@bp.route('/account/resend')
@login_required
def resend_email():
    if current_user.email_confirmed():
        render_template('server_message.html', header="You're already confirmed!", subheader="We do, however, appreciate your enthusiasm.")
    account_id = current_user.id
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    confirm = s.dumps(account_id)
    email_address = current_user.email_address
    send_account_confirmation_email(email_address, confirm=confirm)
    return redirect(url_for('.dashboard'))

@bp.route('/accounts/<account_id>', methods=['PUT'])
@login_required
def update(account_id):

    form = ResetForm()
    email = form.email.data
    old_password = form.oldPassword.data
    new_password = form.newPassword.data

    account = Account.query.get(int(account_id))

    if account is None:
        raise AuthenticationError("You don't have an account!")

    if account.email_address != email:
        raise AuthenticationError("Your email doesn't seem to match our records.")

    if not account.check_password(old_password):
        raise AuthenticationError("Your password is wrong!")

    if old_password == new_password:
        raise ServerError("Your new password can't be the same as your old password!", status_code=409)

    with db_safety() as session:
        account.update_password(session, new_password)

    logout_user()

    return jsonify({"message": "Password successfully updated!"})

@bp.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect(url_for('.dashboard'))
    else:
        return render_template('login.html')

@bp.route('/sessions', methods=['POST'])
def sessions():
    form = LoginForm()

    if not form.validate_on_submit():
        raise BadDataError()

    email_address = form.email.data
    hashed_password = form.hashedPassword.data

    stored_account = Account.lookup_from_email(email_address)

    if stored_account == None:
        raise AuthenticationError("Sorry, it doesn't look like you have an account.")

    if not stored_account.check_password(hashed_password):
        raise AuthenticationError("Your username or password do not match.")

    login_user(stored_account)

    return jsonify({'url': url_for('.dashboard')})

@bp.route('/dashboard')
@login_required
def dashboard():
    email_confirmed = False # Email is confirmed

    account = load_user(current_user.id)

    if account.email_confirmed():
        email_confirmed = True

    name = account.get_name()

    return render_template('dashboard.html', email_confirmed=email_confirmed, name=name, roles=roles_with_context('dashboard'))

@bp.route('/confirm')
def confirm():
    confirm_code = request.args.get('confirm')
    if confirm_code != None:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            confirm_user_id = s.loads(confirm_code, max_age=86400) # Max age of 24 hours
            account = Account.query.get(int(confirm_user_id))
            if account is None:
                return render_template('server_message.html', header="You don't seem to have an account.", subheader="What are you waiting for? Go register!")

            with db_safety() as session:
                account.confirm_email(session)

            email_confirmed = True

            return redirect(url_for('.login'))
        except SignatureExpired:
            return render_template('server_message.html', header="Oops. Your email confirmation link has expired.", subheader="You should probably try again!")
        except BadSignature:
            pass

    return render_template('server_message.html', header="That's not a valid confirmation code!", subheader="Check for typos in the link, or login and resend the confirmation email.")

@bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'GET':
        token = request.args.get('token')
        if current_user.is_authenticated():
            return redirect(url_for('.dashboard'))
        elif token is None:
            return render_template('forgot.html')
        else:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            try:
                confirm_user_id = s.loads(token, max_age=1800) # Max age of 30 minutes
                account = load_user(confirm_user_id)
                if account is None:
                    return render_template('server_message.html', header="You don't seem to have an account.", subheader="What are you waiting for? Go register!")
                return render_template('forgot_set_password.html', token=token)
            except SignatureExpired:
                return render_template('server_message.html', header="Oops. Your token has expired.", subheader="You should probably try again!")
            except BadSignature:
                return render_template('server_message.html', header="Oops. Your token is invalid.")

    if request.method == 'POST':
        form = ForgotForm()
        email = form.email.data
        account = Account.lookup_from_email(email)
        if account != None:
            # Send an email to reset
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(account.id)

            send_forgot_password_email(email, token=token)

            return jsonify({"message": "Email sent! Check your email for a link to reset your password."})
        else:
            raise AuthenticationError("This account doesn't exist!")

@bp.route('/accounts/reset', methods=['POST'])
def forgot_reset():
    token = request.args.get('token')
    if token is None:
        return render_template('server_message', header="You can't forgot the password for an account that doesn't exist!", subheader="Go register for a real account now!")
    form = ForgotResetForm()
    new_password = form.newPassword.data
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        confirm_user_id = s.loads(token, max_age=1800) # Max age of 30 minutes
        account = load_user(confirm_user_id)
        if account is None:
            return render_template('server_message.html', header="You don't seem to have an account.", subheader="What are you waiting for? Go register!")

        with db_safety() as session:
            # In case the user hasn't already been confirmed.
            account.confirm_email(session)

            account.update_password(session, new_password)

        # Notify the user that their password has been reset
        send_password_reset_email(account.email_address)

        return jsonify({"message": "You have successfully reset your password!"})

    except SignatureExpired:
        return render_template('server_message.html', header="Oops. Your token has expired.", subheader="You should probably try again!")

    except BadSignature:
        return render_template('server_message.html', header="Oops. Your token is invalid.")

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@bp.route('/reset')
@login_required
def reset():
    email = current_user.email_address
    return render_template('reset.html', email=email)

