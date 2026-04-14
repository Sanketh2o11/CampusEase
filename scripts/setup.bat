@echo off
cd /d "%~dp0.."

echo ==========================================
echo   CampusEase - Dev Environment Setup
echo ==========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 ( echo ERROR: Python not found. Install Python 3.11+ first. & pause & exit /b 1 )

echo [2/4] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 ( echo ERROR: pip install failed. & pause & exit /b 1 )

if "%1"=="--mysql" (
    echo [3/4] Setting up MySQL .env...
    if not exist .env (
        copy .env.example .env
        echo.
        echo  >>> .env created from .env.example
        echo  >>> Uncomment and edit DATABASE_URL in .env with your MySQL password.
        echo  >>> Then run: venv\Scripts\python manage.py migrate
        echo.
        pause
        exit /b 0
    )
    echo [4/4] Running migrations...
    python manage.py migrate
    if errorlevel 1 ( echo ERROR: Migration failed. Check DATABASE_URL in .env & pause & exit /b 1 )
    echo.
    echo ==========================================
    echo  Start the server:
    echo    venv\Scripts\python manage.py runserver
    echo.
    echo  Open: http://127.0.0.1:8000/
    echo  Login: cr@campusease.com / CR@1234
    echo ==========================================
) else (
    echo [3/4] Using SQLite ^(default^)...
    echo [4/4] Running migrations + creating test accounts...
    python manage.py migrate
    if errorlevel 1 ( echo ERROR: Migration failed. & pause & exit /b 1 )
    python scripts\create_test_user.py
    echo.
    echo ==========================================
    echo  Start the server:
    echo    venv\Scripts\python manage.py runserver
    echo.
    echo  Open: http://127.0.0.1:8000/
    echo  Login: cr@test.com / campusease123
    echo ==========================================
)
pause
