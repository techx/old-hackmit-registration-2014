from binascii import unhexlify

from flask import current_app, redirect

from .. import app, render_full_template

from . import bp

@bp.route('/')
def index():
    return render_full_template('index.html')

@bp.route('/sponsor')
def sponsors():
    return bp.send_static_file('assets/docs/HackMIT2014Sponsorship.pdf')

with app.app_context():
    extra = current_app.config.get('EXTRA_URL')
if extra is not None:
    @bp.route('/' + extra)
    def hex():
        try:
            template_name = unhexlify(extra)
            return render_full_template(template_name + '.html')
        except TypeError:
            pass

@bp.route('/walkin')
def walkin():
    # Temporary redirect in case we need to change
    return redirect('https://techx.wufoo.com/forms/hackmit-walkin-registration/', code=307)

@bp.route('/dayof')
def dayof():
    # Temporary redirect in case we switch off of gh-pages
    return redirect('http://dayof.hackmit.org/', code=307)

@bp.route('/mentormatching')
def mentor_matching():
    return redirect('https://techx.wufoo.com/forms/hackmit-mentor-matching/', code=307)

@bp.route('/massages')
def massages():
    return redirect('https://techx.wufoo.com/forms/hackmit-massage-signup/', code=307)
