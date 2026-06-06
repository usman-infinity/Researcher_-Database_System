# 🧠 Research Database System

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-orange)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)]()

---

## 🚀 Project Overview

**Research Database System** is a full-stack research management platform built with Flask. It enables users to register, upload papers, search internal and external research content, generate summaries, extract insights, and discover related papers.

The platform supports:
- secure authentication with admin approval,
- research paper upload and verification,
- AI-driven summarization and keyword extraction,
- intelligent recommendations,
- OpenAlex external paper discovery,
- and role-based access control.

---

## ✅ Key Features

### User Authentication & Roles
- Flask-Login based authentication
- Registration with admin approval
- Admin and faculty/user roles
- Secure login and logout flow

### Paper Management
- Upload papers with title, authors, year, abstract, and optional PDF
- Associate papers with user accounts and departments
- Paper verification workflow for admin approval
- Secure file upload and download support

### Search & Discovery
- Internal search across verified papers by title and author
- Fuzzy search using RapidFuzz
- External OpenAlex search integration
- Direct DOI or paper URL open handling
- Automatic author-based external search for signed-in users

### AI-powered Research Tools
- Abstract summarization
- Keyword extraction and insights
- Related paper recommendations
- Summary and recommendations accessible from paper details

### Admin Controls
- View and manage users
- Approve or reject user registrations
- Review and verify uploaded papers
- Promote or demote user roles
- Audit logging for admin actions

---

## 🛠 Technology Stack

- Python 3.10+
- Flask 3.1.3
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- SQLite
- Requests
- RapidFuzz
- Transformers (Hugging Face)
- scikit-learn
- NumPy and SciPy

---

## 📦 Installation

### 1. Clone repository
```bash
git clone https://github.com/usman-infinity/Researcher_-Database_System.git
cd Researcher_-Database_System/research_system
```

### 2. Create and activate virtual environment
```bash
python -m venv research_env
research_env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create admin user and initialize database
```bash
python create_admin.py
```

### 5. Run the app
```bash
python run.py
```

Open the app at `http://127.0.0.1:5000/`

---

## 🚀 Usage

### Regular users
- Register for an account
- Wait for admin approval
- Login and access your dashboard
- Upload papers and submit them for verification
- Search verified papers
- View summaries, insights, and recommendations

### Admin users
- Approve or reject registrations
- Verify uploaded papers
- Manage departments, users, and papers
- Monitor system activity from the admin dashboard

### External search
- Go to the External Search page
- Paste a paper title, DOI, or direct paper URL
- Signed-in users automatically see external papers matching their author name

---

## 🗂 Project Structure

```
research_system/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── routes/
│       ├── auth.py
│       ├── admin.py
│       └── papers.py
├── src/
│   ├── recommender/
│   │   └── recommend.py
│   └── summarizer/
│       └── summarize.py
├── templates/
├── uploads/
├── migrations/
├── config.py
├── create_admin.py
├── run.py
├── requirements.txt
└── README.md
```

---

## 🔧 Configuration

Configuration is defined in `config.py` and includes:
- database connection settings
- secret key and security options
- upload folder settings
- model and external API settings

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Commit your improvements
4. Open a pull request

---

## 📄 License

This project uses the MIT License.
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