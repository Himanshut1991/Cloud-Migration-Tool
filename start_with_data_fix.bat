@echo off
echo Cloud Migration Tool - Startup & Data Fix
echo ==========================================
echo.

echo Step 1: Setting up environment...
cd /d "%~dp0backend"

echo Step 2: Populating database with sample data...
python populate_full_data.py
if %errorlevel% neq 0 (
    echo Error populating data! Check the output above.
    pause
    exit /b 1
)

echo Step 3: Starting backend server...
start "Backend Server" cmd /k "echo Starting backend... && python app.py"

echo Step 4: Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo Step 5: Testing backend connection...
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorlevel% neq 0 (
    echo Backend may not be responding yet. Continuing anyway...
)

echo Step 6: Starting frontend server...
cd /d "%~dp0frontend"
start "Frontend Server" cmd /k "echo Starting frontend... && npm run dev"

echo Step 7: Waiting for frontend to start...
timeout /t 8 /nobreak >nul

echo Step 8: Opening application...
start http://localhost:3000

echo.
echo ==========================================
echo Setup Complete!
echo.
echo If you see "failed to fetch" messages:
echo 1. Wait a moment for servers to fully start
echo 2. Refresh the browser page
echo 3. Check that both terminal windows are running
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
