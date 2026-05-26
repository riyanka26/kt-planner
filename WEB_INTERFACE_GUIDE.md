# KT Planner Web Interface Guide

## 🌐 Overview

The KT Planner now includes a modern, responsive web interface built with Flask (Python backend) and vanilla JavaScript (frontend). This provides an intuitive graphical interface for managing your knowledge transfer sessions.

## 📋 Features

### Dashboard
- **Real-time Statistics**: View total sessions, completion rates, attendance metrics
- **Progress Summary**: Track completed, in-progress, and pending sessions
- **Document Management**: Monitor uploaded documents across all sessions

### Session Management
- **View All Sessions**: Browse all KT sessions with filtering options
- **Create Sessions**: Easy-to-use form for creating new sessions
- **Session Details**: View comprehensive information about each session
- **Delete Sessions**: Remove sessions you no longer need

### Auto Scheduling
- **Bulk Session Creation**: Schedule multiple sessions at once
- **Smart Scheduling**: Automatically avoids weekends
- **Time Preferences**: Set preferred time slots for sessions
- **Buffer Management**: Automatic spacing between sessions

### Reminders
- **Pending Reminders**: View all upcoming session reminders
- **1 Day Before**: Get notified 24 hours before sessions
- **1 Hour Before**: Last-minute reminders before sessions start

### AI Tools
- **Topic Breakdown**: Break complex topics into manageable subtopics
- **Agenda Generation**: Auto-generate detailed session agendas
- **Smart Suggestions**: AI-powered recommendations for session planning

## 🚀 Installation

### Step 1: Install Dependencies

```bash
# Navigate to KTPlanner directory
cd KTPlanner

# Install Flask and dependencies
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
# Check Flask installation
python -c "import flask; print(flask.__version__)"
```

## ▶️ Running the Web Interface

### Method 1: Direct Python Execution

```bash
# From KTPlanner directory
python web_app.py
```

### Method 2: Using Flask Command

```bash
# Set Flask app environment variable
set FLASK_APP=web_app.py

# Run Flask
flask run
```

### Method 3: Development Mode (with auto-reload)

```bash
# Set Flask to development mode
set FLASK_ENV=development
set FLASK_APP=web_app.py

# Run Flask
flask run
```

## 🌍 Accessing the Interface

Once the server is running, you'll see output like:

