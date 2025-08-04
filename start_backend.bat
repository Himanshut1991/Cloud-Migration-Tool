@echo off
echo ====================================
echo   Cloud Migration Tool - Backend
echo ====================================
echo.
echo Starting Python Flask backend server...
echo.
cd /d "%~dp0backend"
python app.py
echo.
echo Backend server stopped.
pause
