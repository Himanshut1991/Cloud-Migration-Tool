# PowerShell script to start both servers
Write-Host "================================================" -ForegroundColor Green
Write-Host "   CLOUD MIGRATION TOOL - MANUAL START" -ForegroundColor Green  
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Kill existing processes
Write-Host "Stopping existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

# Start Backend
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
$backendPath = "C:\Users\2313274\Cloud Migration Tool\backend"
Set-Location $backendPath

Start-Process -WindowStyle Normal -FilePath "C:\Program Files\Python313\python.exe" -ArgumentList "complete_backend.py"

Write-Host "Backend started - waiting 5 seconds..." -ForegroundColor Green
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
$frontendPath = "C:\Users\2313274\Cloud Migration Tool\frontend"
Set-Location $frontendPath

Start-Process -WindowStyle Normal -FilePath "npm" -ArgumentList "run", "dev"

Write-Host "Frontend started - waiting 10 seconds..." -ForegroundColor Green
Start-Sleep -Seconds 10

# Check if servers are running
Write-Host "Checking server status..." -ForegroundColor Yellow

$backend = netstat -ano | findstr ":5000"
$frontend = netstat -ano | findstr ":5173"

if ($backend) {
    Write-Host "✅ Backend: RUNNING on port 5000" -ForegroundColor Green
} else {
    Write-Host "❌ Backend: NOT RUNNING" -ForegroundColor Red
}

if ($frontend) {
    Write-Host "✅ Frontend: RUNNING on port 5173" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend: NOT RUNNING" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "   ACCESS APPLICATION" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Backend API:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
