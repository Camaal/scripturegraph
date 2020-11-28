import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'c3b1ddc124344a8b8bda21e13b722369'
    SQLALCHEMY_DATABASE_URI = 'postgres://fuhspbzpscsndk:b306496bc6f04a60fdac722b019eb00afb6337ad32ceaf1f515f8bd29deeadb4@ec2-34-200-106-49.compute-1.amazonaws.com:5432/d8un9299fdbl4b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
