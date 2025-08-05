#!/usr/bin/env powershell
Write-Host "Starting Frontend Server..." -ForegroundColor Green

Set-Location "c:\Users\2313274\Cloud Migration Tool\frontend"
Write-Host "Changed to directory: $(Get-Location)" -ForegroundColor Yellow

Write-Host "Starting npm dev server..." -ForegroundColor Green
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -NoNewWindow -Wait
