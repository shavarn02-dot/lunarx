@echo off
setlocal enabledelayedexpansion
title ISRO LUNARX: Live Cloudflare Tunnel + Backend (SIH26166)

echo ======================================================================
echo       ISRO LUNARX - LIVE BACKEND + CLOUDFLARE TUNNEL (SIH26166)
echo       Powers the live Vercel deployment: https://lunarx-pi.vercel.app
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

:: [1/2] Start Python Registration Engine
echo [1/2] Starting Python Registration Engine (Port 8000)...
start "LUNARX Python Engine" cmd /k "title LUNARX Python Engine ^& python -m uvicorn app.api_server:app --port 8000 --host 127.0.0.1"

timeout /t 3 /nobreak >nul

:: [2/2] Start Cloudflare Tunnel
if exist "cloudflared.exe" (
    echo [2/2] Starting Cloudflare Tunnel...
    start "LUNARX Cloudflare Tunnel" cmd /k "title LUNARX Cloudflare Tunnel ^& .\cloudflared.exe tunnel --url http://127.0.0.1:8000"
) else (
    echo [ERROR] cloudflared.exe not found in this directory!
    echo Please make sure cloudflared.exe is located in the project root folder.
    pause
    exit /b 1
)

timeout /t 3 /nobreak >nul

:: Open live Vercel app in browser
echo.
echo Opening Live Vercel App in browser...
start https://lunarx-pi.vercel.app

echo.
echo ======================================================================
echo  LUNARX Live Cloud Connection is ACTIVE!
echo ----------------------------------------------------------------------
echo  - Live Vercel App:   https://lunarx-pi.vercel.app
echo  - Local Engine:      http://127.0.0.1:8000
echo  - Swagger API Docs:  http://127.0.0.1:8000/docs
echo ======================================================================
echo.
echo [IMPORTANT]
echo Keep the "LUNARX Python Engine" and "LUNARX Cloudflare Tunnel" windows OPEN.
echo Closing them will take the live registration service offline.
echo.
pause
