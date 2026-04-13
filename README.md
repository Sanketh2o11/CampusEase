<div align="center">

# CampusEase

**All-in-one campus companion for engineering students.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

</div>

---

## What does this do?


![CampusEase Demo](assets/demo.gif)
*A quick walkthrough of login, dashboard, attendance tracking, and AI assistant.*

---

Students juggle attendance, exams, notes, notices, and timetables across WhatsApp groups, random PDFs, and memory. CampusEase puts it all in one place.

- **Track attendance** per subject with live percentages and 75% threshold warnings
- **View exam schedules** set by your CR, track your scores privately, and get AI-generated study plans
- **Share and find study materials** — Drive links, YouTube, Classroom — with a thank-you system
- **Stay updated** with notices, deadlines, and polls from your CR
- **Report lost items** or claim found ones with a built-in flow
- **AI assistant** that uses your actual data (attendance, exams, deadlines) to tell you what to focus on — not generic advice

Two roles: **Class Representatives (CRs)** manage content. **Students** consume it. Everything is scoped to your batch.

### Modules

| Module | What it does |
|--------|-------------|
| **Dashboard** | Attendance health, upcoming exams, unread notices, 7-day strip, AI daily briefing |
| **Timetable** | Weekly class schedule (CR edits, students view) |
| **Attendance** | Per-subject daily tracking with 75% threshold warnings |
| **Notices** | Announcements, events, deadlines, Yes/No/Maybe polls |
| **Materials** | Share study links (Drive, YouTube, etc.) with thank-you counter |
| **Exams** | Batch exam schedule, personal scores, AI-powered study plan & topic suggestions |
| **Lost & Found** | Report, claim, and resolve lost/found items |

### AI Assistant

A context-aware AI assistant (Gemini API) that adapts based on where you are:
- **Dashboard** — "What should I focus today?" with priority-sorted advice using your real attendance, exams, and deadlines
- **Exams** — "Study Plan" and "Important Topics" buttons per upcoming exam, using syllabus and attendance data
- **Materials** — "Explain" button per subject, exam-aware when relevant

One endpoint, one prompt, multiple contexts. Not a chatbot — an assistant that knows your data.



## Quick Start

### Docker (recommended)

```bash
git clone https://github.com/your-username/CampusEase.git
cd CampusEase
docker compose up -d db
docker compose run --rm --service-ports web
```

Open `http://localhost:8000`. Done.

> Gemini API key is optional — you'll be prompted on startup. Press Enter to skip.

```bash
# Stop
docker compose down

# Full reset (wipes DB)
docker compose down -v && docker compose up -d db && docker compose run --rm --service-ports web
```

### Manual Setup

**Requires:** Python 3.11+, MySQL 8.0+

```bash
git clone https://github.com/Sanketh2o11/CampusEase.git
cd CampusEase
# Windows (Command Prompt)
python -m venv venv && venv\Scripts\activate

# Windows (PowerShell) — use this if the above doesn't work
python -m venv venv
.\venv\Scripts\Activate.ps1

# python3 -m venv venv && source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

> **Windows shortcut:** `scripts\setup.bat` automates steps 1–4 above.

```sql
-- Create DB in MySQL
CREATE DATABASE campusease CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```bash
# Optional: import sample data
mysql -u root -p campusease < campusease_dev.sql

# Configure
copy .env.example .env   # then edit DATABASE_URL with your MySQL password

# Run
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

---

## Test Accounts

Pre-loaded via `campusease_dev.sql`. All in batch **CS-2023**.

| Role | Email | Password |
|------|-------|----------|
| CR | `cr@campusease.com` | `CR@1234` |
| Student | `student1@campusease.com` | `Student@1234` |
| Student | `student2@campusease.com` | `Student@1234` |
| Student | `student3@campusease.com` | `Student@1234` |

---

## Tech Stack

Python 3.11 / Django 5.2 / MySQL 8.0 / Vanilla HTML+CSS+JS / Google Gemini API (optional) / Docker Compose

---

## Project Structure

```
CampusEase/
├── docker/               Dockerfile, entrypoint, sample DB init SQL
├── scripts/              Dev utilities (setup.bat, create_test_user.py)
├── accounts/             Custom User + Batch models, auth
├── attendance/           Per-subject attendance tracking
├── core/                 Dashboard
├── exams/                Batch exams + personal results
├── lostfound/            Lost & found board
├── materials/            Study resource sharing
├── notices/              Announcements + polls
├── timetable/            Weekly schedule
├── ai/                   Context-aware AI assistant (single endpoint)
├── templates/            Django HTML templates
├── static/               CSS
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: MySQLdb` | `pip install mysqlclient` |
| Can't connect to MySQL | Start MySQL: `net start MySQL80` (Win) / `brew services start mysql` (Mac) |
| Unknown column error | Run `python manage.py migrate` |
| Port 8000 in use | Change port in `docker-compose.yml` or stop the other process |

---

<div align="center">
Made with care by the CampusEase team
</div>
