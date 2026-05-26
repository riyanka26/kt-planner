#!/bin/bash

echo "========================================"
echo "  KT Planner Web Interface Launcher"
echo "========================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Flask is not installed. Installing now..."
    pip3 install flask flask-cors
    echo ""
fi

echo "Starting KT Planner Web Server..."
echo ""
echo "The web interface will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python3 web_app.py

# Made with Bob
