from flask import render_template, redirect, request, url_for, flash
from models import db, User, Trek, Booking
from datetime import datetime

def admin_dashboard_handler():
     stats = {
          'total_users': User.query.filter_by(role='trekker').count(),
          'total_staff': User.query.filter_by(role='staff').count(),
          'total_treks': Trek.query.count(),
          'total_bookings': Booking.query.count()
     }
     
     search_query = request.args.get('search', '').strip()
     active_tab = request.args.get('tab','users')

     #FOR USER TAB
     if search_query and active_tab=='users':
          if search_query.isdigit():
               users = User.query.filter_by(id=int(search_query), role = 'trekker').all()
          else:
               users = User.query.filter(User.full_name.contains(search_query), User.role == 'trekker').all()
     else:
          users = User.query.filter_by(role = 'trekker').all()
     
     #FOR TREK TAB
     if search_query and active_tab=='treks':
          if search_query.isdigit():
               treks = Trek.query.filter_by(id=int(search_query)).all()
          else:
               treks = Trek.query.filter((Trek.name.contains(search_query)).all() | Trek.location.contains(search_query)).all()
     else:
          treks = Trek.query.all()
     
     #FOR STAFF TAB
     if search_query and active_tab=='staff':
          if search_query.isdigit():
               staff_members = User.query.filter_by(id=int(search_query), role='staff').all()
          else:
               staff_members = User.query.filter(User.full_name.contains(search_query), User.role=='staff').all()
     else:
          staff_members = User.query.filter_by(role='staff').all()

     #FOR BOOKINGS TAB
     if search_query and active_tab=='bookings':
          if search_query.isdigit():
               bookings = Booking.query.filter_by(id=int(search_query)).all()
          else:
               bookings = Booking.query.join(Trek).join(User, Booking.user_id==User.id).filter(
                    (Trek.name.contains(search_query)) |
                    (User.full_name.contains(search_query))
               ).all()
     else:
          bookings = Booking.query.all()
     
     return render_template('admin_dashboard.html',
                            stats=stats,
                            users=users,
                            treks=treks,
                            staff_members=staff_members,
                            bookings=bookings,
                            active_tab=active_tab)


def toggle_user_status_handler(user_id):
     user = User.query.get_or_404(user_id)

     if user.status == 'active':
          user.status = 'deactivated'
     else:
          user.status = 'active'
     db.session.commit()
     return redirect(url_for('admin_dashboard'))


def approve_staff_handler(user_id):
     staff_member = User.query.get_or_404(user_id)
     if staff_member.role == 'staff':
          staff_member.is_approved = True
          db.session.commit()
     return redirect(url_for('admin_dashboard'))

def add_trek_handler():
     name = request.form.get('name')
     location = request.form.get('location')
     difficulty = request.form.get('difficulty')
     duration = request.form.get('duration')
     price = request.form.get('price')
     total_slots = request.form.get('total_slots')
     description = request.form.get('description')
     start_date_raw = request.form.get('start_date')
     end_date_raw = request.form.get('end_date')
     parsed_start_date = datetime.strptime(start_date_raw, '%Y-%m-%d').date()
     parsed_end_date = datetime.strptime(end_date_raw, '%Y-%m-%d').date()

     new_trek = Trek(
          name=name,
          location=location,
          difficulty=difficulty,
          duration=duration,
          price=float(price) if price else 0.0,
          total_slots=int(total_slots) if total_slots else 0,
          available_slots=int(total_slots) if total_slots else 0,
          start_date=parsed_start_date,
          end_date=parsed_end_date,
          description=description

     )

     db.session.add(new_trek)
     db.session.commit()
     return redirect(url_for('admin_dashboard'))

def assign_staff_to_trek_handler():
     trek_id = request.form.get('trek_id')
     staff_id = request.form.get('staff_id')
     
     if not trek_id or not staff_id:
          print("DEBUG: Missing form values, skipping assignment!")
          return redirect(url_for('admin_dashboard'))

     trek = Trek.query.get_or_404(int(trek_id))
     trek.assigned_staff_id = int(staff_id)
          
     db.session.add(trek)
     db.session.commit()
     
     return redirect(url_for('admin_dashboard'))


def delete_trek_handler(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    
    try:
        # 1. Delete all bookings associated with this trek first to avoid DB constraint crashes
        Booking.query.filter_by(trek_id=trek.id).delete()
        
        # 2. Delete the trek itself
        db.session.delete(trek)
        db.session.commit()
        
        flash(f"Expedition '{trek.name}' has been successfully removed from the system.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while trying to delete the trek.", "danger")
        
    # Redirect back to the treks tab
    return redirect(url_for('admin_dashboard', tab='treks'))