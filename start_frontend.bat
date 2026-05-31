@echo off
echo Starting Smart Canteen Frontend...
cd /d "%~dp0frontend"
python -m http.server 5500 --bind 127.0.0.1
pause
