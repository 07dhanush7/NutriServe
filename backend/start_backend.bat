@echo off
echo Starting Smart Canteen Backend...
cd /d "%~dp0"
if exist venv\Scripts\activate call venv\Scripts\activate
python run.py
pause
