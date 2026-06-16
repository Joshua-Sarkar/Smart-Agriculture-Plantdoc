@echo off
title PlantDoc - Starting Servers...
echo.
echo  =============================================
echo   PLANTDOC - Plant Disease Detection System
echo  =============================================
echo.
echo  Starting Backend (FastAPI)...
start "PlantDoc Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo  Starting Frontend (Vite)...
start "PlantDoc Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 4 /nobreak >nul

echo.
echo  Both servers are starting...
echo.
echo  Frontend:  http://localhost:5173
echo  Backend:   http://localhost:8000
echo  API Docs:  http://localhost:8000/docs
echo.
echo  Opening browser...
start "" "http://localhost:5173"

echo.
echo  Press any key to close this window.
pause >nul
