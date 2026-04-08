from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from restaurant.models import Table, User, Item, Reservation
from restaurant.forms import RegisterForm, LoginForm, OrderIDForm, ReserveForm, AddForm, OrderForm, DishForm, TableForm
from restaurant import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

# Create blueprint prefix /admin/
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Check 
@admin_bp.before_request
def restrict_admin_access():
    # Allow access admin/login without admin role
    if request.endpoint == 'admin.login':
        print("LMAOOOO")
        return
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("You are not an admin", category="danger")
        return redirect(url_for('home_page')) # Chuyển hướng về trang chủ

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("ADMIN/LOGIN")
    if current_user.is_authenticated and current_user.is_admin:
        print(current_user.is_authenticated)
        print(current_user.is_admin)
        return redirect(url_for('admin.dashboard'))
    print('going')
    forml = LoginForm()
    if forml.validate_on_submit():
        attempted_user = User.query.filter_by(username = forml.username.data).first() #get username data entered from sign in form
        if attempted_user and attempted_user.check_password_correction(attempted_password = forml.password.data): #to check if username & password entered is in user database
            if attempted_user.is_admin:
                login_user(attempted_user) #checks if user is registered 
            # flash(f'Signed in successfully as: {attempted_user.username}', category = 'success')
                print("THIS IS ADMIN")
            else:
                print("this is not admin")
            return redirect(url_for('admin.dashboard'))
        else:
            print("passowrd incorrect")
            flash('Username or password is incorrect! Please Try Again', category = 'danger') #displayed in case user is not registered
    else:
        print("invalid")
    return render_template('admin/login.html', forml = forml)

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/manage_menu', methods=['GET', 'POST'])
def manage_menu():
    form = DishForm()
    if form.validate_on_submit():
        target_id = request.form.get('item_id')
        
        if target_id:
            item = Item.query.filter_by(item_id=target_id).first()
        else:
            item = Item()

        if form.source.data:
            file = form.source.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'img', filename)
            file.save(upload_path)
            item.source = filename
        elif not target_id:
            item.source = "default.jpg"

        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data

        try:
            if not target_id:
                db.session.add(item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # flash(f"Lỗi: {str(e)}", "danger")

        return redirect(url_for('admin.manage_menu'))

    # Lấy toàn bộ danh sách món để hiển thị ra bảng
    items = Item.query.all()
    return render_template('admin/manage-menu.html', form=form, items=items)

@admin_bp.route('/delete_dish/<int:item_id>', methods=['POST'])
def delete_dish(item_id):
    item = Item.query.get(item_id)
    if item.source and item.source != "default.jpg":
        image_path = os.path.join(current_app.root_path, 'static', 'img', item.source)
        if os.path.exists(image_path):
            os.remove(image_path)
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('admin.manage_menu'))

@admin_bp.route('/manage_tables', methods=['POST', 'GET'])
def manage_tables():
    form = TableForm();
    if request.method == 'POST':
        table_id = request.form.get('table_id')
        name = request.form.get('table_name')
        cap = request.form.get('capacity')
        
        if table_id: # Edit Mode
            table = Table.query.get(table_id)
            table.table_name = name
            table.capacity = cap
        else: # Add Mode
            new_table = Table(table_name=name, capacity=cap)
            db.session.add(new_table)
            
        db.session.commit()
        return redirect(url_for('admin.manage_tables'))
        
    tables = Table.query.all()
    return render_template('admin/manage_tables.html', form=form, tables=tables)

@admin_bp.route('/delete_table/<int:table_id>', methods=['POST'])
def delete_table(table_id):
    table = Table.query.get(table_id)
    if table.source:
        db.session.delete(table)
        db.session.commit()
    return redirect(url_for('admin.manage_tables'))

@admin_bp.route('/manage_reservations', methods=['POST', 'GET'])
def manage_reservations():
    reservations = Reservation.query.all()
    return render_template('admin/manage_reservations.html', reservations = reservations)
@admin_bp.route('/logout')
def logout():
    return redirect(url_for('main.logout'))