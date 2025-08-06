@echo off
setlocal enabledelayedexpansion

echo ============================================
echo    Cloud Migration Tool - FORCE START
echo ============================================
echo.

REM Test Python installation first
echo [1/5] Testing Python installation...
"C:\Program Files\Python313\python.exe" --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Python not found at expected location
    echo Please check Python installation
    pause
    exit /b 1
)
echo ✅ Python found

REM Kill existing processes
echo [2/5] Stopping existing processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo ✅ Processes stopped

REM Test environment
echo [3/5] Testing Python environment...
cd /d "%~dp0\backend"
"C:\Program Files\Python313\python.exe" test_environment.py

REM Start backend
echo [4/5] Starting backend server...
start "Backend Server" cmd /k ""C:\Program Files\Python313\python.exe" complete_backend.py"
echo ✅ Backend process started

REM Wait for backend
echo Waiting for backend to start...
timeout /t 10 /nobreak >nul

REM Start frontend  
echo [5/5] Starting frontend server...
cd /d "%~dp0\frontend"
start "Frontend Server" cmd /k "npm run dev"
echo ✅ Frontend process started

echo.
echo ============================================
echo    STARTUP COMPLETE
echo ============================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Wait 15-20 seconds for both servers to fully start
echo Then navigate to: http://localhost:5173
echo.

REM Wait and check ports
echo Checking server status in 15 seconds...
timeout /t 15 /nobreak >nul

echo.
echo Server Status:
netstat -ano | findstr ":5000" >nul && echo ✅ Backend running on port 5000 || echo ❌ Backend NOT running
netstat -ano | findstr ":5173" >nul && echo ✅ Frontend running on port 5173 || echo ❌ Frontend NOT running

echo.
echo Opening browser...
start http://localhost:5173

pause
