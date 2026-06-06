import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

# Flask imports
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import re

# Database models
from app.models import Paper, Department
from app.extensions import db

# AI / utilities
from src.recommender.recommend import recommend_papers
from src.summarizer.summarize import generate_summary, extract_keywords
from src.external.openalex_integration import search_openalex
from rapidfuzz import fuzz

# -------------------------------
# Blueprint
# -------------------------------
papers_bp = Blueprint("papers", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------------
# Routes
# -------------------------------

@papers_bp.route("/summary/<int:paper_id>")
def summary(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    summary = generate_summary(paper.abstract)
    return render_template("summary.html", paper=paper, summary=summary)

@papers_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_paper():
    if request.method == "POST":
        title = request.form.get("title")
        authors = request.form.get("authors")
        year = request.form.get("year")
        department_name = request.form.get("department")
        abstract = request.form.get("abstract")
        pdf_file = request.files.get("pdf_file")

        if not (title and authors and year and department_name and abstract):
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
            abstract=abstract,
            pdf_path=pdf_path,
            user_id=current_user.id
        )

        db.session.add(paper)
        db.session.commit()
        return "Paper Uploaded Successfully"

    return render_template("auth/upload_paper.html")

@papers_bp.route("/list")
def list_papers():
    papers = Paper.query.all()
    return render_template("list_papers.html", papers=papers)

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

@papers_bp.route("/recommend/<int:paper_id>")
def recommend(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    papers = Paper.query.filter_by(verified=True).all()
    recommendations = recommend_papers(papers, paper.title)
    return render_template("recommendations.html", paper=paper, recommendations=recommendations)


@papers_bp.route("/insights/<int:paper_id>")
def insights(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    keywords = extract_keywords(paper.abstract)
    return render_template("insights.html", paper=paper, keywords=keywords)


@papers_bp.route('/external_search', methods=['GET', 'POST'])
def external_search():
    """Search OpenAlex and display results to import."""
    results = []
    query = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            url_pattern = re.compile(r'^(https?://)', re.IGNORECASE)
            doi_pattern = re.compile(r'^(?:doi:\s*|https?://doi\.org/)?(10\.\d{4,9}/.+)$', re.IGNORECASE)
            if url_pattern.match(query.strip()):
                return redirect(query.strip())
            doi_match = doi_pattern.match(query.strip())
            if doi_match:
                doi = doi_match.group(1)
                return redirect(f'https://doi.org/{doi}')
        try:
            results = search_openalex(query, num=10)
        except Exception as e:
            flash(f'External search failed: {e}', 'danger')

    return render_template('external_search.html', results=results, query=query)