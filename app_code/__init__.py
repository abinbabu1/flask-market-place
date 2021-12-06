
from flask import Flask
from flask_bs4 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'e2353ddeb887430fa070a2ace07dd719'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from .auth import auth
from .views import views

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
