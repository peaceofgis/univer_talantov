import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "cars"


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://blog:blog@localhost/' + db_name


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, db_name + '.db')
