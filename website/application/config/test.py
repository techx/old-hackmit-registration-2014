import base
class TestingConfig(base.Config):
    TESTING = True
    SECRET_KEY = "I'm just testing some things out!"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests/test.db'
