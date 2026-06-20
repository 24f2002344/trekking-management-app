from flask import Flask, render_template, request, redirect, url_for 
from flask_login import LoginManager 
from models import db, User
from routes.login import login_route_handler
from routes.registeration import registraiton_route_handler

app = Flask(__name__)

# Basic database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key_for_my_project'

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader Callback (Tells Flask-Login how to look up a user tracking ID)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# --- ROUTES ---

# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_route_handler()

# REGISTRATION ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():
    return registraiton_route_handler()

# ROOT PATH REDIRECT
@app.route('/')
def home():
    return redirect(url_for('login'))

# ROLE PROTECTION DEMO PAGES
@app.route('/admin/dashboard')
def admin_dashboard():
    return "admin dashboard."

@app.route('/user/dashboard')
def user_dashboard():
    return "user dashboard."

@app.route('/staff/dashboard')
def staff_dashboard():
    return "welcome, dear staff member"

if __name__ == '__main__':
    app.run(debug=True)