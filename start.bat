@echo off
title Arshith LMS - Setup & Start
color 0A

echo ============================================
echo   ARSHITH LMS - Auto Setup ^& Start
echo ============================================
echo.

echo [1/4] Installing required packages...
pip install -r requirements.txt --quiet
echo Done!
echo.

echo [2/4] Setting up database tables...
python manage.py migrate --run-syncdb
echo Done!
echo.

echo [3/4] Checking if courses exist...
python manage.py shell -c "from apps.courses.models import Course; import sys; sys.exit(0 if Course.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo No courses found - seeding database...
    python manage.py seed_data
    echo Importing Python course modules...
    python manage.py import_modules "Python"
    echo Importing Web Development modules...
    python manage.py import_modules "Web"
    echo All courses loaded!
) else (
    echo Courses already exist - skipping seed.
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
