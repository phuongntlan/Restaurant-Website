from wtforms.validators import Length
from restaurant import db, login_manager
from restaurant import bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func

#used for logging in users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#USER TABLE
class User(db.Model, UserMixin):
    #consider changing id to user_id
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    fullname = db.Column(db.String(length = 30), nullable = False)
    address = db.Column(db.String(length = 50), nullable = False)
    phone_number = db.Column(db.Integer(), nullable = False)
    password_hash = db.Column(db.String(length = 60), nullable = False)

    bookings = db.relationship('Reservation', backref='customer', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        return self.password
    
    #hashes the user's password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    #verifies if the entered password in sign in form matches the user's password in the database
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
#TABLE RESERVATION TABLE
class Table(db.Model):
    #consider changing id to table_id
    table_id = db.Column(db.Integer(), primary_key = True)
    table_name = db.Column(db.String(length = 5), nullable = False)
    capacity = db.Column(db.Integer(), nullable = False)
    all_orders = db.relationship('Reservation', backref='table_info', lazy=True)

#MENU TABLE
class Item(db.Model):
    #consider changing id to item_id
    item_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False)
    description = db.Column(db.String(length = 50), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    source = db.Column(db.String(length = 30), nullable = False)
 

# #ORDERS TABLE
# class Order(db.Model):
#     order_id = db.Column(db.Integer(), primary_key = True)
#     name = db.Column(db.String(length = 30), db.ForeignKey('user.username'))
#     address = db.Column(db.String(length = 30), nullable = False)
#     order_items = db.Column(db.String(length = 300), nullable = False)
#     datetime = db.Column(db.DateTime(timezone = True), server_default = func.now())

#     #function for assigning ownership to the user's order
#     # def set_info(self, user):
#     #     self.name = user.username
#     #     self.addresss = user.address 
#     #     # self.order_items = item.name #where name has orderer
#     #     db.session.commit()

# #CART TABLE

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False) 
    time_slot = db.Column(db.String(30), nullable=False)
    guest_count = db.Column(db.Integer(), nullable = False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.table_id'))

    # #function for assigning ownership to the user's selected item
    # def assign_ownership(self, user):
    #     self.orderer = user.id 
    #     db.session.commit()

    # def remove_ownership(self, user):
    #     self.orderer = None
    #     db.session.commit()