@echo off
title Arshith LMS
color 0A
cls

echo.
echo  ============================================
echo    ARSHITH LMS - Auto Setup and Start
echo  ============================================
echo.

REM ---- Check if Python is installed ----
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python not found. Downloading and installing Python...
    echo  Please wait - this only happens once!
    echo.

    REM Download Python installer silently
    curl -o "%TEMP%\python_installer.exe" "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" --progress-bar

    REM Install Python silently with PATH added
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=0

    REM Refresh PATH so python command works
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"

    echo.
    echo  Python installed! Continuing setup...
    echo.
)

REM ---- Install packages ----
echo  [1/3] Installing required packages...
python -m pip install django djangorestframework djangorestframework-simplejwt django-cors-headers reportlab pillow --quiet --no-warn-script-location
echo  Done.
echo.

REM ---- Setup database ----
echo  [2/3] Setting up database...
python manage.py migrate --run-syncdb >nul 2>&1

python manage.py shell -c "from apps.courses.models import Course; import sys; sys.exit(0 if Course.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo  Loading course data...
    python manage.py loaddata apps\courses\fixtures\initial_courses.json >nul 2>&1
    python manage.py loaddata apps\courses\fixtures\initial_users.json >nul 2>&1
    python manage.py loaddata apps\courses\fixtures\initial_learning.json >nul 2>&1
)
echo  Done.
echo.

REM ---- Start server ----
echo  [3/3] Starting server...
echo.
echo  ============================================
echo.
echo   Open your browser and go to:
echo.
echo      http://127.0.0.1:8000
echo.
echo   Student Login:
echo      Email:    student@arshith.com
echo      Password: student123
echo.
echo   Admin Login:
echo      Email:    admin@arshith.com
echo      Password: admin123
echo.
echo  ============================================
echo.
echo  Press CTRL+C to stop the server
echo.
python manage.py runserver
pause
