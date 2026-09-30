@echo off
title Arshith LMS - Setup & Start
color 0A

echo ============================================
echo   ARSHITH LMS - Auto Setup ^& Start
echo ============================================
echo.

echo [1/4] Installing required packages...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: pip failed. Make sure Python is installed.
    pause
    exit /b 1
)
echo Done!
echo.

echo [2/4] Setting up database tables...
python manage.py migrate --run-syncdb
echo Done!
echo.

echo [3/4] Loading courses into database...
python manage.py shell -c "from apps.courses.models import Course; import sys; sys.exit(0 if Course.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo Courses not found - loading from fixture...
    python manage.py loaddata apps/courses/fixtures/initial_courses.json
    python manage.py loaddata apps/courses/fixtures/initial_users.json
    python manage.py loaddata apps/courses/fixtures/initial_learning.json
    echo All courses loaded successfully!
) else (
    echo Courses already loaded - skipping.
)
echo Done!
echo.

echo [4/4] Starting server...
echo.
echo ============================================
echo   Open browser: http://127.0.0.1:8000
echo.
echo   Student: student@arshith.com / student123
echo   Admin:   admin@arshith.com   / admin123
echo ============================================
echo.
python manage.py runserver
pause
