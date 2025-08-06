#!/usr/bin/env powershell
# Start both backend and frontend servers

Write-Host "Starting Cloud Migration Tool servers..." -ForegroundColor Green

# Kill existing processes
Write-Host "Stopping existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait a moment
Start-Sleep -Seconds 2

# Start backend
Write-Host "Starting backend server on port 5000..." -ForegroundColor Cyan
$backendPath = "c:\Users\2313274\Cloud Migration Tool\backend"
Set-Location $backendPath

# Start backend in background
Start-Process -FilePath "C:\Program Files\Python313\python.exe" -ArgumentList "complete_backend.py" -WindowStyle Minimized -PassThru

# Wait for backend to start
Start-Sleep -Seconds 5

# Start frontend
Write-Host "Starting frontend server on port 5173..." -ForegroundColor Cyan
$frontendPath = "c:\Users\2313274\Cloud Migration Tool\frontend"
Set-Location $frontendPath

# Start frontend in background
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Minimized -PassThru

Write-Host "Servers starting... Please wait 10 seconds then check:" -ForegroundColor Green
Write-Host "- Backend: http://localhost:5000/api/servers" -ForegroundColor White
Write-Host "- Frontend: http://localhost:5173" -ForegroundColor White

# Wait and check if servers are running
Start-Sleep -Seconds 10
Write-Host "Checking server status..." -ForegroundColor Yellow
netstat -ano | findstr :5000
netstat -ano | findstr :5173
