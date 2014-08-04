from flask.ext.mail import Mail, Message, email_dispatched

from . import render_full_template

mail = Mail()

# Nifty decorator to do 90% of the work
def send_email(template_name):
    def wrap(subject_func):
        def wrapped_send_email_function(email_address, **kwargs):
            subject, render_kwargs = subject_func(email_address, **kwargs)
            msg = Message(subject, recipients=[email_address])
            msg.body = render_full_template('emails/' + template_name + '.email.txt', **render_kwargs)
            msg.html = render_full_template('emails/' + template_name + '.email.html', **render_kwargs)
            mail.send(msg)
        return wrapped_send_email_function
    return wrap

from . import app

if app.config['DEBUG']:
    def print_message(message, app):
        print "SENT EMAIL MESSAGE:"
        print "recipients: " + repr(message.recipients)
        print "html:       " + repr(message.html)
        print "plain text: " + repr(message.body)
    email_dispatched.connect(print_message)
