@echo off
echo Killing any existing Python processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo Starting minimal backend...
cd /d "c:\Users\2313274\Cloud Migration Tool\backend"
python minimal_resource_backend.py
