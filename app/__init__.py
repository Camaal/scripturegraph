from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////cm_bible.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models
