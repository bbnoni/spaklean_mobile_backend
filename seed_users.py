from werkzeug.security import generate_password_hash
from app import app, db
from models.user import User

with app.app_context():
    # Check if admin already exists
    if not User.query.filter_by(email="admin@spaklean.com").first():
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@spaklean.com",
            password_hash=generate_password_hash("admin123"),
            role="Admin"
        )
        db.session.add(admin)
        print("✅ Admin user created")

    if not User.query.filter_by(email="custodian@spaklean.com").first():
        custodian = User(
            first_name="John",
            last_name="Custodian",
            email="custodian@spaklean.com",
            password_hash=generate_password_hash("custodian123"),
            role="Custodian"
        )
        db.session.add(custodian)
        print("✅ Custodian user created")

    db.session.commit()
    print("🎉 Dummy users inserted successfully!")
