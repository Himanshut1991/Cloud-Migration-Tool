@echo off
echo ====================================
echo   Cloud Migration Tool - Frontend
echo ====================================
echo.
echo Starting React development server...
echo.
cd /d "%~dp0frontend"
npm run dev
echo.
echo Frontend server stopped.
pause
