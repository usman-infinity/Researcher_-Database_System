from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from app.models import Paper, User, Department, AuditLog
from app.extensions import db
from flask_login import login_required, current_user
from sqlalchemy import func
from .auth import log_admin_action  # Import the audit logging function

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# -----------------------
# Admin Dashboard
# -----------------------
@admin_bp.route("/")
@login_required
def dashboard():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))
    
    # Statistics
    total_users = User.query.count()
    pending_users = User.query.filter_by(approved=False).count()
    admin_count = User.query.filter_by(role="admin").count()
    total_papers = Paper.query.count()
    pending_papers = Paper.query.filter_by(verified=False).count()
    verified_papers = Paper.query.filter_by(verified=True).count()
    total_departments = Department.query.count()
    
    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_papers = Paper.query.order_by(Paper.created_at.desc()).limit(5).all()
    
    stats = {
        'total_users': total_users,
        'pending_users': pending_users,
        'admin_count': admin_count,
        'total_papers': total_papers,
        'pending_papers': pending_papers,
        'verified_papers': verified_papers,
        'total_departments': total_departments,
    }
    
    return render_template("admin_dashboard.html", stats=stats, recent_users=recent_users, recent_papers=recent_papers)


@admin_bp.route("/papers")
@login_required
def view_papers():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    # Filter and search
    search = request.args.get('search', '')
    filter_status = request.args.get('status', 'all')  # all, pending, verified
    
    query = Paper.query
    
    if search:
        query = query.filter(
            (Paper.title.ilike(f'%{search}%')) |
            (Paper.authors.ilike(f'%{search}%'))
        )
    
    if filter_status == 'pending':
        query = query.filter_by(verified=False)
    elif filter_status == 'verified':
        query = query.filter_by(verified=True)
    
    papers = query.order_by(Paper.created_at.desc()).all()
    return render_template("admin_papers.html", papers=papers, search=search, filter_status=filter_status)


# -----------------------
# User approvals
# -----------------------
@admin_bp.route("/users")
@login_required
def view_users():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    # Filter options
    filter_status = request.args.get('status', 'all')  # all, pending, approved
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    if filter_status == 'pending':
        query = query.filter_by(approved=False)
    elif filter_status == 'approved':
        query = query.filter_by(approved=True)
    
    users = query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users, filter_status=filter_status, search=search)


@admin_bp.route("/departments")
@login_required
def view_departments():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    departments = Department.query.all()
    return render_template("admin_departments.html", departments=departments)


@admin_bp.route("/departments/add", methods=["POST"])
@login_required
def add_department():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    name = request.form.get('name', '').strip()
    
    if not name:
        flash("Department name is required.", "danger")
        return redirect(url_for("admin.view_departments"))
    
    if Department.query.filter_by(name=name).first():
        flash("Department already exists.", "danger")
        return redirect(url_for("admin.view_departments"))
    
    dept = Department(name=name)
    db.session.add(dept)
    db.session.commit()
    flash(f"Department '{name}' created successfully.", "success")
    return redirect(url_for("admin.view_departments"))


