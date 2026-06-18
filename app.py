from flask import Flask, redirect, url_for
from models import db, User
from routes.login import login_route_handler
from flask import Flask,render_template,request,redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['secret_key']='secret_key_for_my_project'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/login', methods = ['GET','POST'])
def login():
    return login_route_handler()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    return "admin dashboard."

@app.route('/user/dashboard')
def user_dashboard():
    return "user dashboard."

@app.route('/register')
def register():
    return "register here."

if __name__ =='__main__':
    app.run(debug=True)