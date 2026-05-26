@echo off
echo ========================================
echo   KT Planner Web Interface Launcher
echo ========================================
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask is not installed. Installing now...
    pip install flask flask-cors
    echo.
)

echo Starting KT Planner Web Server...
echo.
echo The web interface will be available at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python web_app.py

@REM Made with Bob
