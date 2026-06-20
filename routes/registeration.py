from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from models import db, User

def registraiton_route_handler():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        is_approved = True if role == 'trekker' else False
        new_user = User(
            full_name=full_name,
            username=username,
            phone=phone,
            email=email,
            password=generate_password_hash(password),
            role=role,
            is_approved=is_approved,
            status='active'
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login')) 

    return render_template('registration.html')