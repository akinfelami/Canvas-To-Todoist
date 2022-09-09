from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os



app =  Flask(__name__)


# Databse config
basedir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(basedir, "app.db")) 
app.config["SQLALCHEMY_DATABASE_URI"] = db_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = os.getenv('somerandomstring')

# Blueprints

from .routes.users import users
from .routes.tasks import tasks

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(tasks, url_prefix='/tasks')


@app.route('/')
def index():
    return render_template('index.html')