from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import *
import os
#from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#This makes the website crash
login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#moment = Moment(app)

from app import routes, models 