from flask import render_template, request, redirect, url_for,flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from models import User

def login_route_handler():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Account not found. Please register.", "warning")
            return redirect(url_for('register'))
            
        if check_password_hash(user.password, password):
            
            #Check if the admin deactivated the account
            if user.status == 'deactivated':
                flash("Your account has been deactivated by an Administrator. Contact support for assistance.", "danger")
                return redirect(url_for('login'))
            
            # Check if staff is approved by admin
            if user.role == "staff" and not user.is_approved:
                flash("Access denied: Your staff account is awaiting Admin approval.", "warning")
                return redirect(url_for('login'))
                
            # If all checks pass, log them in!
            login_user(user)

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid password. Please try again.", "danger")
            
    return render_template('login.html')