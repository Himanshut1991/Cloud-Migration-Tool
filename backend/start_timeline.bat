@echo off
echo Starting Timeline Backend Server...
cd /d "%~dp0"

echo Stopping any existing Python processes...
taskkill /f /im python.exe 2>nul

echo Starting timeline server...
python timeline_server.py

pause
