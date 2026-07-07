from flask import render_template,request, redirect, url_for, flash
from flask_login import login_required,current_user
from werkzeug.security import generate_password_hash
from models import db, User, Trek, Booking

def staff_dashboard_logic():
    if current_user.role != 'staff':
        flash("Access denied. Staff credential required.","danger")
        return redirect(url_for('login'))
    
    if not current_user.is_approved:
        from flask_login import logout_user
        logout_user()
        flash("Your account has been terminated by admin.","danger")
        return redirect(url_for('login'))
    
    assigned_treks = Trek.query.filter_by(assigned_staff_id = current_user.id).all()

    open_treks_count = sum(1 for t in assigned_treks if t.available_slots>0)

    total_participants_counts = 0
    for trek in assigned_treks:
        total_participants_counts +=len(trek.bookings)

    return render_template(
        'staff_dashboard.html',
        assigned_treks=assigned_treks,
        open_treks_count=open_treks_count,
        total_participants_counts=total_participants_counts
    )

def staff_update_trek_logic(trek_id):
    if current_user.role != 'staff':
        flash("access denied.","danger")
        return redirect(url_for('login'))
    
    trek = Trek.query.filter_by(id = trek_id, staff_id =current_user.id).first_or_404()

    try:
        trek.available_slots = int(request.form.get('available_slots', trek.available_slots))
        db.session.commit()
        flash(f"Successfully updated available slots for {trek.name}!","success")

    except Exception as e:
        db.session.rollback()
        flash("An error occurred while upadating the trek parameters.","danger")
    return redirect(url_for('staff_dashboard.html'))