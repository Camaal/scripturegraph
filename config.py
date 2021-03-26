import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/camaalmoten/PycharmProjects/scripturegraph/cm_bible.db'
    SECRET_KEY = '38fb6d0e8452487584a03de1290fd1f7'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
