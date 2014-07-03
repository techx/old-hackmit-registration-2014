import base
class DevelopmentConfig(base.Config):
    PORT = 5001
    DEBUG = True
    SECRET_KEY = "THIS DOESN'T MATTER!"
    SQLALCHEMY_BINDS = {
        'local':   'sqlite:///dev-local.db',
        'central': 'sqlite:///dev-central.db'
    }
