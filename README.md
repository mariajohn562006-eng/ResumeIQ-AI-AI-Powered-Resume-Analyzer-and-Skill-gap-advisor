# AI Resume Studio

A full-stack resume builder and analyzer. Create a structured resume, calculate a transparent heuristic completeness score, compare resume keywords against a target job description, upload an existing resume, and export a PDF.

## Features
- Resume builder for contact details, summary, skills, experience, projects, education, and certifications.
- Resume completeness scoring with a checklist and suggestions.
- Job-description keyword overlap, matched terms, and missing terms.
- Upload and extract text from PDF, DOCX, and TXT files (max 8 MB).
- PDF export, copy-to-clipboard, responsive interface, and API health check.
- No external AI API key required; analysis runs locally using transparent rules.

> The score is a heuristic guide, not a real ATS vendor score or a hiring prediction. Only add skills and experience that are accurate.

## Tech stack
- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Python and Flask
- Parsing: pypdf and python-docx
- PDF generation: ReportLab

## Run locally
Python 3.10+ is recommended.

### 1. Create a virtual environment
**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install packages
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```
Open http://127.0.0.1:5000.

## Project structure
```text
ai_resume_studio/
├── app.py
├── resume_engine.py
├── requirements.txt
├── README.md
├── .gitignore
├── uploads/.gitkeep
├── templates/index.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/health` | Service health check |
| POST | `/api/generate` | Generate resume text from form fields |
| POST | `/api/analyze` | Score resume and compare keywords |
| POST | `/api/upload` | Extract text from PDF, DOCX, or TXT |
| POST | `/api/export/pdf` | Download a resume PDF |

## Example analysis request
```json
{
  "resume_text": "Alex Doe\nEmail: alex@example.com\nSUMMARY\nComputer science student ...",
  "job_description": "Python, SQL, machine learning, data analysis ..."
}
```

## Privacy and deployment
- Uploaded files are processed in memory and are not stored by the upload endpoint.
- The project is designed for local development. Before public deployment, set a strong `SECRET_KEY`, use HTTPS and a production WSGI server, add rate limiting, and review file-parsing and privacy requirements.
- Resume data is not sent to an external AI provider by this version.

## Future improvements
Optional LLM-powered rewriting, DOCX export, user accounts, saved versions, semantic job matching, and configurable scoring criteria.
