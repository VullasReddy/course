@echo off
title Arshith LMS
color 0A
cls

echo.
echo  =============================================
echo    ARSHITH LMS - Starting...
echo  =============================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed!
    echo  Please install Python from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

echo  [1/3] Installing packages...
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers reportlab pillow --quiet
echo  Done.
echo.

echo  [2/3] Setting up database...
python manage.py migrate --run-syncdb >nul 2>&1

REM Check if courses exist, if not load fixtures
python manage.py shell -c "from apps.courses.models import Course; import sys; sys.exit(0 if Course.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo  Loading course data...
    python manage.py loaddata apps\courses\fixtures\initial_courses.json >nul 2>&1
    python manage.py loaddata apps\courses\fixtures\initial_users.json >nul 2>&1
    python manage.py loaddata apps\courses\fixtures\initial_learning.json >nul 2>&1
)
echo  Done.
echo.

echo  [3/3] Starting server...
echo.
echo  =============================================
echo.
echo   Open this link in your browser:
echo.
echo      http://127.0.0.1:8000
echo.
echo   Login:
echo      Student -^> student@arshith.com / student123
echo      Admin   -^> admin@arshith.com   / admin123
echo.
echo  =============================================
echo.
echo  (Press CTRL+C to stop the server)
echo.
python manage.py runserver
pause
