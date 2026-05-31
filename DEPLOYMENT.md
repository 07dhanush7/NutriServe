# NutriServe Deployment Guide

This guide prepares NutriServe for public deployment on Render.

## Deployment Targets

| Component | Recommended Render Service | Notes |
| --- | --- | --- |
| Flask API | Web Service | Runs `backend/wsgi.py` with Gunicorn |
| Static Frontend | Static Site | Serves files from `frontend/` |
| Database | SQLite for demo, Postgres for production | SQLite needs a persistent disk for durable data |

## Backend Deployment on Render

Render supports Python web services and commonly uses `pip install -r requirements.txt` as the build command and Gunicorn as the start command for Python apps.

### Backend Service Settings

Create a new Render Web Service:

| Setting | Value |
| --- | --- |
| Repository | `https://github.com/07dhanush7/NutriServe` |
| Branch | `main` |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT` |
| Health Check Path | `/health` |

The same values are also provided in `render.yaml`.

### Environment Variables

Set these in Render under `Environment`:

| Key | Example Value | Required | Notes |
| --- | --- | --- | --- |
| `FLASK_ENV` | `production` | Yes | Loads production config |
| `SECRET_KEY` | generated secret | Yes | Use a long random value |
| `JWT_SECRET_KEY` | generated secret | Yes | Use a different long random value |
| `AUTO_CREATE_TABLES` | `1` | Yes for SQLite demo | Creates SQLite tables on startup |
| `JWT_ACCESS_TOKEN_MINUTES` | `120` | No | Access token lifetime |
| `JWT_REFRESH_TOKEN_DAYS` | `30` | No | Refresh token lifetime |
| `LOG_LEVEL` | `INFO` | No | Production logging level |
| `UPLOAD_FOLDER` | `uploads` | No | Upload path |
| `MAX_CONTENT_LENGTH` | `5242880` | No | Upload limit in bytes |

## SQLite Notes

SQLite works for demos and coursework deployments, but Render instances use an ephemeral filesystem by default. That means local SQLite data can be lost after a redeploy or restart unless you attach a persistent disk.

For a public production app:

- Use Render Postgres or another managed database.
- Keep SQLite only for local development or demos.
- Do not commit `backend/instance/smart_canteen.db`.

## Frontend Deployment on Render

Create a Render Static Site:

| Setting | Value |
| --- | --- |
| Repository | `https://github.com/07dhanush7/NutriServe` |
| Branch | `main` |
| Root Directory | `frontend` |
| Build Command | leave empty |
| Publish Directory | `.` |

After the backend Web Service is deployed, update:

```text
frontend/frontend_api.js
```

Change:

```javascript
const API_BASE_URL = 'http://127.0.0.1:5000/api';
```

To:

```javascript
const API_BASE_URL = 'https://your-render-backend-url.onrender.com/api';
```

Commit and push the change to redeploy the frontend.

## Make the App Public

1. Deploy the backend as a Render Web Service.
2. Deploy the frontend as a Render Static Site.
3. Update `frontend/frontend_api.js` to use the live backend URL.
4. Confirm the backend health check works:

```text
https://your-render-backend-url.onrender.com/health
```

5. Open the frontend public URL provided by Render.
6. Test registration, login, meal browsing, ordering, payment creation, and admin pages.

## GitHub Push Commands

```bash
git checkout main
git pull origin main
git add .
git commit -m "chore: prepare NutriServe for public release"
git push origin main
```

## Create GitHub Release v1.0.0

### From GitHub Website

1. Open `https://github.com/07dhanush7/NutriServe`.
2. Go to `Releases`.
3. Click `Draft a new release`.
4. Click `Choose a tag` and enter `v1.0.0`.
5. Target branch: `main`.
6. Release title: `NutriServe v1.0.0`.
7. Paste the release description from `RELEASE_NOTES_v1.0.0.md`.
8. Click `Publish release`.

### From GitHub CLI

```bash
gh release create v1.0.0 --target main --title "NutriServe v1.0.0" --notes-file RELEASE_NOTES_v1.0.0.md
```

## Production Readiness Checklist

- Set strong `SECRET_KEY` and `JWT_SECRET_KEY`.
- Disable debug mode in production.
- Use HTTPS-only public URLs.
- Restrict CORS to the deployed frontend domain.
- Move production data from SQLite to a managed database.
- Add database migrations for production schema changes.
- Add CI to run `python -m pytest` before merging.
- Protect the `main` branch with pull request reviews.
- Keep `.env`, virtual environments, logs, and SQLite DB files out of Git.
- Review authentication and admin routes before accepting public users.

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| Build fails on Render | Dependencies missing | Confirm `requirements.txt` exists at repo root and includes `-r backend/requirements.txt` |
| `gunicorn: command not found` | Gunicorn missing | Confirm `gunicorn==23.0.0` is in `backend/requirements.txt` |
| App starts but database tables are missing | `AUTO_CREATE_TABLES` disabled | Set `AUTO_CREATE_TABLES=1` for SQLite demo deployment |
| Frontend cannot call backend | API URL still points to localhost | Update `frontend/frontend_api.js` with the Render backend URL |
| Data disappears after redeploy | SQLite on ephemeral filesystem | Attach a persistent disk or migrate to Postgres |
| Health check fails | Wrong start command or app crash | Use `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT` and inspect Render logs |
