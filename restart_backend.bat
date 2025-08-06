@echo off
echo Restarting backend...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 >nul
cd /d "C:\Users\2313274\Cloud Migration Tool\backend"
echo Starting real data backend...
python real_data_backend.py
