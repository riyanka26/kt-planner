# KT Planner Testing Guide

## Overview
This guide provides comprehensive instructions for testing the KT Planner application with its various interfaces.

## Prerequisites
- Python 3.7 or higher installed
- Required packages: `pip install -r requirements.txt`

## Testing Methods

### 1. Automated Unit Tests

Run the complete test suite:
```bash
python test_kt_planner.py
```

This will execute 11 comprehensive tests covering:
- ✓ Session creation
- ✓ Session serialization/deserialization
- ✓ Status updates
- ✓ Progress tracking
- ✓ Note management
- ✓ Planner operations
- ✓ Save/load functionality
- ✓ Session filtering
- ✓ Upcoming sessions
- ✓ Statistics generation

Expected output:
```
============================================================
KT Planner Test Suite
============================================================

Testing session creation...
✓ Session creation test passed
Testing session serialization...
✓ Session serialization test passed
...
============================================================
Test Results: 11 passed, 0 failed
============================================================

🎉 All tests passed! The KT Planner is working correctly.
```

### 2. Command Line Interface (CLI) Testing

#### Create a New Session
```bash
python kt_cli.py create
```
Follow the interactive prompts to create a session.

#### List All Sessions
```bash
python kt_cli.py list
```

#### Filter Sessions
```bash
# By status
python kt_cli.py list --status "In Progress"

# By trainer
python kt_cli.py list --trainer "Alice"

# By priority
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

#### Update Progress
```bash
python kt_cli.py progress KT-0001 50
```

#### Add Notes
```bash
python kt_cli.py note KT-0001 "Completed first module successfully"
```

#### View Upcoming Sessions
```bash
# Next 7 days (default)
python kt_cli.py upcoming

# Next 30 days
python kt_cli.py upcoming --days 30
```

#### View Overdue Sessions
```bash
python kt_cli.py overdue
```

#### View Statistics
```bash
python kt_cli.py stats
```

#### Delete a Session
```bash
python kt_cli.py delete KT-0001
```

### 3. Python API Testing

Create a test script:

```python
from kt_planner import KTPlanner, KTStatus, KTPriority

# Initialize planner
planner = KTPlanner()

# Create a session
session = planner.create_session(
    title="Python API Testing",
    description="Testing the Python API",
    trainer="Alice Smith",
    trainee="Bob Johnson",
    scheduled_date="2026-06-01 10:00",
    duration_hours=2.5,
    topics=["API Basics", "Advanced Features"],
    priority="High"
)

print(f"Created session: {session.session_id}")

# Update status
session.update_status(KTStatus.IN_PROGRESS.value)
print(f"Status: {session.status}")

# Update progress
session.update_progress(75)
print(f"Progress: {session.completion_percentage}%")

# Add notes
session.add_note("Great progress on API testing")
print(f"Notes: {session.notes}")

# List all sessions
all_sessions = planner.list_sessions()
print(f"Total sessions: {len(all_sessions)}")

# Get statistics
stats = planner.get_statistics()
print(f"Statistics: {stats}")
```

### 4. Interactive Testing Scenarios

#### Scenario 1: Complete KT Session Lifecycle
1. Create a new session with `create` command
2. View the session with `view` command
3. Start the session: `status KT-XXXX "In Progress"`
4. Update progress periodically: `progress KT-XXXX 25`, `progress KT-XXXX 50`, etc.
5. Add notes during the session: `note KT-XXXX "Covered topic 1"`
6. Complete the session: `progress KT-XXXX 100`
7. Verify completion: `view KT-XXXX`

#### Scenario 2: Managing Multiple Sessions
1. Create 3-5 sessions with different dates and priorities
2. List all sessions: `list`
3. Filter by priority: `list --priority "High"`
4. Check upcoming sessions: `upcoming`
5. View statistics: `stats`

#### Scenario 3: Handling Overdue Sessions
1. Create sessions with past dates
2. Check overdue: `overdue`
3. Update their status or reschedule

### 5. Data Persistence Testing

1. Create several sessions
2. Close the application
3. Reopen and verify sessions are loaded
4. Check that `kt_sessions.json` file exists and contains valid JSON

### 6. Error Handling Testing

Test invalid inputs:
```bash
# Invalid session ID
python kt_cli.py view INVALID-ID

# Invalid status
python kt_cli.py status KT-0001 "InvalidStatus"

# Invalid progress percentage
python kt_cli.py progress KT-0001 150
```

## Expected Results

### Successful Test Indicators
- ✓ All unit tests pass
- ✓ Sessions are created with unique IDs
- ✓ Data persists across sessions
- ✓ Status updates work correctly
- ✓ Progress tracking updates status automatically at 100%
- ✓ Filters return correct results
- ✓ Statistics are accurate
- ✓ CLI commands execute without errors

### Common Issues and Solutions

#### Issue: Python not found
**Solution:** Install Python 3.7+ and add to PATH

#### Issue: Module not found
**Solution:** Run `pip install -r requirements.txt`

#### Issue: Permission denied on JSON file
**Solution:** Check file permissions or run with appropriate privileges

#### Issue: Invalid date format
**Solution:** Use format YYYY-MM-DD HH:MM

## Performance Testing

For large datasets:
```python
# Create 100 sessions
for i in range(100):
    planner.create_session(
        title=f"Session {i}",
        description=f"Test session {i}",
        trainer="Trainer",
        trainee="Trainee",
        scheduled_date="2026-06-01 10:00",
        duration_hours=2,
        topics=["Topic"]
    )

# Test listing performance
import time
start = time.time()
sessions = planner.list_sessions()
end = time.time()
print(f"Listed {len(sessions)} sessions in {end-start:.4f} seconds")
```

## Continuous Testing

Set up automated testing:
```bash
# Run tests before commits
git add .
python test_kt_planner.py && git commit -m "Your message"
```

## Test Coverage

Current test coverage:
- Session creation: ✓
- Session serialization: ✓
- Status management: ✓
- Progress tracking: ✓
- Note management: ✓
- Filtering: ✓
- Statistics: ✓
- Data persistence: ✓
- CLI commands: ✓

## Reporting Issues

When reporting issues, include:
1. Python version: `python --version`
2. Operating system
3. Command executed
4. Expected vs actual behavior
5. Error messages
6. Contents of `kt_sessions.json` (if relevant)

## Next Steps

After successful testing:
1. Review the [QUICKSTART.md](QUICKSTART.md) for usage examples
2. Check [README.md](README.md) for feature documentation
3. Explore [example_usage.py](example_usage.py) for code samples
4. Start using KT Planner for your knowledge transfer sessions!

---
*Made with Bob*