<div align="center">
  <h1>SubTrack</h1>
  <p>Daily expense tracking with optional income, smart limits, and proactive alerts.</p>
  <p>
    <img alt="Django" src="https://img.shields.io/badge/Django-4.x-0C4B33?logo=django&logoColor=white" />
    <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" />
    <img alt="License" src="https://img.shields.io/badge/License-MIT-000000" />
  </p>
</div>

---

## Overview

SubTrack is a Django-based expense tracker that helps you log daily spending, set optional income, and get notified when you drift over budget. It keeps the focus on daily discipline with clear limits and actionable alerts.

## Feature Highlights

| Area | What you get |
| --- | --- |
| Income (Optional) | Monthly income input to power daily limits |
| Expenses | Fast CRUD for daily expenses |
| Daily Limit | Auto-calculated per-day spending limit |
| Overspend Alerts | Email alerts when you exceed your allowance |
| Daily Reminders | Prompts to log expenses each day |
| Reasons | Capture why each expense happened |
| Analytics | Reason-based charts and insights |
| Notifications | Email dispatch + audit log |

## Tech Stack

- Backend: Python, Django
- Database: SQLite for development, PostgreSQL-compatible setup for production
- Frontend: Django Templates, Bootstrap 5, Chart.js
- ORM: Django ORM

## Quick Start

```bash
# 0) Enable debug for local development
# PowerShell: $env:DJANGO_DEBUG="true"
# Bash/Zsh: export DJANGO_DEBUG=true

# 1) Create and activate a virtual environment
# 2) Install dependencies
pip install -r requirements.txt

# 3) Apply migrations
python manage.py migrate

# 4) Create an admin account
python manage.py createsuperuser

# 5) Run the server
python manage.py runserver
```

## Production Deploy

1. Set environment variables (see `.env.example`) in your hosting platform.
2. Use PostgreSQL and set `DATABASE_URL`.
3. Turn off debug with `DJANGO_DEBUG=false`.
4. Configure allowed hosts and CSRF trusted origins.
5. Collect static assets and run migrations.

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn subtrack_project.wsgi:application
```

## Common Commands

| Task | Command |
| --- | --- |
| Run the app | `python manage.py runserver` |
| Create admin user | `python manage.py createsuperuser` |
| Apply migrations | `python manage.py migrate` |
| Send daily reminders | `python manage.py send_due_reminders` |

## Notifications

- Daily reminders prompt users to log expenses.
- Overspend alerts trigger when month-to-date spend exceeds the prorated allowance.

In development, emails are printed to the console. Configure SMTP in `subtrack_project/settings.py` for production.

## Project Structure

```
.
+-- docs
+-- static
+-- subtrack
+-- subtrack_project
+-- templates
+-- db.sqlite3
+-- manage.py
+-- README.md
+-- requirements.txt
```

## Academic Scope Mapping

This implementation covers:

- Authentication module
- Expense CRUD with reasons
- Dashboard and analytics views
- Notification process
- Daily limit and overspend logic
- Non-functional requirements documentation in `docs/PROJECT_PROPOSAL.md`

## License

MIT License. See `LICENSE`.
