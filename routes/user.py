from flask import render_template, redirect, request, url_for,flash
from flask_login import current_user
from models import db, Trek, Booking
from werkzeug.security import generate_password_hash

from models import Trek, Booking, db

from flask import render_template, request
from flask_login import current_user
from models import db, Trek, Booking

def user_dashboard_handler():
    # 1. Capture and strip arguments quickly
    search = request.args.get('search', '').strip()
    difficulty = request.args.get('difficulty', '').strip()
    
    # 2. Start query and stack filters compactly using implicit truthiness
    query = Trek.query
    if search:
        query = query.filter(Trek.name.contains(search))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
        
    # 3. Fetch data and return in one go
    return render_template(
        'user_dashboard.html', 
        treks=query.all(), 
        bookings=Booking.query.filter_by(user_id=current_user.id).all()
    )

def book_trek_action_handler(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.available_slots>0:
        trek.available_slots -=1;
        new_booking = Booking(
            user_id=current_user.id,
            trek_id=trek.id
        )
        db.session.add(new_booking)
        db.session.commit()
        flash(f"Successfully booked your expedition to {trek.name}!", "success")
    else:
        flash("Sorry, this trek expedition window is completely full!", "danger")
    
    return redirect(url_for('user_dashboard'))

def user_profile_update_handler():
    # 1. Capture text fields from the request form context
    new_username = request.form.get('username', '').strip()
    new_password = request.form.get('password', '').strip()
    
    # 2. Mutate username if an adjustment was supplied
    if new_username:
        current_user.username = new_username
        
    # 3. Securely hash and update the password if provided
    if new_password:
        current_user.password = generate_password_hash(new_password)
        
    # 4. Commit changes to your database session ledger
    db.session.commit()
    
    flash("Profile configurations saved successfully!", "success")
    return redirect(url_for('user_dashboard'))