@echo off
echo ==========================================
echo   CampusEase - Dev Environment Setup
echo ==========================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 ( echo ERROR: Python not found. Install Python 3.11+ first. & pause & exit /b 1 )

echo [2/5] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 ( echo ERROR: pip install failed. & pause & exit /b 1 )

echo [3/5] Setting up .env...
if not exist .env (
    copy .env.example .env
    echo.
    echo  >>> .env file created from .env.example
    echo  >>> Open .env and set your MySQL password in DATABASE_URL
    echo  >>> Then run this script again.
    echo.
    pause
    exit /b 0
)

echo [4/5] Running migrations...
python manage.py migrate
if errorlevel 1 ( echo ERROR: Migration failed. Check your DATABASE_URL in .env & pause & exit /b 1 )

echo [5/5] Done!
echo.
echo ==========================================
echo  Start the server with:
echo  venv\Scripts\python manage.py runserver
echo.
echo  Then open: http://127.0.0.1:8000/
echo.
echo  Login: cr@campusease.com / CR@1234
echo ==========================================
pause
