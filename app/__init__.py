from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# Feed it the flask app instance
# ui = FlaskUI(app, host="127.0.0.1", port="8000", width=1600, height=1000)

# call the 'run' method
# ui.run()

if __name__ == '__main__':
    app.run()