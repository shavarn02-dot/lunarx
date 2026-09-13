@echo off
title ISRO Lunar-X Live Backend + Cloudflare Tunnel (SIH26166)
echo ======================================================================
echo    ISRO Lunar-X: Live Backend Engine + Cloudflare Tunnel
echo ======================================================================
echo.

echo [1/2] Starting Python Registration Engine (Port 8000)...
start "Lunar-X Backend (Port 8000)" cmd /k "python -m uvicorn app.api_server:app --port 8000 --host 127.0.0.1"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Cloudflare Tunnel...
echo NOTE: Tunnel URL will be active as long as this window stays open.
start "Lunar-X Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel --url http://127.0.0.1:8000"

echo.
echo ======================================================================
echo Backend and Tunnel are now running!
echo Live Vercel Frontend: https://lunarx-pi.vercel.app
echo ======================================================================
pause
