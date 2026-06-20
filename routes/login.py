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
            if user.role == "staff" and not user.is_approved:
                return "<h3>Access denied: waiting from admin approval</h3>"
            login_user(user)

            if user.role=='admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
    return render_template('login.html')