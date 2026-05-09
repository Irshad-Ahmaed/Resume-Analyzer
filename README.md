# 📄 Resume Analyzer

An AI-powered web application that evaluates resumes against specific job roles and experience levels to provide actionable insights, learning roadmaps, and interview preparation.

## 🌟 Overview

The **Resume Analyzer** helps job seekers align their profiles with their career goals. By leveraging the power of **Google Gemini AI**, the application parses resumes (supporting PDF, DOCX, and raw text) and compares them against a target role and experience level.

**Key Features:**
- **Skill Extraction:** Automatically identifies relevant skills from your resume.
- **Gap Analysis:** Pinpoints missing skills and qualifications for your target role.
- **Learning Roadmap:** Generates a step-by-step path to bridge the identified gaps.
- **Interview Prep:** Provides tailored interview questions and ideal answers based on your profile.
- **History Tracking:** Save and revisit previous analysis reports in a dedicated history dashboard.

## 🛠️ Things Used

### Backend
- **Framework:** [Flask](https://flask.palletsprojects.com/) (Python)
- **AI Engine:** [Google Gemini API](https://ai.google.dev/) (`google-genai`)
- **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- **Authentication:** Werkzeug (Password Hashing), Flask Sessions
- **File Parsing:** [PyPDF2](https://pypdf2.readthedocs.io/) (PDF), [python-docx](https://python-docx.readthedocs.io/) (Word)

### Frontend
- **Templating:** Jinja2
- **Styling:** Custom CSS (Responsive Design)

---

## 🛤️ Pipeline Diagram

```mermaid
graph TD
    User([User]) -->|Upload Resume + Goal| App[Flask Server]
    App -->|Parse File| Parser{Parser}
    Parser -->|.pdf| PyPDF2[PyPDF2]
    Parser -->|.docx| Docx[python-docx]
    
    PyPDF2 --> Text[Resume Text]
    Docx --> Text
    
    Text --> AI[Gemini API]
    AI -->|JSON Analysis| App
    
    App -->|Save Report| DB[(Database)]
    App -->|Display Results| UI[User Dashboard]
```

---

## ⚙️ Setup Instructions

Follow these steps to get the project running locally:

### 1. Prerequisites
- Python 3.10 or higher
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 2. Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd resume-analyzer
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

Create a `.env` file in the root directory and add your credentials:

```env
SECRET_KEY=your_flask_secret_key
DATABASE_URL=mysql+pymysql://user:password@host/dbname?ssl-mode=REQUIRED
GEMINI_API_KEY=your_google_gemini_api_key
```

> **Note:** The project is currently configured for a MySQL database with SSL. If you wish to use a different database (like SQLite), update the `DATABASE_URL` and `connect_args` in `db.py`.

### 4. Database Initialization
The application uses SQLAlchemy to automatically create the necessary tables (`users`, `reports`) on the first run.

### 5. Run the Application
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

---
