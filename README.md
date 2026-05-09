# 🧠 Research Database System

![Project Banner](banner.png)

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-orange)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)]()

---

## 🚀 Project Overview

**Research Database System** is a comprehensive AI-powered platform for managing, uploading, searching, and analyzing research papers. Built with Flask and modern AI technologies, it provides researchers with intelligent tools to discover, analyze, and manage academic literature.

The system features a secure admin approval workflow, AI-powered paper analysis, intelligent recommendations, and a user-friendly interface for seamless research management.

---

## 📂 Project Status

| Phase | Feature | Status |
|------|--------|--------|
| Phase 1 | Project Setup & Environment | ✅ **Completed** |
| Phase 2 | Database Models & Migrations | ✅ **Completed** |
| Phase 3 | Authentication & User Management | ✅ **Completed** |
| Phase 4 | Paper Upload & File Management | ✅ **Completed** |
| Phase 5 | Admin Approval Dashboard | ✅ **Completed** |
| Phase 6 | Intelligent Paper Search | ✅ **Completed** |
| Phase 7 | AI Recommendation System | ✅ **Completed** |
| Phase 8 | AI Paper Summarization | ✅ **Completed** |
| Phase 9 | AI Paper Insights & Keywords | ✅ **Completed** |
| Phase 10 | Security & Role Management | ✅ **Completed** |
| Phase 11 | UI/UX Polish & Testing | ✅ **Completed** |

**🎉 All Features Fully Implemented and Tested!**

---

## 🔍 Key Features

### 👤 User Management
- **Secure Authentication**: Flask-Login based user system
- **Admin Approval**: New accounts require administrator approval
- **Role-Based Access**: Admin and regular user roles
- **Profile Dashboard**: User statistics and quick actions

### 📄 Paper Management
- **Smart Upload**: Upload research papers with abstracts and PDF files
- **Admin Verification**: Comprehensive approval workflow
- **File Management**: Secure PDF storage and download
- **Department Organization**: Papers organized by academic departments

### 🔎 Intelligent Search
- **Fuzzy Search**: RapidFuzz-powered search by title and author
- **Real-time Results**: Fast research paper discovery
- **Verified Papers Only**: Search through approved publications

### 🤖 AI-Powered Analysis

#### AI Paper Summarization
- **Automatic Summaries**: Generate concise paper summaries using advanced NLP
- **Transformer Models**: Powered by Hugging Face Transformers
- **Abstract Analysis**: Intelligent summarization of research abstracts

#### AI Paper Insights
- **Keyword Extraction**: TF-IDF based keyword extraction from abstracts
- **Content Analysis**: Identify main topics and themes
- **Smart Metadata**: Extract key information for better paper understanding

#### AI Recommendations
- **Content-Based Similarity**: TF-IDF + Cosine Similarity algorithm
- **Related Research**: Discover papers with similar topics and themes
- **Intelligent Suggestions**: Personalized paper recommendations

### 🛡️ Security Features
- **Admin-Only Promotions**: Only administrators can create new admins
- **Approval Workflow**: All new accounts and papers require verification
- **Secure File Upload**: Safe PDF handling and storage
- **Role-Based Permissions**: Granular access control throughout the system

---

## 🛠 Technology Stack

### Backend Framework
- **Python 3.10+**: Core programming language
- **Flask 3.1.3**: Web framework with modern features
- **Flask-SQLAlchemy 3.1.1**: Database ORM and management
- **Flask-Login 0.6.3**: User authentication and session management
- **Flask-Migrate 4.0.7**: Database migrations and schema management

### AI & Machine Learning
- **Transformers 4.48.0**: Hugging Face NLP models for summarization
- **Scikit-learn 1.6.1**: Machine learning algorithms for recommendations
- **RapidFuzz 3.12.1**: Fuzzy string matching for search
- **Torch 2.6.0**: PyTorch for deep learning models
- **NumPy 2.2.6 & SciPy 1.15.3**: Scientific computing libraries

### Database & Storage
- **SQLite**: Local database for development and production
- **Alembic 1.13.4**: Database migration tool
- **File System**: Secure PDF storage in uploads directory

### Frontend & UI
- **HTML5 & CSS3**: Semantic markup and styling
- **Bootstrap 5**: Responsive design framework
- **Jinja2 3.1.6**: Template engine for dynamic content
- **Font Awesome**: Icons and visual elements

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/usman-infinity/Researcher_-Database_System.git
cd Researcher_-Database_System/research_system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv research_env
research_env\Scripts\activate

# Linux/Mac
python -m venv research_env
source research_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
# Create database tables
python create_admin.py
```

### 5. Run the Application
```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000/`

### 6. Access Admin Account
- **Email**: admin@university.com
- **Password**: admin123
- **Role**: Administrator (can approve users and papers)

---

## 📖 Usage Guide

### For Regular Users
1. **Register**: Create an account (requires admin approval)
2. **Login**: Access your dashboard after approval
3. **Upload Papers**: Submit research papers for admin review
4. **Explore**: Search, view summaries, insights, and recommendations
5. **Download**: Access approved PDF files

### For Administrators
1. **User Management**: Approve/reject user registrations
2. **Paper Management**: Review and verify submitted papers
3. **Department Management**: Create and manage academic departments
4. **System Monitoring**: View statistics and manage the platform

### AI Features Usage
- **Search**: Use the search page to find papers by title or author
- **Summary**: Click "View Summary" to generate AI-powered paper summaries
- **Insights**: Click "View Insights" to extract keywords and analyze content
- **Recommendations**: Click "View Recommendations" to find similar papers

---

## 🏗 Project Structure

```
research_system/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── extensions.py        # Flask extensions initialization
│   ├── models.py           # Database models (User, Paper, Department)
│   └── routes/
│       ├── __init__.py
│       ├── auth.py         # Authentication routes
│       ├── admin.py        # Admin management routes
│       └── papers.py       # Paper management routes
├── src/
│   ├── __init__.py
│   ├── recommender/
│   │   ├── __init__.py
│   │   └── recommend.py    # AI recommendation engine
│   └── summarizer/
│       ├── __init__.py
│       └── summarize.py    # AI summarization and insights
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS, JS, images
├── migrations/             # Database migrations
├── uploads/                # PDF file storage
├── config.py              # Application configuration
├── run.py                 # Application entry point
├── create_admin.py        # Admin account creation script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔧 Configuration

The application uses environment-based configuration:

- **Development**: SQLite database, debug mode enabled
- **Production**: Configurable database URL, debug disabled
- **Security**: Secure session keys and file upload restrictions

Key configuration options in `config.py`:
- Database URI
- Secret keys
- Upload folder paths
- AI model settings

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Flask Community**: For the excellent web framework
- **Hugging Face**: For transformer models and NLP tools
- **Scikit-learn**: For machine learning algorithms
- **Bootstrap**: For responsive UI components

---

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the maintainers
- Check the documentation for detailed guides

---

**Built with ❤️ for the research community**

*Powered by Usmania's infinity*