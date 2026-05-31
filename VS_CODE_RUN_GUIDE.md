# VS Code Run Guide

Use two VS Code terminals.

## Terminal 1 - Backend

```powershell
cd backend
venv\Scripts\activate
python run.py
```

Alternative from the project root:

```powershell
.\start_backend.bat
```

Backend runs at:

```text
http://127.0.0.1:5000
```

## Terminal 2 - Frontend

```powershell
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

Alternative from the project root:

```powershell
.\start_frontend.bat
```

Frontend runs at:

```text
http://127.0.0.1:5500/index.html
```

## Test

Open:

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/health
http://127.0.0.1:5500/index.html
```

Sample logins:

```text
Admin: admin@nutriserve.com / admin123
User: john@example.com / user123
Delivery: delivery@nutriserve.com / staff123
```

Stop either server with `Ctrl + C` in its terminal.
