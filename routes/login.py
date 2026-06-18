from flask import render_template, request, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash
from models import User


def login_route_handler():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return redirect(url_for('register'))
        if check_password_hash(user.password,password):
            login_user(user)

            if user.role=='admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
    return render_template('login.html')