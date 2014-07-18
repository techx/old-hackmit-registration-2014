from binascii import unhexlify

from flask import render_template, current_app

from .. import app

from . import bp

@bp.route('/')
def index():
    return render_template('index.html')

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
            return render_template(template_name + '.html')
        except TypeError:
            pass
