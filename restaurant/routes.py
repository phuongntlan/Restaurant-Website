# from . import app
from restaurant import app
from flask import render_template, redirect, url_for, flash, request, session, Response, jsonify
from restaurant.models import Table, User, Item, Reservation
from restaurant.forms import RegisterForm, LoginForm, OrderIDForm, ReserveForm, AddForm, OrderForm, ConfirmBookingForm
from restaurant import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy.orm import joinedload

@app.route('/')
#HOME PAGE
@app.route('/home')
def home_page(): 
    return render_template('index.html')

#MENU PAGE
@app.route('/menu', methods = ['GET', 'POST'])
@login_required
def menu_page():
    add_form = AddForm()
    if request.method == 'POST':
        selected_item = request.form.get('selected_item') #get the selected item from the menu page
        s_item_object = Item.query.filter_by(name = selected_item).first()
        if s_item_object:
            s_item_object.assign_ownership(current_user) #assign ownership of the ordered item to the user
        
        return redirect(url_for('menu_page'))
    
    if request.method == 'GET':
        items = Item.query.all()
        return render_template('menu.html', items = items, add_form = add_form)

#CART PAGE
@app.route('/cart', methods = ['GET', 'POST'])
def cart_page():
    order_form = OrderForm()
    if request.method == 'POST':
        ordered_item = request.form.get('ordered_item') #get the ordered item(s) from the cart page
        o_item_object = Item.query.filter_by(name = ordered_item).first()
        order_info = Order(name = current_user.fullname,
                           address = current_user.address,
                           order_items = o_item_object.name ) 

        db.session.add(order_info)
        db.session.commit()

        o_item_object.remove_ownership(current_user)    
        #return congrats page on successfull order
        return redirect(url_for('congrats_page'))
    
    if request.method == 'GET':
        selected_items = Item.query.filter_by(orderer = current_user.id)#get items which user has added to the cart
        return render_template('cart.html', order_form = order_form, selected_items = selected_items)

#CONGRATULATIONS PAGE
@app.route('/congrats')
def congrats_page():
    return render_template('congrats.html')   

#TABLE RESERVATION PAGE
@app.route('/table', methods = ['GET', 'POST'])
@login_required
def table_page():
    print('going on booking')
    print(request.form)
    form = ConfirmBookingForm()
    print(request.form)
    # Khi khách nhấn nút Submit (Confirm Reservation)
    if form.validate_on_submit():
        print("form validate")
        date = form.date.data
        actual_date = datetime.strptime(date, '%Y-%m-%d').date()
        guests = int(form.guests.data)
        time_slot = form.time_slot.data
        
        # Check for existing reservations for that date and time slot
        booked_ids = [r.table_id for r in Reservation.query.filter(
            Reservation.date == actual_date, 
            Reservation.time_slot == time_slot,
            Reservation.status != "Cancelled"
        ).all()]
       
        # Find the first table that fits the capacity and isn't booked
        target_table = Table.query.filter(
            Table.capacity >= guests, 
            ~Table.table_id.in_(booked_ids)
        ).first()
        if target_table:
            new_res = Reservation(
                date=actual_date, 
                time_slot=time_slot, 
                guest_count=guests, 
                table_id=target_table.table_id,
                user_id=current_user.id
            )
            db.session.add(new_res)
            db.session.commit()
            print("RES OK")
            flash("Reservation successful!", "success")
            return redirect(url_for('profile_page'))
        else:
            print("RES NO OK")
            flash("Sorry, that table was just taken!", "danger")
    else:
        print(form.errors)   
    return render_template('table.html', form=form)
# ct.table }} has been reserved successfully!")

        # return redirect(url_for('table_page'))

    # if request.method == 'GET':
    #     tables = Table.query.filter_by(reservee = None)
    #     return render_template('table.html', tables = tables, reserve_form = reserve_form)

#LOGIN PAGE
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    print("LOGIN")
    forml = LoginForm()
    if forml.validate_on_submit():
        attempted_user = User.query.filter_by(username = forml.username.data).first() #get username data entered from sign in form
        if attempted_user and attempted_user.check_password_correction(attempted_password = forml.password.data): #to check if username & password entered is in user database
            login_user(attempted_user) #checks if user is registered 
            # flash(f'Signed in successfully as: {attempted_user.username}', category = 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password is incorrect! Please Try Again', category = 'danger') #displayed in case user is not registered
    return render_template('login.html', forml = forml)

#FORGOT PASSWORD
@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    return render_template("forgot.html")

def return_login():
    return render_template("login.html")


#LOGOUT FUNCTIONALITY
@app.route('/logout')
def logout():
    logout_user() #used to log out
    flash('You have been logged out!', category = 'info')
    return redirect(url_for("home_page")) 

@app.route('/profile')
@login_required # Đảm bảo chỉ user đã đăng nhập mới vào được
def profile_page():
    # Sử dụng joinedload để lấy kèm thông tin table_info
    # (Lưu ý: dùng 'table' hoặc 'table_info' tùy theo backref bạn đặt trong Model)
    reservations = Reservation.query.filter_by(user_id=current_user.id)\
        .options(joinedload(Reservation.table_info))\
        .order_by(Reservation.date.desc()).all()
    
    return render_template('profile.html', reservations=reservations)
