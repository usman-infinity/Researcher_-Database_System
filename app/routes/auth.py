from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, login_manager
from ..models import User, Department

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


# ----------------------
# Login
# ----------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials", "danger")
            return redirect(url_for('auth.login'))

        login_user(user)
        flash(f"Welcome {user.name}", "success")
        return redirect(url_for('auth.dashboard'))

    return render_template('login.html')


# ----------------------
# Register
# ----------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        department_id = request.form.get('department_id')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method='sha256')
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            department_id=department_id
        )
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully", "success")
        return redirect(url_for('auth.login'))

    departments = Department.query.all()
    return render_template('register.html', departments=departments)


# ----------------------
# Logout
# ----------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('auth.login'))


# ----------------------
# Dashboard (Example)
# ----------------------
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


# ----------------------
# Login Manager
# ----------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))