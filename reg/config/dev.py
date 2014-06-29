import base
class DevelopmentConfig(base.Config):
    DEBUG = True
    SECRET_KEY = "THIS DOESN'T MATTER!"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
