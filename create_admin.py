from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin_email = "usmaniainfinity@gmail.com"
    existing_admin = User.query.filter_by(email=admin_email).first()
    
    if existing_admin:
        print("Admin already exists.")
    else:
        admin = User(
            name="Usmaan",
            email=admin_email,
            password=generate_password_hash("@1402"),
            role="admin",
            approved=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")