#REGISTER PAGE
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm() 
    #checks if form is valid
    if form.validate_on_submit():
        user_exists = User.query.filter_by(username = form.username.data).first() #get username data entered from sign up form
        if user_exists:
            flash("Username already exists!")
            return render_template('signup.html', form = form)
        else:
            user_to_create = User(username = form.username.data,
                                fullname = form.fullname.data,
                                address = form.address.data,
                                phone_number = form.phone_number.data,
                                password = form.password1.data,)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create) #login the user on registration 
            #  return redirect(url_for('verify'))
            return redirect(url_for('home_page'))
    
    if form.errors != {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('signup.html', form = form)

#ORDER ID PAGE
@app.route('/order_id', methods = ['GET', 'POST'])
def track_page():
    orderid = OrderIDForm()
    # if request.method == "POST":
    if orderid.validate_on_submit:
        #check to see if order id matches
        valid_orderid = Order.query.filter_by( order_id = orderid.orderid.data ).first()
        if valid_orderid:
            return redirect(url_for('delivery'))
        else:
            flash('Your Order-ID is invalid! Please Try Again.', category = 'danger')

    return render_template('order-id.html', orderid = orderid)

#DELIVERY TRACKING PAGE
@app.route('/deliverytracking')
def delivery():
    return render_template('track.html')


@app.route('/api/get-available-slots')
def get_slots():
    date_str = request.args.get('date')
    guests = int(request.args.get('guests'))
    print(date_str)
    print(guests)
    # --- CẤU HÌNH KHUNG GIỜ LINH HOẠT ---
    start_hour = 9  # Mở cửa lúc 9:00
    end_hour = 21   # Đóng cửa lúc 21:00 (slot cuối bắt đầu lúc 20:00)
    slot_duration = 1 # Mỗi slot kéo dài 1 tiếng
    
    all_slots = []
    for h in range(start_hour, end_hour):
        slot = f"{h:02d}:00-{(h + slot_duration):02d}:00"        # Lưu ý: Python không có padStart như JS, nên dùng f-string:
        # slot = f"{h:02d}:00-{(h + slot_duration):02d}:00"
        all_slots.append(slot)
    # ------------------------------------

    # 2. Query tìm bàn đủ chỗ
    tables = Table.query.filter(Table.capacity >= guests).all()
    if not tables:
        return jsonify({'slots': []})
        
    table_ids = [t.table_id for t in tables]
    
    # 3. Tìm các đơn đặt đã có
    reservations = Reservation.query.filter(
        Reservation.date == date_str,
        Reservation.table_id.in_(table_ids),
        Reservation.status != 'Cancelled'
    ).all()
    
    # 4. Logic loại trừ
    available_slots = []
    for slot in all_slots:
        booked_count = sum(1 for r in reservations if r.time_slot == slot)
        if booked_count < len(tables):
            available_slots.append(slot)
            
    return jsonify({'slots': available_slots})

@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    # Find the reservation and ensure it belongs to the current user
    reservation = Reservation.query.get_or_404(booking_id)
    
    if reservation.user_id != current_user.id:
        return {"message": "Unauthorized"}, 403

    # Option A: Delete the record
    # db.session.delete(reservation)
    
    # Option B: Just update the status (Better for business records)
    reservation.status = 'Cancelled'
    
    db.session.commit()
    return {"message": "Success"}, 200

# @app.route('/confirm-booking', methods=['POST'])
# def confirm_booking():
#     print('going confirm booking')
#     # Get selection from the hidden form
#     res_date = request.form.get('date')
#     res_guests = int(request.form.get('guests'))
#     res_time = request.form.get('time_slot')

#     print(res_date, res_guests, res_time)
#     # Find IDs of tables already taken at this time
#     booked_ids = [r.table_id for r in Reservation.query.filter_by(date=res_date, time_slot=res_time).all()]

#     # Find the first available table: Big enough AND not in the booked list
#     # Sorting by capacity ensures we don't waste a 10-person table for a 2-person group
#     target_table = Table.query.filter(
#         Table.capacity >= res_guests, 
#         ~Table.table_id.in_(booked_ids)
#     ).order_by(Table.capacity.asc()).first()

#     if target_table:
#         new_reservation = Reservation(
#             date=res_date, 
#             time_slot=res_time, 
#             guest_count=res_guests, 
#             table_id=target_table.table_id,
#             user_id=current_user.id # Assumes user is logged in
#         )
#         db.session.add(new_reservation)
#         db.session.commit()
#         print("Reservation successful!")
#         flash("Reservation successful!", "success")
#     else:
#         print("Sorry, that slot just filled up!")
#         flash("Sorry, that slot just filled up!", "danger")

#     return redirect(url_for('confirm_booking'))
# #OTP VERIFICATION
# @app.route("/verify", methods=["GET", "POST"])
# def verify():
#     country_code = "+91"
#     phone_number = current_user.phone_number
#     method = "sms"
#     session['country_code'] = "+91"
#     session['phone_number'] = current_user.phone_number

#     if request.method == "POST":
#             token = request.form.get("token") #OTP user entered

#             phone_number = session.get("phone_number")
#             country_code = session.get("country_code")

#             verification = api.phones.verification_check(phone_number,
#                                                          country_code,
#                                                          token)

#             if verification.ok():
#                 # return Response("<h1>Your Phone has been Verified successfully!</h1>")
#                 return render_template("index.html")
#             else:
#                 # return Response("<center><h1>Wrong OTP!</h1><center>")
#                 flash('Your OTP is incorrect! Please Try Again', category = 'danger')

#     return render_template("otp.html")


