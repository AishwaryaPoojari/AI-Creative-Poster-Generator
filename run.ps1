# PowerShell Launcher for ArtGen Studio
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "    ArtGen Studio - Generative AI & Creative Suite      " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Launching Streamlit Web App using project virtual environment..." -ForegroundColor Yellow

& ".\venv\Scripts\python.exe" -m streamlit run app.py
