# 🌐 KT Planner Web Interface

A modern, responsive web application for managing Knowledge Transfer sessions with an intuitive graphical interface.

## ✨ Features

### 📊 Dashboard
- Real-time statistics and metrics
- Progress tracking
- Completion rates
- Attendance analytics

### 📝 Session Management
- Create, view, edit, and delete sessions
- Comprehensive session details
- Status tracking (Planned, In Progress, Completed)
- Priority management

### 📅 Smart Scheduling
- Auto-schedule multiple sessions
- Weekend avoidance
- Buffer time management
- Time preference support

### 🔔 Reminders
- 1 day before notifications
- 1 hour before alerts
- Pending reminders dashboard

### 🤖 AI-Powered Tools
- Topic breakdown into subtopics
- Automatic agenda generation
- Smart session planning

## 🚀 Quick Start

### Windows

```bash
# Double-click or run:
run_web.bat
```

### Linux/Mac

```bash
# Make executable and run:
chmod +x run_web.sh
./run_web.sh
```

### Manual Start

```bash
# Install dependencies
pip install flask flask-cors

# Run the server
python web_app.py
```

## 🌍 Access

Once running, open your browser and go to:
- **http://localhost:5000**

## 📱 Interface Overview

### Navigation Tabs

1. **📊 Dashboard** - Overview and statistics
2. **📝 Sessions** - View and manage all sessions
3. **➕ Create Session** - Add new KT sessions
4. **📅 Auto Schedule** - Bulk session scheduling
5. **🔔 Reminders** - Pending notifications
6. **🤖 AI Tools** - Topic breakdown and agenda generation

## 🎯 Usage Examples

### Creating a Session

1. Click "➕ Create Session"
2. Fill in:
   - Title: "Python Advanced Concepts"
   - Trainer: "John Doe"
   - Date & Time: Select from calendar
   - Duration: 2 hours
   - Topics: "Decorators, Generators, Context Managers"
3. Click "Create Session"

### Auto-Scheduling

1. Go to "📅 Auto Schedule"
2. Enter topics (one per line):
   ```
   Python Basics
   Object-Oriented Programming
   Web Development with Flask
   Database Integration
   Testing and Debugging
   ```
3. Set trainer, participants, date range
4. Click "Schedule All Sessions"

### Using AI Tools

**Topic Breakdown:**
- Enter: "Machine Learning"
- Get: 5 structured subtopics

**Generate Agenda:**
- Select a session
- Get detailed agenda with timing

## 🎨 Features Highlights

### Responsive Design
- ✅ Desktop optimized
- ✅ Tablet friendly
- ✅ Mobile compatible

### Visual Indicators
- 🟡 Planned sessions
- 🔵 In Progress
- 🟢 Completed
- Color-coded priorities

### Real-time Updates
- Instant dashboard refresh
- Live session updates
- Automatic data sync

## 🔧 API Endpoints

The web interface uses REST API:

```
GET    /api/sessions           - List all sessions
POST   /api/sessions           - Create session
GET    /api/sessions/<id>      - Get session details
PUT    /api/sessions/<id>      - Update session
DELETE /api/sessions/<id>      - Delete session
POST   /api/schedule           - Auto-schedule
GET    /api/reminders          - Get reminders
GET    /api/progress           - Get statistics
POST   /api/ai/breakdown       - Break down topic
POST   /api/ai/agenda          - Generate agenda
```

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Use different port
python web_app.py --port 5001
```

### Flask Not Found

```bash
pip install --upgrade flask flask-cors
```

### Data Not Loading

1. Check `kt_sessions.json` exists
2. Verify JSON format is valid
3. Check browser console (F12)

## 📚 Documentation

- **Full Guide**: See `WEB_INTERFACE_GUIDE.md`
- **CLI Usage**: See main `README.md`
- **Installation**: See `INSTALLATION.md`

## 🔒 Security Note

This is a development server for local use. For production:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## 💡 Tips

1. **Use descriptive titles** for easy identification
2. **Set priorities** to focus on critical sessions
3. **Add participants** for better tracking
4. **Update status** regularly
5. **Use auto-schedule** for efficiency

## 🆘 Support

- Check terminal logs for errors
- Use browser console (F12) for debugging
- Refer to `WEB_INTERFACE_GUIDE.md` for detailed help

## 🎉 Enjoy!

You now have a powerful web interface for managing your KT sessions!

---

**Made with ❤️ using Flask + Vanilla JavaScript**