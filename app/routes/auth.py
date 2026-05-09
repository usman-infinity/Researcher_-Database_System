from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, login_manager
from ..models import User, Department, Paper, LoginAttempt, AuditLog
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


# ----------------------
# Security Helper Functions
# ----------------------
def is_account_locked(email):
    """Check if account is locked due to too many failed login attempts"""
    # Check last 15 minutes for failed attempts
    fifteen_minutes_ago = datetime.utcnow() - timedelta(minutes=15)
    recent_attempts = LoginAttempt.query.filter_by(
        email=email,
        successful=False,
        timestamp=fifteen_minutes_ago
    ).count()

    return recent_attempts >= 5  # Lock after 5 failed attempts


def log_login_attempt(email, successful, ip_address=None, user_agent=None):
    """Log a login attempt"""
    attempt = LoginAttempt(
        email=email,
        successful=successful,
        ip_address=ip_address or request.remote_addr,
        user_agent=user_agent or request.headers.get('User-Agent')
    )
    db.session.add(attempt)
    db.session.commit()


def log_admin_action(user_id, action, target_type, target_id, details=None):
    """Log admin actions for audit trail"""
    if current_user.is_authenticated and current_user.role == 'admin':
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()


# ----------------------
# Login
# ----------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if account is locked
        if is_account_locked(email):
            flash("Account temporarily locked due to too many failed login attempts. Try again in 15 minutes.", "danger")
            log_login_attempt(email, False)
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials", "danger")
            log_login_attempt(email, False)
            return redirect(url_for('auth.login'))

        if not user.approved and user.role != 'admin':
            flash("Your account is pending admin approval.", "warning")
            log_login_attempt(email, False)
            return redirect(url_for('auth.login'))

        # Successful login
        login_user(user)
        log_login_attempt(email, True)
        flash(f"Welcome {user.name}", "success")
        return redirect(url_for('auth.dashboard'))

    return render_template('auth/login.html')


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
            department_id=department_id,
            approved=False
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Your account will be approved by an admin before login.", "success")
        return redirect(url_for('auth.login'))

    departments = Department.query.all()
    return render_template('auth/register.html', departments=departments)


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
    # Calculate statistics for the user
    total_papers = Paper.query.count()
    user_papers = Paper.query.filter_by(user_id=current_user.id).count()
    pending_papers = Paper.query.filter_by(user_id=current_user.id, verified=False).count()
    verified_papers = Paper.query.filter_by(user_id=current_user.id, verified=True).count()
    
    return render_template('auth/dashboard.html', 
                         user=current_user,
                         total_papers=total_papers,
                         user_papers=user_papers,
                         pending_papers=pending_papers,
                         verified_papers=verified_papers)


# ----------------------
# Login Manager
# ----------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))