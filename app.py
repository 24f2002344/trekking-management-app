from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_login import LoginManager,login_required,current_user,logout_user
from models import db, User, Trek
from routes.login import login_route_handler
from routes.registeration import registraiton_route_handler
from routes.admin import admin_dashboard_handler, toggle_user_status_handler, approve_staff_handler, add_trek_handler, assign_staff_to_trek_handler
from routes.user import book_trek_action_handler
from routes.staff import staff_dashboard_logic, staff_update_trek_logic, staff_update_profile_logic
from routes.payment import initiate_booking,payment_checkout
app = Flask(__name__)

# Basic database configuration


# Flask automatically knows to look inside the /instance folder for this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key_for_my_project'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader Callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# --- ROUTES ---

# ROOT PATH REDIRECT
@app.route('/')
def home():
    return redirect(url_for('register'))

# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_route_handler()

# LOGOUT ROUTE
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully signed out", "info")
    return redirect(url_for('login'))

# REGISTRATION ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():
    return registraiton_route_handler()


# --- ADMIN PANEL & MANAGEMENT ROUTES ---

# 1. Main Bento Dashboard Page
@app.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    return admin_dashboard_handler()

# 2. Status Toggle Form Target Action Route
@app.route('/admin/user/toggle/<int:user_id>', methods=['POST'])
def admin_toggle_user(user_id):
    return toggle_user_status_handler(user_id)

# 3. Staff Approval Form Target Action Route
@app.route('/admin/approve_staff/<int:user_id>', methods=['POST'])
def admin_approve_staff(user_id):
    return approve_staff_handler(user_id)

@app.route('/admin/trek/add',methods=['POST'])
def admin_add_trek():
    return add_trek_handler()

# DELETE TREK
@app.route('/admin/trek/delete/<int:trek_id>', methods=['POST'])
@login_required
def delete_trek(trek_id):
    # Security check: Ensure only admins can do this
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    # Find the trek in the database
    trek = Trek.query.get_or_404(trek_id)
    
    try:
        db.session.delete(trek)
        db.session.commit()
        flash(f'Trek "{trek.title}" was successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        # If the trek is tied to existing bookings, the database might block deletion
        flash('Cannot delete this trek. It may have existing bookings tied to it.', 'danger')

    # Redirect back to the admin dashboard, specifically on the 'treks' tab
    return redirect(url_for('admin_dashboard', tab='treks'))


# --- GENERAL USER & STAFF PORTALS (PLACEHOLDERS) ---

# 1. Ensure you are importing the handler from your routes folder at the top of app.py
from routes.user import user_dashboard_handler

# 2. Make sure the route function looks exactly like this:
@app.route('/user/dashboard', methods=['GET'])
@login_required
def user_dashboard():
    # Call the code inside user.py that returns the diagnostic variables
    return user_dashboard_handler()

@app.route('/user/book/<int:trek_id>', methods=['POST'])
@login_required
def book_trek(trek_id):
    return book_trek_action_handler(trek_id)

@app.route('/staff/update-profile', methods=['POST'])
@login_required
def staff_update_profile():
    return staff_update_profile_logic()

@app.route('/staff/dashboard',methods = ['GET'])
@login_required
def staff_dashboard():
    # Placeholder layout until staff panel milestone
    return staff_dashboard_logic()

@app.route('/staff/update-trek/<int:trek_id>',methods=['POST'])
@login_required
def staff_update_trek(trek_id):
    return staff_update_trek_logic(trek_id)

@app.route('/admin/trek/assign_staff', methods=['POST'])
def admin_assign_staff():
    return assign_staff_to_trek_handler()

#PAYMENT ROUTE
@app.route('/trek/book/<int:trek_id>', methods=['POST'])
@login_required
def payment_function(trek_id):
    return initiate_booking(trek_id)

@app.route('/trek/checkout', methods=['GET', 'POST'])
@login_required
def payment_checkout_function():
    return payment_checkout()



if __name__ == '__main__':
    app.run(debug=True)