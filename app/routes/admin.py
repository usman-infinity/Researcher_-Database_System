from flask import Blueprint, render_template, redirect, url_for
from app.models import Paper, User
from app.extensions import db
from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# -----------------------
# Admin Dashboard
# -----------------------
@admin_bp.route("/papers")
@login_required
def view_papers():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    papers = Paper.query.all()
    return render_template("admin_papers.html", papers=papers)


# -----------------------
# User approvals
# -----------------------
@admin_bp.route("/users")
@login_required
def view_users():
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users)


@admin_bp.route("/users/approve/<int:user_id>")
@login_required
def approve_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("auth.dashboard"))

    user = User.query.get_or_404(user_id)
    user.approved = True
    db.session.commit()
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
    db.session.delete(paper)
    db.session.commit()
    return redirect(url_for("admin.view_papers"))


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)