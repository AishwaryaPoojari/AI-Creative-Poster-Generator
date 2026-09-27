@echo off
title ArtGen Studio Launcher
echo ========================================================
echo     ArtGen Studio - Generative AI & Creative Suite
echo ========================================================
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Launching Streamlit Web App...
streamlit run app.py
pause
