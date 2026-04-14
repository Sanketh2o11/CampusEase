<div align="center">

# CampusEase

**All-in-one campus companion for engineering students.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-default-003B57?style=flat-square&logo=sqlite&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

![CampusEase Demo](assets/demo.gif)

</div>



CampusEase puts attendance, exams, notes, notices, and timetables in one place — no more juggling WhatsApp groups, random PDFs, and memory. Two roles: **CRs** manage content, **Students** consume it. Everything is scoped to your batch.

- **Track attendance** per subject with live percentages and 75% threshold warnings
- **View exam schedules** set by your CR, track your scores privately, and get AI-generated study plans
- **Share and find study materials** — Drive links, YouTube, Classroom — with a thank-you system
- **Stay updated** with notices, deadlines, and polls from your CR
- **Report lost items** or claim found ones with a built-in flow
- **AI assistant** that uses your actual data (attendance, exams, deadlines) to tell you what to focus on — not generic advice

<details>
<summary><strong>View Full Module Breakdown & AI Details</strong></summary>
<br>
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

</details>

---

## Quick Start

**Try it out — no database setup needed.** Requires Python 3.11+.

```bash
git clone https://github.com/Sanketh2o11/CampusEase.git
cd CampusEase


python -m venv venv     #Create a virtual Environment

# Activate virtual environment:
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
python manage.py migrate
python scripts/create_test_user.py
python manage.py runserver
```
Open `http://127.0.0.1:8000`.

Login with `cr@test.com` / `campusease123` (CR) 
or
`student@test.com` / `campusease123` (Student).

> 👉 Facing issues? Jump to [Troubleshooting](#troubleshooting).

> Gemini API key is optional. Set `GEMINI_API_KEY` in a `.env` file to enable the AI assistant.

## Development Setup (MySQL)

For active development with sample data. Requires MySQL 8.0+.

1. Create the database:
   ```sql
   CREATE DATABASE campusease CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Configure environment:
   ```bash
   copy .env.example .env   # then uncomment and edit DATABASE_URL with your MySQL password
   ```
   > **Windows shortcut:** `scripts\setup.bat --mysql` automates venv + dependency install + `.env` setup.
3. Import sample data:
   ```bash
   mysql -u root -p campusease < docker/init/campusease_dev.sql
   ```
4. Run:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Pre-loaded test accounts (from `campusease_dev.sql`, batch **CS-2023**):

| Role | Email | Password |
|------|-------|----------|
| CR | `cr@campusease.com` | `CR@1234` |
| Student | `student1@campusease.com` | `Student@1234` |

<details>
<summary><strong>Docker alternative</strong></summary>

```bash
docker compose up -d db
docker compose run --rm --service-ports web
```

Open `http://localhost:8000`. Sample data is imported automatically. You'll be prompted for an optional Gemini API key on startup.

```bash
# Stop
docker compose down

# Full reset (wipes DB)
docker compose down -v && docker compose up -d db && docker compose run --rm --service-ports web
```

</details>

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

## Tech Stack

Python 3.11 / Django 5.2 / SQLite or MySQL 8.0 / Vanilla HTML+CSS+JS / Google Gemini API (optional) / Docker Compose

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `mysqlclient` install fails | Remove `mysqlclient==2.2.8` from `requirements.txt` — not needed for SQLite |
| Can't login with `cr@test.com` | Run `python scripts/create_test_user.py` — SQLite starts empty |
| Can't connect to MySQL | Start MySQL: `net start MySQL80` (Win) / `brew services start mysql` (Mac) |
| Unknown column error | Run `python manage.py migrate` |
| Port 8000 in use | Change port in `docker-compose.yml` or stop the other process |
| AI Assistant not working | Set `GEMINI_API_KEY` in a `.env` file |

---

<div align="center">
Made with care by the CampusEase team
</div>
