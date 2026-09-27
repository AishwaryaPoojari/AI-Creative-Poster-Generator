@echo off
title ArtGen Studio Setup
echo ========================================================
echo     ArtGen Studio - Virtual Environment Setup
echo ========================================================
echo Step 1: Creating Python virtual environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creating virtual environment. Please ensure Python is installed and added to PATH.
    pause
    exit /b %errorlevel%
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing required dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies.
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo Setup complete! You can now run the project with: run.bat
echo ========================================================
pause
