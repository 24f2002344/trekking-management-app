from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, Trek, Booking

def staff_dashboard_logic():
    if current_user.role != 'staff':
        flash("Access denied. Staff credential required.", "danger")
        return redirect(url_for('login'))
    
    if not current_user.is_approved:
        from flask_login import logout_user
        logout_user()
        flash("Your account has been terminated by admin.", "danger")
        return redirect(url_for('login'))
    
    # Securely fetch ONLY treks assigned to this specific staff member
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()

    open_treks_count = sum(1 for t in assigned_treks if t.available_slots > 0)
    total_participants_counts = sum(len(trek.bookings) for trek in assigned_treks)

    return render_template(
        'staff_dashboard.html',
        assigned_treks=assigned_treks,
        open_treks_count=open_treks_count,
        total_participants_counts=total_participants_counts
    )

def staff_update_trek_logic(trek_id):
    if current_user.role != 'staff':
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()

    try:
        # Update slots
        trek.available_slots = int(request.form.get('available_slots', trek.available_slots))
        
        # Update Trek Status (Upcoming / Ongoing / Completed)
        new_status = request.form.get('trek_status')
        if new_status:
            trek.status = new_status

        db.session.commit()
        flash(f"Successfully updated parameters for {trek.name}!", "success")

    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating the trek parameters.", "danger")
        
    return redirect(url_for('staff_dashboard'))

def staff_update_profile_logic():
    if current_user.role != 'staff':
        return redirect(url_for('login'))
        
    new_password = request.form.get('password', '').strip()
    if new_password:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Security credentials updated successfully!", "success")
    else:
        flash("No changes were made to your profile.", "info")
        
    return redirect(url_for('staff_dashboard'))