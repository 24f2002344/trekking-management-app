from flask_sqlalchemy import SQLAlchemy
from flask_login import userMixin
from datetime import datetime

db = SQLAlchemy()

class User(userMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable = False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)
    full_name = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(15),nullable=False)
    role = db.Column(db.String(20),nullable = False,default='user')
    status = db.Column(db.String(20),nullable= False, default='active')
    is_approved = db.Column(db.boolean,dafault = False)