from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskwebgui import FlaskUI #get the FlaskUI class


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# Feed it the flask app instance
ui = FlaskUI(app, host="127.0.0.1", port="8000", width=1920, height=1080)

# call the 'run' method
# ui.run()





