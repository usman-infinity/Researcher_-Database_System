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