from os import environ
from binascii import unhexlify

from flask import Flask, render_template
from flask_sslify import SSLify

application = Flask(__name__,instance_relative_config=True)

# For AWS
app = application

try:
    configuration_module_name = environ['HACKMIT_FLASK_CONFIG_MODULE']
    app.config.from_object(configuration_module_name)
except KeyError:
    app.config.from_object('config.dev.DevelopmentConfig')

# Redirect all requests to HTTPS
sslify = SSLify(app, permanent=True)

@app.errorhandler(404)
def not_found(error):
    return render_template('server_message.html', header="404", subheader="Whoa, you must be lost.")

@app.route('/')
def index():
    return render_template('index.html')

extra = app.config.get('EXTRA_URL')
if extra is not None:
    @app.route('/' + extra)
    def hex():
        try:
            template_name = unhexlify(extra)
            return render_template(template_name + '.html')
        except TypeError:
            pass

@app.route('/sponsor')
def sponsors():
    return app.send_static_file('assets/docs/HackMIT2014Sponsorship.pdf')

if __name__ == '__main__':
    port = app.config['PORT']
    if not port:
        port = 5000 # Default
    debug = app.config['DEBUG']
    if not debug:
        print 'NOT DEBUG'
    app.run(port=port, debug=debug)
