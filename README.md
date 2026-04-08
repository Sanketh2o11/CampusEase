<div align="center">

# 🎓 CampusEase

**A modern campus management platform built for students and class representatives.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

[Features](#-features) • [Getting Started](#-getting-started) • [Test Accounts](#-test-accounts) • [Project Structure](#-project-structure) • [FAQ](#-faq)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

**📊 Dashboard**
Real-time overview of attendance health, upcoming exams, unread notices, and a 7-day weekly calendar strip.

**🗓 Timetable**
CR sets the weekly class schedule. Students get a clean read-only view with today's column highlighted.

**✅ Attendance**
Per-subject daily tracking with live percentage, progress rings, 75% threshold warnings, and a day-filtered calendar view.

**📢 Notices**
CR posts announcements, events, and urgent alerts — with optional deadlines and Yes/No/Maybe polls.

</td>
<td width="50%">

**📚 Materials**
Upload and share study resources via Google Drive, Google Classroom, YouTube, or any link. One-click Thank You counter.

**📝 Exams**
Batch exam schedule visible to all students in the batch. Personal score and notes tracked privately per student.

**🔍 Lost & Found**
Report lost or found items with images and contact info. Claim flow, contact reveal, and CR resolve/delete controls.

</td>
</tr>
</table>

---

## 🚀 Getting Started

There are two ways to run CampusEase locally:

| Method | Best for | Requires |
|--------|----------|----------|
| 🐳 **Docker** (recommended) | Mac, Linux, Windows | Docker Desktop |
| 🖥 **Manual** | Windows with MySQL already set up | Python, MySQL |

---

### 🐳 Docker Setup (any OS)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash
# 1. Clone the repo
git clone https://github.com/your-username/CampusEase.git
cd CampusEase

# 2. Start the database (runs in background)
docker compose up -d db

# 3. Start the app (runs in foreground — Gemini prompt appears here)
docker compose run --rm --service-ports web
```

Docker handles Python, MySQL, migrations, and sample data automatically.

Open `http://localhost:8000` and log in with the [test accounts](#-test-accounts) below.

**To stop:**
```bash
# Ctrl+C stops the web container, then:
docker compose down
```

**To reset the database completely:**
```bash
docker compose down -v   # -v removes the MySQL volume
docker compose up -d db
docker compose run --rm --service-ports web
```

> 💡 **Hot reload is on** — edit any `.py` file or template and Django restarts automatically. No rebuild needed.

> 🔑 **Gemini AI feature:** On startup you'll be prompted to enter a Gemini API key (press Enter to skip). You can also pre-set it by adding `GEMINI_API_KEY=your-key` to a `.env` file in the project root. All other features work without it.

---

### 🖥 Manual Setup (Windows)

### Prerequisites

Make sure the following are installed on your machine before proceeding:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| MySQL | 8.0+ | [mysql.com](https://dev.mysql.com/downloads/mysql/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

> ⚠️ **Windows:** During Python installation, make sure to check **"Add Python to PATH"**.
> 📝 **MySQL:** Note your root password during setup — you'll need it later.

---

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/CampusEase.git
cd CampusEase
```

#### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### Database Setup

#### Step 1 — Create the MySQL database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE campusease CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### Step 2 — Import sample data *(recommended for dev team)*

> Get the `campusease_dev.sql` file from your team lead and place it in the project root.

```bash
mysql -u root -p campusease < campusease_dev.sql
```

> **Starting fresh instead?** Skip this step. Migrations will create all empty tables.

---

### Environment Configuration

Copy the example environment file and fill in your values:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and update:

```env
DEBUG=True
SECRET_KEY=any-long-random-string-for-local-dev
DATABASE_URL=mysql://root:YOUR_MYSQL_PASSWORD@127.0.0.1:3306/campusease
```

> 🔑 Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL root password.

---

### Run Migrations

```bash
python manage.py migrate
```

---

### Start the Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

### ⚡ Windows Quickstart

If you're on Windows, you can run the automated setup script after completing the database and `.env` steps above:

```bash
setup.bat
```

This handles virtual environment creation, dependency installation, and migrations automatically.

---

## 🔐 Test Accounts

> These accounts are pre-loaded if you imported `campusease_dev.sql`. All belong to batch **CS-2023 — Computer Science**.

| Role | Email | Password | Access |
|------|-------|----------|--------|
| 👑 **CR** | `cr@campusease.com` | `CR@1234` | Full access — post notices, edit timetable, manage lost & found, delete content |
| 🎓 Student | `student1@campusease.com` | `Student@1234` | Standard student access |
| 🎓 Student | `student2@campusease.com` | `Student@1234` | Standard student access |
| 🎓 Student | `student3@campusease.com` | `Student@1234` | Standard student access |

---

## 📁 Project Structure

```
CampusEase/
│
├── 📂 accounts/          # Custom User model, Batch model, auth views
├── 📂 attendance/        # Attendance tracking, per-subject records
├── 📂 core/              # Dashboard view and context
├── 📂 exams/             # Batch exams + personal result tracking
├── 📂 lostfound/         # Lost & found board with claim/resolve flow
├── 📂 materials/         # Study material uploads and thank-you counter
├── 📂 notices/           # Announcements, events, polls
├── 📂 timetable/         # Weekly timetable (CR edit, student view)
│
├── 📂 templates/         # All Django HTML templates
├── 📂 static/            # CSS, JavaScript, images
├── 📂 campusease/        # Project settings, URLs, WSGI
│
├── 📄 manage.py
├── 📄 requirements.txt
├── 📄 .env.example       # Environment variable template
├── 📄 setup.bat          # Windows automated setup script
├── 📄 Dockerfile         # Docker image definition
├── 📄 docker-compose.yml # Dev stack (Django + MySQL)
├── 📄 entrypoint.sh      # Container startup script
└── 📄 campusease_dev.sql # Database dump (shared separately)
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | Django 5.2 |
| Database | MySQL 8.0 |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Auth | Django built-in + custom User model |
| Config | django-environ |

---

## ❓ FAQ

<details>
<summary><b>ModuleNotFoundError: No module named 'MySQLdb'</b></summary>

Make sure your virtual environment is activated and run:
```bash
pip install mysqlclient
```
</details>

<details>
<summary><b>Can't connect to MySQL server (OperationalError 2003)</b></summary>

MySQL isn't running. Start it:
```bash
# Windows
net start MySQL80

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```
</details>

<details>
<summary><b>Unknown column '...' in field list</b></summary>

You have unapplied migrations. Run:
```bash
python manage.py migrate
```
</details>

<details>
<summary><b>The page shows raw {{ template tags }} instead of real content</b></summary>

You're opening the `.html` file directly in your browser. Always access the app through the dev server at `http://127.0.0.1:8000/` — never open template files directly.
</details>

<details>
<summary><b>.env file not found / SECRET_KEY missing</b></summary>

You haven't created your `.env` file yet. Run:
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux
```
Then fill in your `DATABASE_URL` with your MySQL password.
</details>

<details>
<summary><b>Docker: port 8000 already in use</b></summary>

Something else is using port 8000. Either stop that process or change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"   # access at http://localhost:8080 instead
```
</details>

<details>
<summary><b>Docker: web container exits immediately / migration error</b></summary>

Usually means MySQL wasn't ready in time despite the healthcheck. Try:
```bash
docker compose down && docker compose up
```
If it persists, check logs with `docker compose logs db` to see if MySQL had an import error.
</details>

---

## 👥 Contributing

This is a dev team project. To contribute:

1. Pull the latest changes from `main`
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and test locally
4. Push and open a pull request

---

<div align="center">

Made with ❤️ by the CampusEase Dev Team

</div>
