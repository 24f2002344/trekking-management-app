from flask import render_template, redirect, request, url_for
from models import db, User, Trek
from datetime import datetime

def admin_dashboard_handler():
     stats = {
          'total_users': User.query.filter_by(role='trekker').count(),
          'total_staff': User.query.filter_by(role='staff').count(),
          'total_treks': Trek.query.count(),
          'total_bookings': 0
     }
     
     search_query = request.args.get('search', '').strip()

     treks = Trek.query.all()

     if search_query:
          if search_query.isdigit():
               users = User.query.filter_by(id=int(search_query)).all()
          else:
               users = User.query.filter(User.full_name.contains(search_query)).all()
     else:
          users = User.query.all()
     
     return render_template('admin_dashboard.html', stats=stats, users=users, treks=treks)


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