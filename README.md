# KT Planner - Knowledge Transfer Session Manager

A comprehensive Python-based tool to create, organize, track, and manage Knowledge Transfer (KT) sessions.

## Features

- ✅ **Create KT Sessions** - Define detailed KT sessions with trainers, trainees, topics, and schedules
- 📋 **Track Progress** - Monitor completion percentage and session status
- 🔔 **Upcoming & Overdue Alerts** - Stay on top of scheduled and overdue sessions
- 🏷️ **Priority Management** - Categorize sessions by priority (Low, Medium, High, Critical)
- 📝 **Notes & Documentation** - Add timestamped notes to sessions
- 📊 **Statistics Dashboard** - View comprehensive statistics about your KT sessions
- 🔍 **Advanced Filtering** - Filter sessions by status, trainer, trainee, or priority
- 💾 **Persistent Storage** - All data saved in JSON format

## Installation

1. Clone or download this repository
2. Navigate to the KTPlanner directory
3. No external dependencies required - uses Python standard library only!

```bash
cd KTPlanner
```

## Usage

### Command Line Interface

The KT Planner provides a comprehensive CLI for managing sessions:

#### Create a New Session

```bash
python kt_cli.py create
```

This will launch an interactive session creator that prompts you for:
- Session title
- Description
- Trainer and trainee names
- Scheduled date and time
- Duration in hours
- Topics to be covered
- Priority level
- Prerequisites (optional)
- Materials/resources (optional)

#### List All Sessions

```bash
python kt_cli.py list
```

Filter sessions:
```bash
python kt_cli.py list --status "In Progress"
python kt_cli.py list --trainer "John Doe"
python kt_cli.py list --trainee "Jane Smith"
python kt_cli.py list --priority "High"
```

#### View Session Details

```bash
python kt_cli.py view KT-0001
```

#### Update Session Status

```bash
python kt_cli.py status KT-0001 "In Progress"
```

Available statuses:
- `Planned`
- `In Progress`
- `Completed`
- `Cancelled`
- `Postponed`

#### Update Session Progress

```bash
python kt_cli.py progress KT-0001 75
```

Progress is tracked as a percentage (0-100). When progress reaches 100%, the session is automatically marked as completed.

#### Add Notes to a Session

```bash
python kt_cli.py note KT-0001 "Covered topics 1-3, trainee needs more practice on topic 2"
```

Notes are automatically timestamped.

#### View Upcoming Sessions

```bash
python kt_cli.py upcoming
python kt_cli.py upcoming --days 14  # Next 14 days
```

#### View Overdue Sessions

```bash
python kt_cli.py overdue
```

#### View Statistics

```bash
python kt_cli.py stats
```

Displays:
- Total number of sessions
- Average completion percentage
- Sessions by status
- Sessions by priority
- Upcoming and overdue counts

#### Delete a Session

```bash
python kt_cli.py delete KT-0001
```

You'll be prompted to confirm the deletion.

## Data Structure

### KT Session Fields

Each KT session contains:

- **session_id**: Unique identifier (auto-generated, e.g., KT-0001)
- **title**: Session title
- **description**: Detailed description
- **trainer**: Name of the person conducting the KT
- **trainee**: Name of the person receiving the KT
- **scheduled_date**: Date and time (ISO format: YYYY-MM-DD HH:MM)
- **duration_hours**: Duration in hours
- **topics**: List of topics to be covered
- **priority**: Priority level (Low, Medium, High, Critical)
- **status**: Current status (Planned, In Progress, Completed, Cancelled, Postponed)
- **prerequisites**: List of prerequisites (optional)
- **materials**: List of materials/resources (optional)
- **notes**: Timestamped notes
- **completion_percentage**: Progress tracking (0-100%)
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

## Data Storage

All sessions are stored in `kt_sessions.json` in the same directory as the scripts. The file is automatically created on first use and updated whenever changes are made.

## Examples

### Example 1: Creating a Python Training Session

```bash
python kt_cli.py create
```

```
Session Title: Python Basics Training
Description: Introduction to Python programming for new team members
Trainer Name: Alice Johnson
Trainee Name: Bob Smith
Scheduled Date (YYYY-MM-DD HH:MM): 2026-05-30 10:00
Duration (hours): 3
Enter topics (one per line, empty line to finish):
  - Python syntax and data types
  - Control structures
  - Functions and modules
  - 
Priority (default: Medium): High
Enter prerequisites (one per line, empty line to finish):
  - Basic programming knowledge
  - Python installed on laptop
  - 
Enter materials/resources (one per line, empty line to finish):
  - Python documentation
  - Training slides
  - 
```

### Example 2: Tracking Progress

```bash
# Start the session
python kt_cli.py status KT-0001 "In Progress"

# Update progress after covering some topics
python kt_cli.py progress KT-0001 50
python kt_cli.py note KT-0001 "Completed first two topics, trainee is following well"

# Complete the session
python kt_cli.py progress KT-0001 100
```

### Example 3: Weekly Review

```bash
# Check upcoming sessions for the week
python kt_cli.py upcoming --days 7

# Check for any overdue sessions
python kt_cli.py overdue

# View overall statistics
python kt_cli.py stats
```

## Use Cases

- **Onboarding**: Track knowledge transfer sessions for new team members
- **Project Handoffs**: Manage KT sessions when transitioning projects between teams
- **Skill Development**: Organize training sessions for team skill enhancement
- **Documentation**: Keep detailed records of what was covered in each session
- **Team Management**: Monitor KT progress across multiple trainers and trainees

## Tips

1. **Regular Updates**: Update session progress and add notes during or immediately after sessions
2. **Set Priorities**: Use priority levels to focus on critical knowledge transfers first
3. **Check Overdue**: Regularly check for overdue sessions to reschedule them
4. **Use Prerequisites**: Document prerequisites to ensure trainees are prepared
5. **Add Materials**: Link to relevant documentation and resources for future reference

## File Structure

```
KTPlanner/
├── kt_planner.py      # Core KT Planner logic and data models
├── kt_cli.py          # Command-line interface
├── kt_sessions.json   # Data storage (auto-created)
└── README.md          # This file
```

## Python API Usage

You can also use the KT Planner programmatically:

```python
from kt_planner import KTPlanner

# Initialize planner
planner = KTPlanner()

# Create a session
session = planner.create_session(
    title="API Training",
    description="REST API development training",
    trainer="Alice",
    trainee="Bob",
    scheduled_date="2026-06-01 14:00",
    duration_hours=2,
    topics=["REST principles", "API design", "Authentication"],
    priority="High"
)

# Update progress
session.update_progress(50)
planner.save_sessions()

# Get statistics
stats = planner.get_statistics()
print(stats)
```

## Requirements

- Python 3.7 or higher
- No external dependencies required

## License

This project is open source and available for use in any organization or project.

## Support

For issues or questions, please refer to the code comments or create an issue in the repository.

---

**Happy Knowledge Transferring! 🎓**