@admin_bp.route("/departments/delete/<int:dept_id>", methods=["POST"])
@login_required
def delete_department(dept_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    dept = Department.query.get_or_404(dept_id)
    dept_name = dept.name
    db.session.delete(dept)
    db.session.commit()
    flash(f"Department '{dept_name}' deleted successfully.", "success")
    return redirect(url_for("admin.view_departments"))



@admin_bp.route("/users/approve/<int:user_id>")
@login_required
def approve_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    user = User.query.get_or_404(user_id)

    # Prevent modification of primary admin account
    if user.email == "usmaniainfinity@gmail.com":
        return redirect(url_for("admin.view_users"))

    user.approved = True
    db.session.commit()

    # Log admin action
    log_admin_action(
        current_user.id,
        "approve_user",
        "user",
        user_id,
        f"Approved user: {user.name} ({user.email})"
    )

    flash(f"User '{user.name}' approved successfully.", "success")
    return redirect(url_for("admin.view_users"))


@admin_bp.route("/users/reject/<int:user_id>", methods=["POST"])
@login_required
def reject_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    user = User.query.get_or_404(user_id)

    # Prevent modification of primary admin account
    if user.email == "usmaniainfinity@gmail.com":
        flash("Cannot reject the primary admin account.", "danger")
        return redirect(url_for("admin.view_users"))

    user_name = user.name
    user_email = user.email
    db.session.delete(user)
    db.session.commit()

    # Log admin action
    log_admin_action(
        current_user.id,
        "reject_user",
        "user",
        user_id,
        f"Rejected and deleted user: {user_name} ({user_email})"
    )

    flash(f"User '{user_name}' rejected and removed.", "success")
    return redirect(url_for("admin.view_users"))



@admin_bp.route("/users/promote/<int:user_id>")
@login_required
def promote_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    user = User.query.get_or_404(user_id)
    
    # Prevent modification of primary admin account
    if user.email == "usmaniainfinity@gmail.com":
        return redirect(url_for("admin.view_users"))
    
    user.role = "admin"
    user.approved = True
    db.session.commit()
    flash(f"User '{user.name}' promoted to admin.", "success")
    return redirect(url_for("admin.view_users"))


@admin_bp.route("/users/demote/<int:user_id>", methods=["POST"])
@login_required
def demote_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    user = User.query.get_or_404(user_id)
    
    # Prevent modification of primary admin account
    if user.email == "usmaniainfinity@gmail.com":
        flash("Cannot demote the primary admin account.", "danger")
        return redirect(url_for("admin.view_users"))
    
    user.role = "faculty"
    db.session.commit()
    flash(f"User '{user.name}' demoted to faculty.", "success")
    return redirect(url_for("admin.view_users"))



# -----------------------
# Approve Paper
# -----------------------
@admin_bp.route("/approve/<int:paper_id>")
@login_required
def approve_paper(paper_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    paper = Paper.query.get_or_404(paper_id)
    paper.verified = True
    db.session.commit()

    # Log admin action
    log_admin_action(
        current_user.id,
        "verify_paper",
        "paper",
        paper_id,
        f"Verified paper: {paper.title} by {paper.authors}"
    )

    flash(f"Paper '{paper.title}' verified successfully.", "success")
    return redirect(url_for("admin.view_papers"))


# -----------------------
# Delete Paper
# -----------------------
@admin_bp.route("/delete/<int:paper_id>", methods=["POST"])
@login_required
def delete_paper(paper_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    paper = Paper.query.get_or_404(paper_id)
    paper_title = paper.title
    paper_authors = paper.authors
    db.session.delete(paper)
    db.session.commit()

    # Log admin action
    log_admin_action(
        current_user.id,
        "delete_paper",
        "paper",
        paper_id,
        f"Deleted paper: {paper_title} by {paper_authors}"
    )

    flash(f"Paper '{paper_title}' deleted successfully.", "success")
    return redirect(url_for("admin.view_papers"))


# -----------------------
# Reject Paper (mark as unverified)
# -----------------------
@admin_bp.route("/reject/<int:paper_id>", methods=["POST"])
@login_required
def reject_paper(paper_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    paper = Paper.query.get_or_404(paper_id)
    paper.verified = False
    db.session.commit()
    flash(f"Paper '{paper.title}' marked as unverified.", "success")
    return redirect(url_for("admin.view_papers"))



dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# -----------------------
# View Audit Logs (Security)
# -----------------------
@admin_bp.route("/audit-logs")
@login_required
def view_audit_logs():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    # Get recent audit logs (last 100 entries)
    audit_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()

    return render_template("admin_audit_logs.html", audit_logs=audit_logs)


from flask import render_template, request
from app.models import Paper, Department


@admin_bp.route('/admin/papers')
def manage_papers():
    # Get filter values from the request
    selected_year = request.args.get('year', type=int)
    selected_dept = request.args.get('department', type=int)

    # Start with a base query
    query = Paper.query

    # Apply filters if they exist
    if selected_year:
        query = query.filter(Paper.year == selected_year)
    if selected_dept:
        query = query.filter(Paper.department_id == selected_dept)

    papers = query.all()
    departments = Department.query.all()
    
    # Get unique years for the dropdown
    years = [year[0] for year in Paper.query.with_entities(Paper.year).distinct().all()]

    return render_template('admin/papers.html', 
                           papers=papers, 
                           departments=departments, 
                           years=sorted(years, reverse=True),
                           selected_year=selected_year,
                           selected_dept=selected_dept)