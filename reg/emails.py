from flask import current_app, render_template
from flask.ext.mail import Mail, Message

mail = Mail()

# Nifty decorator to do 90% of the work
def send_email(template_name):
    def wrap(subject_func):
        def wrapped_send_email_function(email_address, **kwargs):
            #if not(current_app.config['DEBUG']):                
                subject, render_kwargs = subject_func(email_address, **kwargs)
                msg = Message(subject, recipients = [email_address], sender=current_app.config['DEFAULT_MAIL_SENDER'])
                msg.body = render_template(template_name + '.email.txt', **render_kwargs)
                msg.html = render_template(template_name + '.email.html', **render_kwargs)
                mail.send(msg)
        return wrapped_send_email_function
    return wrap

@send_email('account_confirmation')
def send_account_confirmation_email(email_address, **kwargs):
    return ("Welcome to HackMIT!", kwargs)
