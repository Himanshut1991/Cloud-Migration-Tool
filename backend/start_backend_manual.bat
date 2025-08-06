@echo off
echo Starting Cloud Migration Tool Backend
cd /d "c:\Users\2313274\Cloud Migration Tool\backend"

echo Checking Python...
"C:\Program Files\Python313\python.exe" --version

echo Starting server...
"C:\Program Files\Python313\python.exe" complete_backend.py

pause
