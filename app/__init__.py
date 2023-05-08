from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_session import Session


app = Flask(__name__)
app.config.from_object(Config)

Session(app)
mongo_client = PyMongo(app)
db = mongo_client.db


# login = LoginManager(app)
# login.login_view = 'login'


from app import routes