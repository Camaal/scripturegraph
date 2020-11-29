import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL' or 'postgresql://postgres:postgres@localhost:5432/biblegraph')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
