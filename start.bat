@echo off
title Arshith LMS - Setup & Start
color 0A

echo ============================================
echo   ARSHITH LMS - Auto Setup ^& Start
echo ============================================
echo.

echo [1/3] Installing required packages...
pip install -r requirements.txt --quiet
echo Done!
echo.

echo [2/3] Setting up database...
python manage.py migrate --run-syncdb
echo Done!
echo.

echo [3/3] Starting server...
echo.
echo ============================================
echo   Open your browser: http://127.0.0.1:8000
echo.
echo   Student Login: student@arshith.com / student123
echo   Admin Login:   admin@arshith.com   / admin123
echo ============================================
echo.
python manage.py runserver
pause
