from flask import Flask
from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tables.db'
app.config['SECRET_KEY'] = '1b1bdc96eb8dba64b0fc5ae2'

db = SQLAlchemy(app)

# import model
# from .models import User

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #to redirect user to login page if login required


# create tables
from restaurant.models import User
from sqlalchemy import inspect
with app.app_context():
    db.create_all()
    print("Already created") # debug
    ins = inspect(db.engine) 
    print(ins.get_table_names())

#OTP API
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
# api = AuthyApiClient(app.config['AUTHY_API_KEY'])

from restaurant import routes 
