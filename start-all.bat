@echo off
echo ========================================
echo   GarudaRush - Starting Both Servers
echo ========================================
echo.

echo Starting Backend Server in new window...
start "GarudaRush Backend" cmd /k "cd backend && venv\Scripts\activate && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server in new window...
start "GarudaRush Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   Both servers are starting!
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this window...
echo (The server windows will stay open)
pause >nul
