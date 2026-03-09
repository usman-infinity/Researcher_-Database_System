import os
from flask import Blueprint, request, render_template, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Paper, Department
from app.extensions import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Paper
from flask import request
from rapidfuzz import fuzz
from flask_login import login_required
from app.models import Paper


papers_bp = Blueprint("papers", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@papers_bp.route("/upload", methods=["GET", "POST"])
def upload_paper():
    if request.method == "POST":
        title = request.form.get("title")
        authors = request.form.get("authors")
        year = request.form.get("year")
        department_name = request.form.get("department")
        pdf_file = request.files.get("pdf_file")

        if not (title and authors and year and department_name):
            return "All fields are required", 400

        # Check file
        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            upload_folder = os.path.join(current_app.root_path, "..", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            pdf_path = os.path.join(upload_folder, filename)
            pdf_file.save(pdf_path)
        else:
            pdf_path = None

        # Department
        dept = Department.query.filter_by(name=department_name).first()
        if not dept:
            dept = Department(name=department_name)
            db.session.add(dept)
            db.session.commit()

        # Paper record
        paper = Paper(
            title=title,
            authors=authors,
            year=int(year),
            department=dept,
            pdf_path=pdf_path
        )

        db.session.add(paper)
        db.session.commit()

        return "Paper Uploaded Successfully"

    # GET → show form
    return render_template("upload_paper.html")

# List uploaded papers
@papers_bp.route("/list")
def list_papers():
    papers = Paper.query.all()
    return render_template("list_papers.html", papers=papers)

# Download PDF
@papers_bp.route("/download/<int:paper_id>")
def download_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    if paper.pdf_path:
        directory = os.path.dirname(paper.pdf_path)
        filename = os.path.basename(paper.pdf_path)
        return send_from_directory(directory, filename, as_attachment=True)
    return "No PDF available", 404

@papers_bp.route("/verify/<int:paper_id>", methods=["POST"])
@login_required
def verify_paper(paper_id):
    # Only admin can verify
    if current_user.role != "admin":
        flash("You are not authorized to verify papers.", "danger")
        return redirect(url_for("papers.list_papers"))

    paper = Paper.query.get_or_404(paper_id)
    paper.verified = True
    db.session.commit()
    flash(f"Paper '{paper.title}' has been verified!", "success")
    return redirect(url_for("papers.list_papers"))



@papers_bp.route("/search", methods=["GET", "POST"])
@login_required
def search_papers():

    papers = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query")

        all_papers = Paper.query.filter_by(verified=True).all()

        for paper in all_papers:

            title_score = fuzz.partial_ratio(query.lower(), paper.title.lower())
            author_score = fuzz.partial_ratio(query.lower(), (paper.authors or "").lower())

            if title_score > 60 or author_score > 60:
                papers.append(paper)

    return render_template("search_results.html", papers=papers, query=query)