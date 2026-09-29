# Placement Portal

A web-based placement management system built with Flask and SQLite for the IIT Madras BS Degree program (MAD 1 Project). It connects students, companies, and an admin on a single platform to streamline the campus placement process.

---

## Features

### Admin
- Login with pre-seeded credentials
- Verify or reject company registrations
- Approve or reject placement drives posted by companies
- View all students, companies, drives, and applications
- Search students by name, ID, or phone
- Search companies by name or field
- Deactivate companies and delete placement drives or student records

### Company
- Register and log in
- Post new placement drives (pending admin approval)
- View, close, and manage their drives
- Review applicants — shortlist, select, or reject them
- View shortlisted and selected applicants per drive

### Student
- Register with resume upload (PDF stored in DB)
- Log in and access a personalised dashboard
- Browse and search verified placement drives
- Apply to drives and track application status (applied → shortlisted → selected/rejected)
- View application history
- Update profile (phone, academic level, GitHub, resume)

---

## Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Backend    | Python, Flask               |
| Database   | SQLite via Flask-SQLAlchemy |
| Templating | Jinja2                      |
| Frontend   | HTML, CSS (custom per role) |

---

## Project Structure

```
├── app.py                  # App factory and entry point
├── application/
│   ├── controllers.py      # All route handlers
│   ├── model.py            # SQLAlchemy models
│   └── database.py         # DB instance
├── templates/
│   ├── home.html
│   ├── admin-login.html
│   ├── student-login.html
│   ├── student-register.html
│   ├── company-login.html
│   ├── company-register.html
│   ├── admin/              # Admin dashboard templates
│   ├── student/            # Student dashboard templates
│   └── company/            # Company dashboard templates
├── static/
│   ├── css/                # Role-specific stylesheets
│   └── images/             # Static assets
├── instance/
│   └── placement_portal.db # SQLite database (auto-created)
└── requirements.txt
```

---

## Database Models

- **User** — base auth record (email, password, role: admin / student / company)
- **Student** — profile linked to User (name, phone, academic level, resume, GitHub)
- **Company** — company profile linked to User (name, HR contact, website, field, status)
- **PlacementDrive** — job drive posted by a company (title, mode, package, deadline, eligibility, status)
- **Applications** — student application to a drive (status: applied → shortlisted → selected / rejected)

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd placement-portal

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

On first run, the database is created automatically and a default admin account is seeded.

---

## Default Admin Credentials

| Field    | Value                  |
|----------|------------------------|
| Email    | iitmadmin123@gmail.com |
| Password | admin@123              |

---

## Application Flow

```
Student registers → logs in → browses drives → applies
                                                    ↓
Company posts drive → admin approves → company reviews applications
                                                    ↓
                              shortlist → select / reject applicants
```

---

## Key Routes

| Role    | Route                            | Description                        |
|---------|----------------------------------|------------------------------------|
| General | `/`                              | Home page                          |
| Admin   | `/admin-login`                   | Admin login                        |
| Admin   | `/admin-dashboard`               | Overview dashboard                 |
| Student | `/student-register`              | Student registration               |
| Student | `/student-login`                 | Student login                      |
| Student | `/student-dashboard/<id>`        | Student home with available drives |
| Student | `/student-profile/<id>`          | Profile & resume update            |
| Student | `/student-history/<id>`          | Application history                |
| Company | `/company-register`              | Company registration               |
| Company | `/company-login`                 | Company login                      |
| Company | `/company-dashboard/<id>`        | Company overview                   |
| Company | `/add-drive/<company_id>`        | Post a new placement drive         |
| Misc    | `/resume/<student_id>`           | Serve student resume as PDF        |

---

## Notes

- Passwords are stored in plain text — this is an academic project and not intended for production use.
- Resume files are stored as binary blobs directly in the SQLite database.
- No session management is implemented; URL-based navigation is used for role routing.
