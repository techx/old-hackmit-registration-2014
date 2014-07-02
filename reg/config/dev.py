import base
class DevelopmentConfig(base.Config):
    PORT = 5001
    DEBUG = True
    SECRET_KEY = "THIS DOESN'T MATTER!"
    SERVER_NAME = 'localhost:5001'
    SQLALCHEMY_BINDS = {
        'local':   'sqlite:///dev-local.db',
        'central': 'sqlite:///dev-central.db'
    }
