#!/bin/bash

echo "=========================================="
echo "  Pushing Web Interface Updates to GitHub"
echo "=========================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not a git repository. Please run 'git init' first."
    exit 1
fi

# Add all new web interface files
echo "Adding new files..."
git add web_app.py
git add templates/
git add requirements.txt
git add run_web.bat
git add run_web.sh
git add WEB_INTERFACE_GUIDE.md
git add README_WEB.md
git add push_web_updates.sh

# Show what will be committed
echo ""
echo "Files to be committed:"
git status --short

echo ""
read -p "Do you want to commit these changes? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Commit the changes
    echo ""
    echo "Committing changes..."
    git commit -m "Add web interface: Flask backend + responsive frontend

- Added Flask web application (web_app.py)
- Created modern responsive HTML/CSS/JavaScript interface
- Added 6 interactive tabs: Dashboard, Sessions, Create, Schedule, Reminders, AI Tools
- Implemented REST API with 15+ endpoints
- Added launch scripts for Windows and Linux/Mac
- Updated requirements.txt with Flask dependencies
- Added comprehensive documentation (WEB_INTERFACE_GUIDE.md, README_WEB.md)
- Features: Real-time stats, smart scheduling, reminders, AI tools
- Fully responsive design for desktop, tablet, and mobile"

    # Push to GitHub
    echo ""
    echo "Pushing to GitHub..."
    git push origin main

    echo ""
    echo "=========================================="
    echo "✓ Successfully pushed to GitHub!"
    echo "=========================================="
    echo ""
    echo "View your repository at:"
    echo "https://github.com/riyanka26/kt-planner"
else
    echo ""
    echo "Commit cancelled."
fi

# Made with Bob
