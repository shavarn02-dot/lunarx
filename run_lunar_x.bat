@echo off
setlocal enabledelayedexpansion
title ISRO LUNARX: Chandra-Sync Mission Control (SIH26166)

echo ======================================================================
echo       ISRO LUNARX - CHANDRA-SYNC REGISTRATION SYSTEM (SIH26166)
echo       Next.js UI (Port 3030) + Python Engine (Port 8000) + Tunnel
echo ======================================================================
echo.

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in your PATH!
    echo Please install Python 3.10+ or add it to your system environment variables.
    pause
    exit /b 1
)

:: [1/3] Start Python Backend
echo [1/3] Starting Python Registration Engine (Port 8000)...
start "LUNARX Engine (Port 8000)" cmd /k "title LUNARX Python Engine ^& python -m uvicorn app.api_server:app --port 8000 --host 127.0.0.1"

timeout /t 3 /nobreak >nul

:: [2/3] Start Cloudflare Tunnel (if cloudflared.exe exists)
if exist "cloudflared.exe" (
    echo [2/3] Starting Cloudflare Tunnel for Vercel connectivity...
    start "LUNARX Cloudflare Tunnel" cmd /k "title LUNARX Cloudflare Tunnel ^& .\cloudflared.exe tunnel --url http://127.0.0.1:8000"
) else (
    echo [2/3] cloudflared.exe not found in folder. Skipping tunnel.
)

timeout /t 2 /nobreak >nul

:: [3/3] Start Local Next.js UI
echo [3/3] Starting Local Next.js UI Server (Port 3030)...
start "LUNARX Local UI (Port 3030)" cmd /k "title LUNARX Next.js UI ^& cd lunar-x ^& npm run dev"

timeout /t 4 /nobreak >nul

:: Open local UI in browser
echo.
echo Launching LUNARX in browser...
start http://localhost:3030

echo.
echo ======================================================================
echo  LUNARX Mission Control is ACTIVE!
echo ----------------------------------------------------------------------
echo  - Local Web UI:      http://localhost:3030
echo  - Live Vercel App:   https://lunarx-pi.vercel.app
echo  - Backend API:       http://127.0.0.1:8000
echo  - API Documentation: http://127.0.0.1:8000/docs
echo ======================================================================
echo.
echo Keep all background command windows OPEN while using the application.
echo Press any key to close this launcher window (services keep running)...
pause >nul
