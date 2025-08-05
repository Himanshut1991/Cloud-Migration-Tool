@echo off
echo Starting Cloud Migration Tool - Complete Application
echo ====================================================
echo.

echo Step 1: Starting Backend Server...
cd /d "%~dp0backend"
start "Backend Server" cmd /k "python app.py"

echo Step 2: Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo Step 3: Starting Frontend Server...
cd /d "%~dp0frontend"
start "Frontend Server" cmd /k "npm run dev"

echo Step 4: Waiting for frontend to initialize...
timeout /t 5 /nobreak >nul

echo Step 5: Opening application in browser...
start http://localhost:3000

echo.
echo ====================================================
echo Cloud Migration Tool is now running!
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Navigate to Reports > Export Reports to test the export functionality
echo.
echo Press any key to close this window...
pause >nul
