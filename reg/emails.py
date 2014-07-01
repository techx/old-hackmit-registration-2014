from flask import current_app, render_template
from flask.ext.mail import Mail, Message

mail = Mail()


# Nifty decorator to do 90% of the work
def send_email(template_name):
    def wrap(subject_func):
        def wrapped_func(email_address, **kwargs):        
            if not(current_app.config['DEBUG'] or current_app.config['TESTING']):
                msg = Message(subject_func(email_address), recipients = [email_address], sender=current_app.config['DEFAULT_MAIL_SENDER'])
                msg.body = render_template(template_name + '.email.txt')
                msg.html = render_template(template_name + '.email.html')
                mail.send(msg)
        return wrapped_func
    return wrap

# Note: Email functions return subjects for a few reasons:
# 1) Prevents another file with just one line of text
# 2) Makes it easy to see what each function is for
# 3) Gives the functions something to do :)

@send_email('account_confirmation')
def send_account_confirmation_email(email_address):
    return "Welcome to HackMIT!"
