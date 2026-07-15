from app import app  # Import your Flask app instance to establish database context
from models import db, User, Trek, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_database():
    with app.app_context():
        print("Initializing database refresh...")
        
        # 1. Clear out old tables safely
        db.drop_all()
        db.create_all()
        
        print("Hydrating Admin Account...")
        # THE ADMIN (Password remains admin123)
        admin_user = User(
            username="admin_trek",
            email="admin@trekkings.com",
            password=generate_password_hash("admin123"),
            full_name="Arjun Sharma",
            phone="9876543210",
            role="admin",
            status="active",
            is_approved=True
        )
        db.session.add(admin_user)

        print("Hydrating 10 Certified Staff Guide Records...")
        #10 STAFF MEMBERS / GUIDES (Password set to 0000)
        staff_data = [
            ("guide_amit", "amit.negi@trekkings.com", "Amit Negi", "9876543211"),
            ("guide_priya", "priya.rawat@trekkings.com", "Priya Rawat", "9876543212"),
            ("guide_vikram", "vikram.bisht@trekkings.com", "Vikram Bisht", "9876543213"),
            ("guide_sneha", "sneha.thapa@trekkings.com", "Sneha Thapa", "9876543214"),
            ("guide_rajesh", "rajesh.kumar@trekkings.com", "Rajesh Kumar", "9876543215"),
            ("guide_anjali", "anjali.sharma@trekkings.com", "Anjali Sharma", "9876543216"),
            ("guide_rohit", "rohit.singh@trekkings.com", "Rohit Singh", "9876543217"),
            ("guide_kiran", "kiran.joshi@trekkings.com", "Kiran Joshi", "9876543218"),
            ("guide_manish", "manish.yadav@trekkings.com", "Manish Yadav", "9876543219"),
            ("guide_deepa", "deepa.shah@trekkings.com", "Deepa Shah", "9876543220")
        ]
        
        guides = []
        for username, email, name, phone in staff_data:
            g = User(
                username=username,
                email=email,
                password=generate_password_hash("0000"),  # 🔒 Set to 0000
                full_name=name,
                phone=phone,
                role="staff",
                status="active",
                is_approved=True
            )
            guides.append(g)
            db.session.add(g)
        
        # Commit guides first so they have assigned database IDs for foreign key reference
        db.session.commit()

        print("Hydrating 10 Customer Trekker Records...")
        #10 REGISTERED TREKKERS (Password set to 0000)
        trekker_data = [
            ("trekker_rahul", "rahul@gmail.com", "Rahul Verma", "9811122233"),
            ("trekker_ria", "ria@gmail.com", "Ria Kapoor", "9811122234"),
            ("trekker_aman", "aman@gmail.com", "Aman Malhotra", "9811122235"),
            ("trekker_divya", "divya@gmail.com", "Divya Joshi", "9811122236"),
            ("trekker_gaurav", "gaurav@gmail.com", "Gaurav Sen", "9811122237"),
            ("trekker_pooja", "pooja@gmail.com", "Pooja Hegde", "9811122238"),
            ("trekker_siddharth", "sid@gmail.com", "Siddharth Malhotra", "9811122239"),
            ("trekker_kriti", "kriti@gmail.com", "Kriti Sanon", "9811122240"),
            ("trekker_varun", "varun@gmail.com", "Varun Dhawan", "9811122241"),
            ("trekker_alia", "alia@gmail.com", "Alia Bhatt", "9811122242")
        ]
        
        trekkers = []
        for username, email, name, phone in trekker_data:
            t = User(
                username=username,
                email=email,
                password=generate_password_hash("0000"),  # 🔒 Set to 0000
                full_name=name,
                phone=phone,
                role="trekker",
                status="active",
                is_approved=True
            )
            trekkers.append(t)
            db.session.add(t)

        print("Hydrating 10 Real-World Trek Destinations...")
        # 10 DETAILED TREK DESTINATIONS
        trek_data = [
            ("Kedarkantha Peak Expedition", "Uttarakhand", "Moderate", "5 Days / 4 Nights", 20, 8500.0, guides[0].id, 15,
             "Famous for its winter snowscape slopes and spectacular 360-degree views from the summit range."),
            ("Valley of Flowers Trail", "Uttarakhand", "Easy", "6 Days / 5 Nights", 15, 9200.0, None, 30,
             "A beautiful UNESCO World Heritage site carpeted with wild alpine meadow flowers."),
            ("Hampta Pass Crossing", "Himachal Pradesh", "Hard", "5 Days / 4 Nights", 12, 11000.0, guides[1].id, 45,
             "An incredible contrast transition route shifting from lush green valley slopes into cold high-altitude desert mountains."),
            ("Roopkund Lake Trek", "Uttarakhand", "Hard", "8 Days / 7 Nights", 10, 14500.0, guides[2].id, 25,
             "A thrilling high-altitude trek leading to the mysterious, glacial Skeleton Lake surrounded by alpine meadows."),
            ("Kushalnagar Tadiandamol Trek", "Karnataka", "Easy", "2 Days / 1 Night", 30, 3500.0, guides[3].id, 5,
             "The highest peak in Coorg offering stunning views of lush green Western Ghats shola forests wrapped in morning mist."),
            ("Triund Ridge Trek", "Himachal Pradesh", "Easy", "2 Days / 1 Night", 40, 2200.0, None, 8,
             "A short, highly accessible trek near McLeod Ganj showcasing breathtaking rocky views of the Dhauladhar Range."),
            ("Kanshet Rajmachi Fort Trail", "Maharashtra", "Moderate", "2 Days / 1 Night", 25, 2800.0, guides[4].id, 12,
             "A beautiful historical fort trail cutting directly through waterfalls and dense green vegetation during monsoon seasons."),
            ("Sandakphu Ridge Trek", "West Bengal", "Moderate", "6 Days / 5 Nights", 15, 12500.0, guides[5].id, 18,
             "Known as the trek of the Titans, offering spectacular views of four of the world's highest peaks, including Mt. Everest."),
            ("Brahmatal Winter Trek", "Uttarakhand", "Moderate", "6 Days / 5 Nights", 18, 9000.0, guides[6].id, 22,
             "A rare, spectacular winter trail offering majestic frozen high-altitude lake vistas and sprawling snowfields."),
            ("Goechala Pass Expedition", "Sikkim", "Hard", "10 Days / 9 Nights", 8, 18500.0, guides[7].id, 35,
             "A demanding mountain path offering views of the massive southeast face of Mt. Kanchenjunga.")
        ]
        
        treks = []
        for name, loc, diff, dur, slots, price, staff_id, days_out, desc in trek_data:
            tr = Trek(
                name=name,
                location=loc,
                difficulty=diff,
                duration=dur,
                total_slots=slots,
                available_slots=slots - 2,
                assigned_staff_id=staff_id,
                start_date=datetime.now().date() + timedelta(days=days_out),
                end_date=datetime.now().date() + timedelta(days=days_out + 5),
                description=desc,
                price=price
            )
            treks.append(tr)
            db.session.add(tr)
        
        db.session.commit()

        print("Hydrating Initial Booking History...")
        # INITIAL MATCHED BOOKINGS FOR METRICS
        for i in range(5):
            b = Booking(
                user_id=trekkers[i].id,
                trek_id=treks[i].id,
                status="confirmed"
            )
            db.session.add(b)
            
        db.session.commit()
        print(" Database successfully re-seeded! All staff and trekkers have password '0000'. Admin password remains 'admin123'.")

if __name__ == "__main__":
    seed_database()