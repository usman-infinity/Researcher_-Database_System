from datetime import datetime
from .extensions import db
from flask_login import UserMixin


# ----------------------
# Department Model
# ----------------------
class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    users = db.relationship("User", backref="department", lazy=True)
    papers = db.relationship("Paper", backref="department", lazy=True)


# ----------------------
# User Model
# ----------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="faculty")  # faculty / admin

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    papers = db.relationship("Paper", backref="author", lazy=True)

    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ----------------------
# Paper Model
# ----------------------
class Paper(db.Model):
    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(500))
    authors = db.Column(db.Text)
    year = db.Column(db.Integer)
    abstract = db.Column(db.Text)

    pdf_path = db.Column(db.String(500))
    link = db.Column(db.String(500))

    verified = db.Column(db.Boolean, default=False)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ----------------------
# Audit Log Model (Security)
# ----------------------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # approve_user, reject_user, verify_paper, etc.
    target_type = db.Column(db.String(50), nullable=False)  # user, paper, department
    target_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text)  # Additional details about the action
    ip_address = db.Column(db.String(45))  # IPv4/IPv6 support
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audit_logs")


# ----------------------
# Login Attempt Model (Security)
# ----------------------
class LoginAttempt(db.Model):
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    successful = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for performance
    __table_args__ = (
        db.Index('idx_login_attempts_email_time', 'email', 'timestamp'),
    )
