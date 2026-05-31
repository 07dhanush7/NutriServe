# NutriServe

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Frontend](https://img.shields.io/badge/frontend-HTML%2FCSS%2FJavaScript-blue)
![Backend](https://img.shields.io/badge/backend-Flask-green)
![Database](https://img.shields.io/badge/database-SQLite-lightgrey)
![License](https://img.shields.io/badge/license-MIT-yellow)

NutriServe is a Nutrition and Food Service Management Web Application for meal plan browsing, weekly food ordering, payments, delivery scheduling, notifications, and admin management. The project is organized for two-developer collaboration, with clear ownership for frontend and backend work and a branch-based Git workflow.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- [Environment Variables Setup](#environment-variables-setup)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [GitHub Collaboration](#github-collaboration)
- [Git Workflow](#git-workflow)
- [Command Reference](#command-reference)
- [Deployment Guide](#deployment-guide)
- [Public Release](#public-release)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Project Overview

| Item | Details |
| --- | --- |
| Project Name | NutriServe |
| Project Type | Nutrition and Food Service Management Web Application |
| Frontend Owner | Savishakthi Prasad |
| Backend Owner | Dhanush |
| Frontend Runtime | Static HTML/CSS/JavaScript served locally |
| Backend Runtime | Python Flask REST API |
| Local Database | SQLite |

NutriServe currently uses a static frontend and a Flask backend. The backend exposes REST APIs for authentication, users, meals, orders, payments, delivery, notifications, and admin analytics.

## Features

- User registration, login, JWT authentication, and profile management.
- Meal plans for elders, gym nutrition, and kids.
- Weekly meal ordering with day-wise meal selection.
- Payment creation and payment status tracking.
- Delivery slot and schedule management.
- Notifications for users and staff.
- Admin dashboard, analytics, user management, and meal management.
- Seed data script for demo accounts and sample meals.
- Postman collection and API documentation for backend testing.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Flask |
| ORM | Flask-SQLAlchemy, SQLAlchemy |
| Authentication | Flask-JWT-Extended, Flask-Bcrypt |
| API Support | Flask-CORS |
| Database | SQLite for local development |
| Testing | Pytest |
| API Testing | Postman |
| Future Frontend Option | React/Vite-ready `.gitignore` support |
| Future Database Option | MongoDB-ready `.gitignore` support |

## Installation Guide

### Prerequisites

Install the following before starting:

| Tool | Recommended Version |
| --- | --- |
| Git | Latest stable |
| Python | 3.11 or newer |
| pip | Latest stable |
| VS Code Live Server or Python HTTP server | For frontend |
| Postman | Optional, for API testing |

### Clone Repository

```bash
git clone https://github.com/07dhanush7/NutriServe.git
cd NutriServe
```

## Project Structure

```text
NutriServe/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── instance/
│   ├── tests/
│   ├── API_DOCUMENTATION.md
│   ├── postman_collection.json
│   ├── requirements.txt
│   ├── run.py
│   └── wsgi.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   ├── admin.html
│   ├── cart.html
│   ├── checkout.html
│   ├── frontend_api.js
│   ├── index.html
│   ├── login.html
│   ├── menu.html
│   └── signup.html
├── start_backend.bat
├── start_frontend.bat
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── .gitignore
```

## Environment Variables Setup

Create a backend environment file from the example:

```bash
cd backend
cp .env.example .env
```

On Windows PowerShell:

```powershell
cd backend
Copy-Item .env.example .env
```

Example variables:

```env
FLASK_ENV=development
SECRET_KEY=change-this-secret-key
JWT_SECRET_KEY=change-this-jwt-secret-key
JWT_ACCESS_TOKEN_MINUTES=120
JWT_REFRESH_TOKEN_DAYS=30
AUTO_CREATE_TABLES=1
LOG_LEVEL=INFO
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=5242880
```

Do not commit `.env` files to GitHub.

## Frontend Setup

The current frontend is static HTML, CSS, and JavaScript.

```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:5500/index.html
```

The frontend API base URL is configured in:

```text
frontend/frontend_api.js
```

Current value:

```javascript
const API_BASE_URL = 'http://127.0.0.1:5000/api';
```

## Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

## Database Setup

NutriServe currently uses SQLite for local development. The database is generated automatically when the Flask app starts and `AUTO_CREATE_TABLES=1`.

Local database path:

```text
backend/instance/smart_canteen.db
```

Seed sample data:

```bash
cd backend
python dummy_data.py
```

Sample logins:

| Role | Email | Password |
| --- | --- | --- |
| Admin | admin@nutriserve.com | admin123 |
| User | john@example.com | user123 |
| Delivery Staff | delivery@nutriserve.com | staff123 |

## Running the Project

### Option 1: Windows Batch Files

From the project root:

```powershell
.\start_backend.bat
.\start_frontend.bat
```

### Option 2: Manual Commands

Terminal 1:

```bash
cd backend
python run.py
```

Terminal 2:

```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

Application URLs:

| Service | URL |
| --- | --- |
| Frontend | http://127.0.0.1:5500/index.html |
| Backend | http://127.0.0.1:5000 |
| Health Check | http://127.0.0.1:5000/health |

## API Documentation

Full backend API documentation is available in:

```text
backend/API_DOCUMENTATION.md
```

Postman collection:

```text
backend/postman_collection.json
```

Key endpoint groups:

| Module | Base Path |
| --- | --- |
| Authentication | `/api/auth` |
| Users | `/api/users` |
| Categories | `/api/categories` |
| Meals | `/api/meals` |
| Orders | `/api/orders` |
| Payments | `/api/payments` |
| Delivery | `/api/delivery` |
| Notifications | `/api/notifications` |
| Admin | `/api/admin` |

Example health check:

```bash
curl http://127.0.0.1:5000/health
```

Example login:

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"john@example.com\",\"password\":\"user123\"}"
```

## Screenshots

Add screenshots after the UI is finalized.

```text
docs/screenshots/home.png
docs/screenshots/menu.png
docs/screenshots/cart.png
docs/screenshots/admin-dashboard.png
```

Suggested Markdown format:

```markdown
![Home Page](docs/screenshots/home.png)
![Menu Page](docs/screenshots/menu.png)
![Admin Dashboard](docs/screenshots/admin-dashboard.png)
```

## GitHub Collaboration

### Add Collaborators

Repository owner steps:

1. Open the GitHub repository.
2. Go to `Settings`.
3. Select `Collaborators and teams`.
4. Click `Add people`.
5. Add each developer by GitHub username or profile URL.
6. Assign suitable access, usually `Write` for developers.

Collaborators:

| Developer | Role | GitHub |
| --- | --- | --- |
| Dhanush | Backend Developer | https://github.com/07dhanush7 |
| Savishakthi Prasad | Frontend Developer | https://github.com/savishakthiprasad-eng |

## Git Workflow

Use three long-lived branches:

| Branch | Purpose | Owner |
| --- | --- | --- |
| `main` | Stable production-ready code | Both developers |
| `frontend` | Frontend development | Savishakthi Prasad |
| `backend` | Backend development | Dhanush |

### Recommended Workflow

1. Pull the latest changes from `main`.
2. Switch to your work branch: `frontend` or `backend`.
3. Create a short feature branch from your work branch.
4. Commit small, focused changes.
5. Push your feature branch.
6. Open a pull request into `frontend` or `backend`.
7. After review, merge into the work branch.
8. Open a pull request from `frontend` or `backend` into `main`.
9. Merge into `main` only after review and testing.

### Pull Request Rules

- Keep each pull request focused on one feature, fix, or documentation update.
- Include screenshots for frontend changes.
- Include API examples or test notes for backend changes.
- Request review from the other developer before merging into `main`.
- Resolve merge conflicts locally and rerun tests before pushing.

### Commit Message Convention

Use clear, conventional prefixes:

```text
feat: add weekly order checkout page
fix: handle expired JWT token response
docs: update backend setup guide
test: add auth smoke test
refactor: simplify meal route validation
chore: update gitignore rules
```

## Command Reference

### Git Repository Setup

```bash
git init
git branch -M main
git add .
git commit -m "chore: initial NutriServe project setup"
git remote add origin https://github.com/07dhanush7/NutriServe.git
git push -u origin main
```

### Create Collaboration Branches

```bash
git checkout -b frontend
git push -u origin frontend

git checkout main
git checkout -b backend
git push -u origin backend

git checkout main
```

### Clone Repository

```bash
git clone https://github.com/07dhanush7/NutriServe.git
cd NutriServe
```

### Pull Latest Changes

```bash
git checkout main
git pull origin main
```

Frontend developer:

```bash
git checkout frontend
git pull origin frontend
git merge main
```

Backend developer:

```bash
git checkout backend
git pull origin backend
git merge main
```

### Create a Feature Branch

```bash
git checkout frontend
git pull origin frontend
git checkout -b feat/frontend-cart-ui
```

```bash
git checkout backend
git pull origin backend
git checkout -b feat/backend-order-api
```

### Push Changes

```bash
git status
git add .
git commit -m "feat: describe the change"
git push -u origin <branch-name>
```

### Create Pull Requests

Using GitHub website:

1. Push the feature branch.
2. Open the repository on GitHub.
3. Click `Compare & pull request`.
4. Select the correct base branch.
5. Add a clear title, description, screenshots or test notes.
6. Request review.
7. Merge after approval.

Using GitHub CLI:

```bash
gh pr create --base frontend --head feat/frontend-cart-ui --title "feat: add cart UI" --body "Adds cart page UI and interactions."
gh pr create --base backend --head feat/backend-order-api --title "feat: add order API" --body "Adds order creation API and tests."
```

### Resolve Merge Conflicts

When Git reports a conflict:

```bash
git status
```

Open each conflicted file and choose the correct final code between the conflict markers:

```text
<<<<<<< HEAD
current branch changes
=======
incoming branch changes
>>>>>>> branch-name
```

After editing:

```bash
git add <resolved-file>
git commit -m "fix: resolve merge conflicts"
git push
```

If the conflict happened while pulling with merge:

```bash
git pull origin <branch-name>
git status
git add .
git commit -m "fix: resolve merge conflicts"
git push
```

## GitHub Best Practices

### Branch Protection

Enable branch protection for `main`:

- Require pull request before merging.
- Require at least one approval.
- Require conversation resolution before merge.
- Require status checks if CI is configured.
- Restrict direct pushes to `main`.
- Keep branch history clean with squash or merge commits consistently.

### Issue Tracking

Use GitHub Issues for planned work:

| Label | Purpose |
| --- | --- |
| `frontend` | UI, HTML, CSS, JavaScript work |
| `backend` | Flask API, database, authentication work |
| `bug` | Incorrect behavior |
| `enhancement` | New feature |
| `documentation` | README, API docs, setup guides |
| `priority-high` | Urgent work |

### Project Board Setup

Recommended columns:

```text
Backlog -> Ready -> In Progress -> Review -> Testing -> Done
```

Each issue should include:

- Goal.
- Assigned developer.
- Branch name.
- Acceptance criteria.
- Screenshots or API examples when relevant.

### Release Management

Use semantic versioning:

```text
v1.0.0
v1.1.0
v1.1.1
```

Recommended release flow:

1. Merge tested work into `main`.
2. Create a GitHub release tag.
3. Add release notes with features, fixes, and known issues.
4. Attach screenshots or deployment notes if needed.

## Deployment Guide

Deployment-specific instructions are available in [DEPLOYMENT.md](DEPLOYMENT.md).

### Backend Deployment Checklist

- Set `FLASK_ENV=production`.
- Set strong `SECRET_KEY` and `JWT_SECRET_KEY`.
- Set `AUTO_CREATE_TABLES=1` only for SQLite demo deployments.
- Set `AUTO_CREATE_TABLES=0` after moving to a managed production database and migrations.
- Do not deploy `.env`, `venv`, local SQLite files, or debug logs.
- Use a production WSGI server such as Gunicorn on Linux.
- Configure CORS for the deployed frontend domain.

Render backend settings:

```bash
Build Command: pip install -r requirements.txt
Start Command: cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT
Health Check Path: /health
```

### Frontend Deployment Checklist

- Update `API_BASE_URL` in `frontend/frontend_api.js` to the deployed backend API URL.
- Deploy the `frontend/` folder to a static hosting provider.
- Verify all pages load assets from `frontend/static/`.

Possible hosting options:

| Layer | Options |
| --- | --- |
| Frontend | GitHub Pages, Netlify, Vercel, static hosting |
| Backend | Render, Railway, Fly.io, VPS |
| Database | SQLite for simple demos, PostgreSQL/MySQL for production |

## Public Release

Release notes for `v1.0.0` are available in [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md).

Create the release from GitHub:

1. Open `https://github.com/07dhanush7/NutriServe`.
2. Go to `Releases`.
3. Click `Draft a new release`.
4. Create tag `v1.0.0` from `main`.
5. Use title `NutriServe v1.0.0`.
6. Paste the contents of `RELEASE_NOTES_v1.0.0.md`.
7. Publish the release.

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| Backend does not start | Virtual environment not active or dependencies missing | Activate `venv` and run `pip install -r requirements.txt` |
| Frontend cannot call API | Backend is not running or API URL is wrong | Start backend and verify `frontend/frontend_api.js` |
| CORS error | Frontend origin is blocked in deployment | Configure allowed frontend origin in Flask CORS settings |
| Database tables missing | `AUTO_CREATE_TABLES` disabled | Set `AUTO_CREATE_TABLES=1` locally and restart backend |
| Login fails with sample account | Sample data not loaded | Run `python dummy_data.py` inside `backend/` |
| Port already in use | Another service is using port 5000 or 5500 | Stop the other service or use another port |
| PowerShell activation blocked | Script execution policy | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for the current shell |

## Contributors

### Backend Developer

- Dhanush
- GitHub: https://github.com/07dhanush7

### Frontend Developer

- Savishakthi Prasad
- GitHub: https://github.com/savishakthiprasad-eng

## Future Enhancements

- Convert the frontend to React with Vite.
- Add CI checks for backend tests and frontend linting.
- Add role-based admin UI improvements.
- Add production database support with migrations.
- Add email or SMS notifications.
- Add payment gateway integration.
- Add Docker and Docker Compose setup.
- Add automated API contract testing.
- Add dashboard charts for nutrition and revenue analytics.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