```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

Open your web browser and navigate to:
- **http://localhost:5000** or
- **http://127.0.0.1:5000**

## 📱 Using the Web Interface

### Creating Your First Session

1. Click on the **"➕ Create Session"** tab
2. Fill in the required fields:
   - **Session Title**: Name of your KT session
   - **Trainer**: Person conducting the session
   - **Scheduled Date & Time**: When the session will occur
   - **Duration**: How long the session will last (in hours)
   - **Topics**: Comma-separated list of topics to cover
3. Optional fields:
   - Description, Trainee, Priority, Time Preference, Participants
4. Click **"Create Session"**

### Auto-Scheduling Multiple Sessions

1. Go to **"📅 Auto Schedule"** tab
2. Enter topics (one per line)
3. Specify trainer and participants
4. Set date range (start and end dates)
5. Choose duration per session
6. Click **"Schedule All Sessions"**

The system will:
- ✅ Skip weekends automatically
- ✅ Add buffer time between sessions
- ✅ Respect your time preferences
- ✅ Create all sessions in one go

### Viewing Session Details

1. Go to **"📝 Sessions"** tab
2. Click **"View Details"** on any session card
3. A modal will show:
   - Complete session information
   - Topics covered
   - Participants list
   - Attached documents
   - Attendance records

### Using AI Tools

#### Topic Breakdown
1. Go to **"🤖 AI Tools"** tab
2. Enter a complex topic (e.g., "Machine Learning")
3. Choose number of subtopics (2-8)
4. Click **"Generate Subtopics"**
5. Get a structured breakdown of the topic

#### Generate Agenda
1. Select a session from the dropdown
2. Click **"Generate Agenda"**
3. Get a detailed session agenda including:
   - Session objectives
   - Topics to cover
   - Prerequisites
   - Materials needed
   - Time breakdown

## 🎨 Interface Features

### Responsive Design
- ✅ Works on desktop, tablet, and mobile devices
- ✅ Adaptive layouts for different screen sizes
- ✅ Touch-friendly buttons and controls

### Visual Indicators
- **Status Colors**:
  - 🟡 Yellow: Planned
  - 🔵 Blue: In Progress
  - 🟢 Green: Completed
- **Priority Badges**: Low, Medium, High, Critical
- **Topic Tags**: Color-coded topic indicators
- **Participant Tags**: Visual participant lists

### Real-time Updates
- Dashboard statistics update automatically
- Session list refreshes after changes
- Instant feedback on all actions

## 🔧 API Endpoints

The web interface uses these REST API endpoints:

### Sessions
- `GET /api/sessions` - List all sessions
- `POST /api/sessions` - Create new session
- `GET /api/sessions/<id>` - Get session details
- `PUT /api/sessions/<id>` - Update session
- `DELETE /api/sessions/<id>` - Delete session

### Attendance & Documents
- `POST /api/sessions/<id>/attendance` - Record attendance
- `POST /api/sessions/<id>/documents` - Add document

### Analytics
- `GET /api/reminders` - Get pending reminders
- `GET /api/progress` - Get progress summary

### Scheduling
- `POST /api/schedule` - Auto-schedule sessions

### AI Features
- `POST /api/ai/breakdown` - Break down topic
- `POST /api/ai/agenda` - Generate agenda

## 🛠️ Troubleshooting

### Port Already in Use

If port 5000 is already in use:

```bash
# Use a different port
flask run --port 5001
```

Then access at: http://localhost:5001

### Flask Not Found

```bash
# Reinstall Flask
pip install --upgrade flask flask-cors
```

### CORS Errors

The app includes CORS support. If you still face issues:

```python
# In web_app.py, CORS is already configured:
CORS(app)
```

### Data Not Loading

1. Check if `kt_sessions.json` exists in the KTPlanner directory
2. Verify the file has valid JSON format
3. Check browser console for errors (F12)

## 🔒 Security Notes

### Development Server Warning

The Flask development server is **NOT suitable for production**. It's designed for:
- ✅ Local development
- ✅ Testing
- ✅ Personal use

For production deployment, use:
- **Gunicorn** (Linux/Mac)
- **Waitress** (Windows)
- **uWSGI**

### Production Deployment Example

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## 📊 Performance Tips

### For Large Datasets

If you have many sessions (100+):

1. **Pagination**: Consider adding pagination to session lists
2. **Filtering**: Use status/priority filters to narrow results
3. **Search**: Implement search functionality
4. **Caching**: Add caching for frequently accessed data

### Browser Compatibility

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## 🎯 Best Practices

### Session Management
1. **Use descriptive titles**: Make sessions easy to identify
2. **Add participants**: Track who needs to attend
3. **Set priorities**: Focus on critical sessions first
4. **Update status**: Keep session status current

### Scheduling
1. **Plan ahead**: Use auto-scheduling for better organization
2. **Set realistic durations**: Don't overbook sessions
3. **Add buffer time**: Allow breaks between sessions
4. **Check conflicts**: Review schedule before finalizing

### Documentation
1. **Add descriptions**: Explain session objectives
2. **List prerequisites**: Help participants prepare
3. **Attach materials**: Link to relevant documents
4. **Take notes**: Record key points during sessions

## 🆘 Getting Help

### Check Logs

The Flask server logs appear in your terminal. Look for:
- Error messages
- Request details
- Response codes

### Browser Console

Press F12 in your browser to:
- View JavaScript errors
- Check network requests
- Debug API calls

### Common Issues

**Issue**: Sessions not appearing
**Solution**: Refresh the page, check `kt_sessions.json` exists

**Issue**: Can't create session
**Solution**: Verify all required fields are filled

**Issue**: Agenda not generating
**Solution**: Ensure session has topics defined

## 🔄 Updates and Maintenance

### Updating the Interface

To update the web interface:

1. Pull latest changes from repository
2. Restart the Flask server
3. Clear browser cache (Ctrl+F5)

### Backup Your Data

Regularly backup `kt_sessions.json`:

```bash
# Create backup
copy kt_sessions.json kt_sessions_backup.json

# Or with timestamp
copy kt_sessions.json kt_sessions_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json
```

## 🎉 Enjoy!

You now have a fully functional web interface for managing your KT sessions. The interface combines the power of the CLI with the convenience of a modern web application.

For CLI usage, refer to the main README.md and other documentation files.

---

**Made with ❤️ for efficient Knowledge Transfer management**