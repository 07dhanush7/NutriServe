@echo off
echo Starting Smart Canteen Frontend...
cd /d "%~dp0"
python -m http.server 5500 --bind 127.0.0.1
pause
