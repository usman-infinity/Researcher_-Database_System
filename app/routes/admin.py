from flask import Blueprint, render_template, redirect, url_for
from app.models import Paper
from app.extensions import db
from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# -----------------------
# Admin Dashboard
# -----------------------
@admin_bp.route("/papers")
def view_papers():
    papers = Paper.query.all()
    return render_template("admin_papers.html", papers=papers)


# -----------------------
# Approve Paper
# -----------------------
@admin_bp.route("/approve/<int:paper_id>")
def approve_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    paper.verified = True
    db.session.commit()
    return redirect(url_for("admin.view_papers"))


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)