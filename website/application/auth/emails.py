from ..emails import send_email

@send_email('account_confirmation')
def send_account_confirmation_email(email_address, **kwargs):
    return ("Welcome to HackMIT!", kwargs)

@send_email('forgot_password')
def send_forgot_password_email(email_address, **kwargs):
    return ("Password Recovery!", kwargs)

@send_email('password_reset')
def send_password_reset_email(email_address, **kwargs):
    return ("Your password has been reset!", kwargs)

