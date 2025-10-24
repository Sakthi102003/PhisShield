@echo off
cd %~dp0
cd backend
call venv\Scripts\activate.bat
python app.py