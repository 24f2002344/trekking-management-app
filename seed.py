from app import app,db 
from models import User
from werkzeug.security import generate_password_hash
with app.app_context():
    admin = User(username = "admin",email = "admin@trekkings.com",password = generate_password_hash("admin123"),role = "admin",full_name = "System Administrator",phone = "0123456789",status = "active",is_approved=True)
    db.session.add(admin)
    db.session.commit()
    print("admin added")