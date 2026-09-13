@echo off
title ISRO CHANDRA-SYNC Mission Control (SIH26166)
echo ======================================================================
echo    ISRO CHANDRA-SYNC: Chandrayaan-2 Lunar Registration System
echo    Next.js UI (Port 3030) ^& Python FastAPI Engine (Port 8000)
echo ======================================================================
echo.

echo [1/2] Starting Python Registration API Engine (Port 8000)...
start "CHANDRA-SYNC Engine (Port 8000)" cmd /k "python -m uvicorn app.api_server:app --port 8000 --host 127.0.0.1"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Next.js UI Server (Port 3030)...
start "CHANDRA-SYNC UI (Port 3030)" cmd /k "cd lunar-x && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo Opening CHANDRA-SYNC Mission Control in browser...
start http://localhost:3030

echo.
echo ======================================================================
echo System is running!
echo - Web UI:  http://localhost:3030
echo - API Docs: http://127.0.0.1:8000/docs
echo ======================================================================
pause
