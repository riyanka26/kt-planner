# KT Planner - Quick Start Guide

Get started with KT Planner in 5 minutes!

## Step 1: Verify Python Installation

```bash
python --version
```

Make sure you have Python 3.7 or higher.

## Step 2: Navigate to KTPlanner Directory

```bash
cd KTPlanner
```

## Step 3: Create Your First KT Session

Run the interactive session creator:

```bash
python kt_cli.py create
```

Follow the prompts to create your first session. Here's an example:

```
Session Title: Introduction to Git
Description: Basic Git commands and workflows
Trainer Name: Sarah Chen
Trainee Name: Mike Johnson
Scheduled Date (YYYY-MM-DD HH:MM): 2026-05-28 14:00
Duration (hours): 2
Enter topics (one per line, empty line to finish):
  - Git basics and installation
  - Branching and merging
  - Pull requests
  - 
Priority (default: Medium): High
```

## Step 4: View Your Sessions

List all sessions:

```bash
python kt_cli.py list
```

View detailed information:

```bash
python kt_cli.py view KT-0001
```

## Step 5: Track Progress

Start the session:

```bash
python kt_cli.py status KT-0001 "In Progress"
```

Update progress (0-100%):

```bash
python kt_cli.py progress KT-0001 50
```

Add notes:

```bash
python kt_cli.py note KT-0001 "Covered Git basics, moving to branching next"
```

Complete the session:

```bash
python kt_cli.py progress KT-0001 100
```

## Common Commands Cheat Sheet

| Command | Description |
|---------|-------------|
| `python kt_cli.py create` | Create new session |
| `python kt_cli.py list` | List all sessions |
| `python kt_cli.py view <ID>` | View session details |
| `python kt_cli.py status <ID> <STATUS>` | Update status |
| `python kt_cli.py progress <ID> <0-100>` | Update progress |
| `python kt_cli.py note <ID> "<text>"` | Add note |
| `python kt_cli.py upcoming` | Show upcoming sessions |
| `python kt_cli.py overdue` | Show overdue sessions |
| `python kt_cli.py stats` | View statistics |
| `python kt_cli.py delete <ID>` | Delete session |

## Available Statuses

- `Planned` - Session is scheduled but not started
- `In Progress` - Session is currently ongoing
- `Completed` - Session is finished
- `Cancelled` - Session was cancelled
- `Postponed` - Session was postponed

## Available Priorities

- `Low` - Can be scheduled flexibly
- `Medium` - Standard priority
- `High` - Important, schedule soon
- `Critical` - Urgent, highest priority

## Tips for Success

1. **Create sessions in advance** - Plan your KT sessions ahead of time
2. **Update regularly** - Keep progress and notes current
3. **Check upcoming** - Run `python kt_cli.py upcoming` weekly
4. **Monitor overdue** - Address overdue sessions promptly
5. **Use filters** - Filter by trainer, trainee, or status to focus on specific sessions

## Example Workflow

### Weekly Planning
```bash
# Check what's coming up
python kt_cli.py upcoming --days 7

# Check for overdue sessions
python kt_cli.py overdue

# View statistics
python kt_cli.py stats
```

### During a Session
```bash
# Mark as in progress
python kt_cli.py status KT-0001 "In Progress"

# Update progress periodically
python kt_cli.py progress KT-0001 25
python kt_cli.py progress KT-0001 50
python kt_cli.py progress KT-0001 75

# Add notes
python kt_cli.py note KT-0001 "Trainee grasped concepts quickly"

# Complete
python kt_cli.py progress KT-0001 100
```

### Monthly Review
```bash
# View all completed sessions
python kt_cli.py list --status "Completed"

# Check statistics
python kt_cli.py stats

# Review specific sessions
python kt_cli.py view KT-0001
```

## Need Help?

- Run `python kt_cli.py --help` for command help
- Run `python kt_cli.py <command> --help` for specific command help
- Check README.md for detailed documentation

## What's Next?

- Explore filtering options with `--status`, `--trainer`, `--trainee`, `--priority`
- Use the Python API for custom integrations (see README.md)
- Set up regular reviews of upcoming and overdue sessions

Happy Knowledge Transferring! 🚀