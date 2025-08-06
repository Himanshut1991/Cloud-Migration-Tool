@echo off
echo ============================================
echo    Cloud Migration Tool - Complete Startup
echo ============================================
echo.

echo [1/3] Starting Backend Server...
cd /d "%~dp0\backend"
start "Complete Backend" cmd /k "C:\Program Files\Python313\python.exe complete_backend.py"
echo Backend starting at http://localhost:5000
echo.

echo [2/3] Waiting for backend to initialize...
timeout /t 8 /nobreak > nul

echo [3/3] Starting Frontend Server...
cd /d "%~dp0\frontend"
start "Frontend Server" cmd /k "npm run dev"
echo Frontend starting at http://localhost:5173
echo.

echo ============================================
echo    Both servers are starting up...
echo    
echo    Backend API: http://localhost:5000
echo    Frontend:    http://localhost:5173
echo    
echo    Wait 10 seconds then navigate to:
echo    http://localhost:5173
echo ============================================
echo.

echo Opening application in browser...
timeout /t 12 /nobreak > nul
start http://localhost:5173

echo.
echo Both servers should now be running.
echo Check the opened windows for any errors.
pause
