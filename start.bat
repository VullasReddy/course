@echo off
title Arshith LMS
color 0A
cls

echo.
echo  ============================================
echo    ARSHITH LMS
echo  ============================================
echo.
echo  Setting up... please wait...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed!
    echo.
    echo  Please install Python from:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: During install, check the box
    echo  that says "Add Python to PATH"
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b
)

echo  Python found. Installing packages...
python -m pip install django djangorestframework djangorestframework-simplejwt django-cors-headers reportlab pillow --quiet --no-warn-script-location
echo  Packages installed.
echo.

echo  Setting up database...
python manage.py migrate --run-syncdb >nul 2>&1

python manage.py shell -c "from apps.courses.models import Course; import sys; sys.exit(0 if Course.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo  Loading courses...
    python manage.py loaddata apps\courses\fixtures\initial_courses.json >nul 2>&1
    python manage.py loaddata apps\courses\fixtures\initial_users.json >nul 2>&1
    python manage.py loaddata apps\courses\fixtures\initial_learning.json >nul 2>&1
)
echo  Database ready.
echo.

echo  ============================================
echo   Opening browser automatically...
echo   URL: http://127.0.0.1:8000
echo.
echo   Student: student@arshith.com / student123
echo   Admin:   admin@arshith.com   / admin123
echo  ============================================
echo.
echo  DO NOT close this window while using the app!
echo.

REM Auto-open browser after 2 seconds
start "" timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8000"

python manage.py runserver
pause
