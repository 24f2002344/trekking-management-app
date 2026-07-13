from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import db, Trek, Booking

def initiate_booking(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    
    # 1. Grab number of participants traveling
    try:
        slots_requested = int(request.form.get('slots_requested', 1))
    except ValueError:
        slots_requested = 1

    # 2. Safety check: Ensure the route has enough seats open
    if slots_requested > trek.available_slots:
        flash(f"Only {trek.available_slots} slots are available for this expedition.", "danger")
        return redirect(url_for('user_dashboard'))

    # 3. Store quantities in temporary session state memory
    session['booking_intent'] = {
        'trek_id': trek.id,
        'slots': slots_requested,
        'total_price': float(trek.price * slots_requested)
    }
    
    return redirect(url_for('payment_checkout_function'))


def payment_checkout():
    # 1. Verify checkout state exists
    intent = session.get('booking_intent')
    if not intent:
        flash("No active checkout session found.", "warning")
        return redirect(url_for('user_dashboard'))
        
    trek = Trek.query.get(intent['trek_id'])
    
    if request.method == 'POST':
        # 2. Process payment details (Mock validation)
        payment_method = request.form.get('payment_method')
        card_name = request.form.get('card_name')
        
        # 3. Save successful ledger to Database
        new_booking = Booking(
            user_id=current_user.id,
            trek_id=trek.id,
            status='confirmed' # Instantly confirm upon mock pay gateway success
        )
        
        # 4. Deduct the reserved seating rows from the master registry
        trek.available_slots -= intent['slots']
        
        db.session.add(new_booking)
        db.session.commit()
        
        # 5. Flush temporary checkout intent state memory clean
        session.pop('booking_intent', None)
        
        flash(f"Payment successful! Journey to {trek.name} confirmed.", "success")
        return redirect(url_for('user_dashboard'))
        
    return render_template('payment_checkout.html', intent=intent, trek=trek)