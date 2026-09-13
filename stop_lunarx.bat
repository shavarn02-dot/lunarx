@echo off
title Stop LUNARX Services (SIH26166)

echo ======================================================================
echo       STOPPING ALL LUNARX BACKGROUND SERVICES
echo ======================================================================
echo.

echo Stopping cloudflared tunnel...
taskkill /F /IM cloudflared.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Cloudflare Tunnel stopped.
) else (
    echo [INFO] Cloudflare Tunnel was not running.
)

echo.
echo Stopping Python uvicorn backend on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo [OK] Killed process PID %%a on port 8000.
)

echo.
echo ======================================================================
echo  All LUNARX background services have been stopped cleanly.
echo ======================================================================
timeout /t 3
