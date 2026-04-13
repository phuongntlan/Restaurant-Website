from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileField

class RegisterForm(FlaskForm):
    username = StringField(label = 'username', validators = [Length(min = 2, max = 30), DataRequired()])
    fullname = StringField(label = 'fullname', validators = [Length(min=3, max = 30), DataRequired()])
    address = StringField(label = 'address', validators = [Length(min=7, max = 50), DataRequired()])
    phone_number = IntegerField(label = 'phone_number', validators = [DataRequired()]) #try to find phone
    password1 = PasswordField(label = 'password1', validators = [Length(min = 6), DataRequired()])
    password2 = PasswordField(label = 'password2', validators = [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label = 'Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label = 'username', validators = [DataRequired()])
    password = PasswordField(label = 'password', validators = [DataRequired()])
    submit = SubmitField(label = 'Sign In')

class OrderIDForm(FlaskForm):
    orderid = StringField(label ='order-id', validators = [Length(min = 1), DataRequired()])      
    submit = SubmitField(label = 'Track')

class ReserveForm(FlaskForm):
    # Using SelectField for dynamic data
    date = SelectField('Date', validators=[DataRequired()])
    time_slot = SelectField('Time Slot', validators=[DataRequired()])
    guest_count = SelectField('Guests', validators=[DataRequired()])
    
    submit = SubmitField(label='Reserve')

class AddForm(FlaskForm):
    submit = SubmitField(label = 'Add')
    
class OrderForm(FlaskForm):
    submit = SubmitField(label = 'Order Now')

class DishForm(FlaskForm):
    name = StringField(label = 'name', validators=[DataRequired(), Length(min=2, max=30)])
    description = TextAreaField(label = 'description', validators=[DataRequired(), Length(max=50)])
    price = IntegerField(label = 'price', validators=[DataRequired(), NumberRange(min=0)])
    source = FileField(label = 'source', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Only file image')])  
    submit = SubmitField(label = 'Save')

class TableForm(FlaskForm):
    table_name = StringField(label = 'name', validators=[DataRequired(), Length(min=2, max=30)])
    capacity = IntegerField(label = 'capacity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField(label = 'Save')

class ConfirmBookingForm(FlaskForm):
    date = HiddenField('Date', validators=[DataRequired()])
    guests = HiddenField('Guests', validators=[DataRequired()])
    time_slot = HiddenField('Time Slot', validators=[DataRequired()])
    submit = SubmitField(label = 'Confirm Reservation')
