# KT Planner - Enhanced Features Guide

## Overview
This guide covers all the advanced features added to the KT Planner, including interactive scheduling, reminders, attendance tracking, document management, and AI-assisted planning.

---

## Table of Contents
1. [Interactive Wizard](#interactive-wizard)
2. [Smart Scheduling](#smart-scheduling)
3. [Reminder System](#reminder-system)
4. [Attendance Tracking](#attendance-tracking)
5. [Document Management](#document-management)
6. [Progress Dashboard](#progress-dashboard)
7. [AI-Assisted Features](#ai-assisted-features)
8. [Enhanced CLI Commands](#enhanced-cli-commands)

---

## Interactive Wizard

### Launch the Wizard
```bash
python kt_wizard.py
```

### What the Wizard Collects

The wizard guides you through creating a complete KT plan by collecting:

1. **KT Topics**
   - Enter topics manually
   - Or break down a high-level topic into subtopics automatically
   - Example: "Python Programming" → 5 subtopics

2. **Presenter Name(s)**
   - Single presenter for all sessions
   - Or assign different presenters to each topic

3. **Participant List**
   - Names of all attendees
   - Can be modified later

4. **Preferred Date Range**
   - Start date (YYYY-MM-DD)
   - End date (YYYY-MM-DD)
   - Automatically skips weekends

5. **Session Duration**
   - 30 minutes
   - 1 hour
   - 2 hours
   - Custom duration

6. **Time Preferences**
   - Specific time slots (e.g., "3 PM - 5 PM")
   - Or flexible scheduling

7. **Sessions Per Day**
   - How many sessions to schedule per day
   - Default: 1 session per day

### Example Wizard Session

```
============================================================
  KT Planner Interactive Wizard
============================================================

Welcome! This wizard will help you create a comprehensive KT plan.

============================================================
  Step 1: KT Topics
============================================================

Do you want to break down a high-level topic? (yes/no) [no]: yes
Enter the high-level topic: Python Advanced Concepts
How many subtopics? [5]: 5

Generated 5 subtopics:
  1. Python Advanced Concepts - Introduction and Basics
  2. Python Advanced Concepts - Core Concepts
  3. Python Advanced Concepts - Advanced Features
  4. Python Advanced Concepts - Best Practices
  5. Python Advanced Concepts - Real-world Applications

[SUCCESS] Collected 5 topics

============================================================
  Step 2: Presenter(s)
============================================================

Is there a single presenter for all sessions? (yes/no) [yes]: yes
Enter presenter name: Alice Smith

[SUCCESS] Assigned presenters

... (continues through all steps)
```

---

## Smart Scheduling

### Automatic Scheduling Rules

The planner automatically applies these rules:

1. **Weekend Avoidance**
   - Skips Saturdays and Sundays
   - Moves sessions to next weekday

2. **Session Distribution**
   - Spreads sessions evenly across date range
   - Respects sessions-per-day limit

3. **Buffer Time**
   - 2-hour buffer between sessions on same day
   - Prevents scheduling conflicts

4. **Time Preferences**
   - Honors specified time slots
   - Falls back to 2 PM if not specified

5. **Date Range Validation**
   - Warns if not enough days for all sessions
   - Suggests alternate dates

### Programmatic Scheduling

```python
from kt_planner import KTPlanner

planner = KTPlanner()

sessions = planner.schedule_sessions(
    topics=["Topic 1", "Topic 2", "Topic 3"],
    trainer="Alice Smith",
    participants=["Bob", "Carol", "David"],
    start_date="2026-06-01",
    end_date="2026-06-15",
    duration_hours=2.0,
    time_preference="3 PM - 5 PM",
    sessions_per_day=1,
    buffer_hours=2
)

print(f"Scheduled {len(sessions)} sessions")
```

---

## Reminder System

### Setup Reminders

Reminders are automatically set up during wizard, or manually:

```python
# Setup reminders for a session
planner.setup_reminders("KT-0001")
```

### Reminder Types

1. **1 Day Before**
   - Sent 24 hours before session
   - Gives participants time to prepare

2. **1 Hour Before**
   - Sent 60 minutes before session
   - Last-minute reminder

### Check Pending Reminders

```bash
python kt_cli_enhanced.py check-reminders
```

Output:
```
=== Pending Reminders (2) ===

[1 Day Before]
  Session: KT-0001 - Python Advanced Concepts
  Scheduled: 2026-06-01 14:00
  Message: Reminder: KT session 'Python Advanced Concepts' is scheduled for tomorrow

[1 Hour Before]
  Session: KT-0002 - Database Design
  Scheduled: 2026-06-02 14:00
  Message: Reminder: KT session 'Database Design' starts in 1 hour
```

### Programmatic Access

```python
reminders = planner.get_pending_reminders()

for reminder in reminders:
    send_email(
        to=session.participants,
        subject=f"KT Reminder: {reminder['session_title']}",
        body=reminder['message']
    )
    
    # Mark as sent
    session = planner.get_session(reminder['session_id'])
    session.mark_reminder_sent(reminder['reminder_type'])
    planner.save_sessions()
```

---

## Attendance Tracking

### Record Attendance (Interactive)

```bash
python kt_cli_enhanced.py record-attendance KT-0001
```

Interactive prompt:
```
=== Record Attendance for KT-0001 ===

Session: Python Advanced Concepts
Participants: Bob, Carol, David

Enter names of attendees (one per line, empty line to finish):
  Attended: Bob
  Attended: Carol
  Attended: 

Enter names of those who missed (one per line, empty line to finish):
  Missed: David
  Missed: 

Any follow-up needed? (optional): Schedule makeup session for David

[SUCCESS] Attendance recorded for KT-0001
  Attended: 2
  Missed: 1
  Follow-up: Schedule makeup session for David
```

### Programmatic Recording

```python
session = planner.get_session("KT-0001")
session.record_attendance(
    attended=["Bob", "Carol"],
    missed=["David"],
    follow_up="Schedule makeup session for David"
)
planner.save_sessions()
```

### View Attendance in Session Details

```bash
python kt_cli_enhanced.py view KT-0001
```

---

## Document Management

### Add Documents to Session

```bash
python kt_cli_enhanced.py add-document KT-0001 "Session Slides" "https://example.com/slides.pdf" --description "Main presentation slides"
```

### Show Session Documents

```bash
python kt_cli_enhanced.py show-documents KT-0001
```

Output:
```
=== Documents for KT-0001 ===

1. Session Slides
   URL: https://example.com/slides.pdf
   Description: Main presentation slides
   Uploaded: 2026-05-25 14:30:00

2. Code Examples
   URL: https://github.com/example/repo
   Description: Sample code repository
   Uploaded: 2026-05-25 15:00:00
```

### Programmatic Document Management

```python
session = planner.get_session("KT-0001")

# Add document
session.add_document(
    name="Session Slides",
    url="https://example.com/slides.pdf",
    description="Main presentation slides"
)

# Access documents
for doc in session.documents:
    print(f"{doc['name']}: {doc['url']}")
```

---

## Progress Dashboard

### View Comprehensive Progress

```bash
python kt_cli_enhanced.py progress-summary
```

Output:
```
=== KT Progress Summary ===

Total Sessions: 10
Completed: 3 (30.0%)
In Progress: 2
Pending: 5

Documents Uploaded: 15
Sessions with Documents: 8

Total Attendance: 45
Total Missed: 5
Attendance Rate: 90.0%
```

### Programmatic Access

```python
summary = planner.get_progress_summary()

print(f"Completion Rate: {summary['completion_rate']}%")
print(f"Attendance Rate: {summary['attendance_rate']}%")
print(f"Documents: {summary['total_documents']}")
```

### Track Progress Over Time

```python
# Get statistics at different points
stats_week1 = planner.get_statistics()
# ... time passes ...
stats_week2 = planner.get_statistics()

improvement = stats_week2['average_completion'] - stats_week1['average_completion']
print(f"Progress improved by {improvement}%")
```

---

## AI-Assisted Features

### Topic Breakdown

Automatically break down high-level topics into subtopics:

```bash
python kt_cli_enhanced.py breakdown-topic "Machine Learning" --num 6
```

Output:
```
=== Topic Breakdown: Machine Learning ===

1. Machine Learning - Introduction and Basics
2. Machine Learning - Core Concepts
3. Machine Learning - Advanced Features
4. Machine Learning - Best Practices
5. Machine Learning - Real-world Applications
6. Machine Learning - Common Pitfalls and Solutions
```

### Agenda Generation

Generate structured agendas for sessions:

```bash
python kt_cli_enhanced.py generate-agenda KT-0001
```

Output:
```
KT SESSION AGENDA
================

Session ID: KT-0001
Title: Python Advanced Concepts
Date: 2026-06-01 14:00
Duration: 2.0 hours
Trainer: Alice Smith
Participants: Bob, Carol, David

OBJECTIVES
----------
Deep dive into advanced Python concepts

TOPICS TO COVER
---------------
1. Decorators
2. Generators
3. Context Managers

PREREQUISITES
-------------
• Basic Python
• OOP Concepts

MATERIALS NEEDED
----------------
• Python Documentation
• Code Examples

SESSION STRUCTURE
-----------------
• Introduction (10 mins)
• Main Content (90 mins)
• Q&A and Wrap-up (20 mins)
```

### Programmatic Usage

```python
# Break down topic
subtopics = planner.break_down_topic("Data Science", num_subtopics=5)

# Generate agenda
agenda = planner.generate_agenda("KT-0001")
print(agenda)

# Save agenda to file
with open(f"agenda_{session_id}.txt", 'w') as f:
    f.write(agenda)
```

---

## Enhanced CLI Commands

### Complete Command Reference

#### Session Management
```bash
# Create session (interactive)
python kt_cli_enhanced.py create

# List sessions with filters
python kt_cli_enhanced.py list
python kt_cli_enhanced.py list --status "In Progress"
python kt_cli_enhanced.py list --priority "High"
python kt_cli_enhanced.py list --trainer "Alice"

# View session details
python kt_cli_enhanced.py view KT-0001

# Update status
python kt_cli_enhanced.py status KT-0001 "In Progress"

# Update progress
python kt_cli_enhanced.py progress KT-0001 75

# Add notes
python kt_cli_enhanced.py note KT-0001 "Great session, covered all topics"

# Delete session
python kt_cli_enhanced.py delete KT-0001
```

#### Scheduling & Planning
```bash
# Launch wizard
python kt_wizard.py

# View upcoming sessions
python kt_cli_enhanced.py upcoming
python kt_cli_enhanced.py upcoming --days 14

# View overdue sessions
python kt_cli_enhanced.py overdue
```

#### Attendance & Documents
```bash
# Record attendance
python kt_cli_enhanced.py record-attendance KT-0001

# Add document
python kt_cli_enhanced.py add-document KT-0001 "Slides" "https://example.com/slides.pdf"

# Show documents
python kt_cli_enhanced.py show-documents KT-0001
```

#### Monitoring & Reporting
```bash
# Check reminders
python kt_cli_enhanced.py check-reminders

# View statistics
python kt_cli_enhanced.py stats

# View progress summary
python kt_cli_enhanced.py progress-summary
```

#### AI Features
```bash
# Break down topic
python kt_cli_enhanced.py breakdown-topic "Cloud Computing" --num 5

# Generate agenda
python kt_cli_enhanced.py generate-agenda KT-0001
```

---

## Best Practices

### 1. Planning Phase
- Use the wizard for initial setup
- Break down complex topics into manageable subtopics
- Allow buffer time between sessions
- Consider participant availability

### 2. Execution Phase
- Set up reminders for all sessions
- Generate agendas before each session
- Record attendance immediately after sessions
- Upload materials promptly

### 3. Tracking Phase
- Check progress summary weekly
- Review pending reminders daily
- Follow up on missed attendees
- Document lessons learned

### 4. Completion Phase
- Ensure all documents are uploaded
- Verify attendance records
- Generate final reports
- Archive session materials

---

## Integration Examples

### Email Integration

```python
import smtplib
from email.mime.text import MIMEText

def send_reminder_emails(planner):
    reminders = planner.get_pending_reminders()
    
    for reminder in reminders:
        session = planner.get_session(reminder['session_id'])
        
        msg = MIMEText(reminder['message'])
        msg['Subject'] = f"KT Reminder: {session.title}"
        msg['From'] = "kt-planner@example.com"
        msg['To'] = ", ".join(session.participants)
        
        # Send email (configure SMTP settings)
        # smtp.send_message(msg)
        
        # Mark as sent
        session.mark_reminder_sent(reminder['reminder_type'])
        planner.save_sessions()
```

### Calendar Integration

```python
from icalendar import Calendar, Event

def export_to_calendar(planner):
    cal = Calendar()
    
    for session in planner.list_sessions():
        event = Event()
        event.add('summary', session.title)
        event.add('dtstart', datetime.fromisoformat(session.scheduled_date))
        event.add('duration', timedelta(hours=session.duration_hours))
        event.add('description', session.description)
        cal.add_component(event)
    
    with open('kt_sessions.ics', 'wb') as f:
        f.write(cal.to_ical())
```

### Slack Integration

```python
import requests

def post_to_slack(webhook_url, session):
    message = {
        "text": f"KT Session Reminder: {session.title}",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{session.title}*\n{session.scheduled_date}\nTrainer: {session.trainer}"
                }
            }
        ]
    }
    requests.post(webhook_url, json=message)
```

---

## Troubleshooting

### Common Issues

**Issue**: Sessions scheduled on weekends
- **Solution**: The planner automatically skips weekends. Check your date range.

**Issue**: Not enough days for all sessions
- **Solution**: Extend the date range or increase sessions per day.

**Issue**: Reminders not showing
- **Solution**: Run `check-reminders` command. Reminders only show when due.

**Issue**: Attendance not saving
- **Solution**: Ensure you're using the correct session ID and saving after recording.

---

## Advanced Usage

### Batch Operations

```python
# Update multiple sessions
for session_id in ["KT-0001", "KT-0002", "KT-0003"]:
    session = planner.get_session(session_id)
    session.update_status("Completed")
    session.update_progress(100)
planner.save_sessions()

# Setup reminders for all upcoming sessions
upcoming = planner.get_upcoming_sessions(days=30)
for session in upcoming:
    planner.setup_reminders(session.session_id)
```

### Custom Reports

```python
def generate_trainer_report(planner, trainer_name):
    sessions = planner.list_sessions(trainer=trainer_name)
    completed = [s for s in sessions if s.status == "Completed"]
    
    report = f"Trainer Report: {trainer_name}\n"
    report += f"Total Sessions: {len(sessions)}\n"
    report += f"Completed: {len(completed)}\n"
    report += f"Completion Rate: {len(completed)/len(sessions)*100:.1f}%\n"
    
    return report
```

---

## Next Steps

1. **Try the Wizard**: Run `python kt_wizard.py` to create your first KT plan
2. **Explore Commands**: Use `python kt_cli_enhanced.py --help` to see all options
3. **Set Up Automation**: Integrate with your email/calendar systems
4. **Monitor Progress**: Check `progress-summary` regularly
5. **Gather Feedback**: Use notes to capture participant feedback

---

*Made with Bob*