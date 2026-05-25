#!/usr/bin/env python3
"""
Example usage of KT Planner API
This script demonstrates how to use the KT Planner programmatically
"""

from kt_planner import KTPlanner, KTStatus, KTPriority
from datetime import datetime, timedelta


def demo_kt_planner():
    """Demonstrate KT Planner functionality"""
    
    print("=" * 60)
    print("KT Planner - Example Usage Demo")
    print("=" * 60)
    
    # Initialize the planner
    planner = KTPlanner(data_file="demo_kt_sessions.json")
    
    # Example 1: Create a Python training session
    print("\n1. Creating a Python training session...")
    session1 = planner.create_session(
        title="Python Fundamentals Training",
        description="Comprehensive introduction to Python programming",
        trainer="Alice Johnson",
        trainee="Bob Smith",
        scheduled_date=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d 10:00"),
        duration_hours=4,
        topics=[
            "Python syntax and data types",
            "Control structures (if, for, while)",
            "Functions and modules",
            "Object-oriented programming basics"
        ],
        priority=KTPriority.HIGH.value,
        prerequisites=[
            "Basic programming knowledge",
            "Python 3.x installed",
            "IDE setup (VS Code or PyCharm)"
        ],
        materials=[
            "Python official documentation",
            "Training slides (shared drive)",
            "Practice exercises repository"
        ]
    )
    print(f"✓ Created session: {session1.session_id} - {session1.title}")
    
    # Example 2: Create a database training session
    print("\n2. Creating a database training session...")
    session2 = planner.create_session(
        title="SQL Database Fundamentals",
        description="Introduction to relational databases and SQL",
        trainer="Carol Davis",
        trainee="David Wilson",
        scheduled_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d 14:00"),
        duration_hours=3,
        topics=[
            "Database concepts and design",
            "SQL queries (SELECT, JOIN, WHERE)",
            "Data manipulation (INSERT, UPDATE, DELETE)",
            "Indexes and optimization"
        ],
        priority=KTPriority.MEDIUM.value,
        prerequisites=[
            "Basic understanding of data structures"
        ],
        materials=[
            "SQL tutorial website",
            "Sample database for practice"
        ]
    )
    print(f"✓ Created session: {session2.session_id} - {session2.title}")
    
    # Example 3: Create an urgent API training session
    print("\n3. Creating an urgent API training session...")
    session3 = planner.create_session(
        title="REST API Development",
        description="Building and consuming REST APIs",
        trainer="Eve Martinez",
        trainee="Frank Brown",
        scheduled_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 09:00"),
        duration_hours=2.5,
        topics=[
            "REST principles and HTTP methods",
            "API design best practices",
            "Authentication and authorization",
            "API testing with Postman"
        ],
        priority=KTPriority.CRITICAL.value
    )
    print(f"✓ Created session: {session3.session_id} - {session3.title}")
    
    # Example 4: Update session status and progress
    print("\n4. Simulating session progress...")
    session1.update_status(KTStatus.IN_PROGRESS.value)
    print(f"✓ Updated {session1.session_id} status to: {session1.status}")
    
    session1.update_progress(50)
    print(f"✓ Updated {session1.session_id} progress to: {session1.completion_percentage}%")
    
    session1.add_note("Covered Python basics and data types. Trainee is following well.")
    print(f"✓ Added note to {session1.session_id}")
    
    # Save all changes
    planner.save_sessions()
    
    # Example 5: List all sessions
    print("\n5. Listing all sessions...")
    all_sessions = planner.list_sessions()
    print(f"\nTotal sessions: {len(all_sessions)}")
    for session in all_sessions:
        print(f"  • {session.session_id}: {session.title} ({session.status})")
    
    # Example 6: Filter sessions by status
    print("\n6. Filtering sessions by status...")
    in_progress = planner.list_sessions(status=KTStatus.IN_PROGRESS.value)
    print(f"\nSessions in progress: {len(in_progress)}")
    for session in in_progress:
        print(f"  • {session.session_id}: {session.title}")
    
    # Example 7: Get upcoming sessions
    print("\n7. Getting upcoming sessions (next 7 days)...")
    upcoming = planner.get_upcoming_sessions(days=7)
    print(f"\nUpcoming sessions: {len(upcoming)}")
    for session in upcoming:
        print(f"  • {session.session_id}: {session.title}")
        print(f"    Scheduled: {session.scheduled_date}")
        print(f"    Priority: {session.priority}")
    
    # Example 8: Get statistics
    print("\n8. Getting statistics...")
    stats = planner.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total sessions: {stats['total_sessions']}")
    print(f"  Average completion: {stats['average_completion']}%")
    print(f"  Upcoming: {stats['upcoming_count']}")
    print(f"  Overdue: {stats['overdue_count']}")
    print(f"\n  By Status:")
    for status, count in stats['by_status'].items():
        print(f"    • {status}: {count}")
    print(f"\n  By Priority:")
    for priority, count in stats['by_priority'].items():
        print(f"    • {priority}: {count}")
    
    # Example 9: View a specific session
    print(f"\n9. Viewing session details for {session1.session_id}...")
    print(f"\n{'='*60}")
    print(f"Session ID: {session1.session_id}")
    print(f"Title: {session1.title}")
    print(f"Description: {session1.description}")
    print(f"Trainer: {session1.trainer} → Trainee: {session1.trainee}")
    print(f"Scheduled: {session1.scheduled_date}")
    print(f"Duration: {session1.duration_hours} hours")
    print(f"Status: {session1.status}")
    print(f"Priority: {session1.priority}")
    print(f"Completion: {session1.completion_percentage}%")
    print(f"\nTopics:")
    for topic in session1.topics:
        print(f"  • {topic}")
    if session1.prerequisites:
        print(f"\nPrerequisites:")
        for prereq in session1.prerequisites:
            print(f"  • {prereq}")
    if session1.materials:
        print(f"\nMaterials:")
        for material in session1.materials:
            print(f"  • {material}")
    if session1.notes:
        print(f"\nNotes:{session1.notes}")
    print(f"{'='*60}")
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print(f"Demo data saved to: demo_kt_sessions.json")
    print("="*60)
    print("\nNext steps:")
    print("1. Check the demo_kt_sessions.json file to see the data structure")
    print("2. Try the CLI: python kt_cli.py list")
    print("3. Create your own sessions: python kt_cli.py create")
    print("4. Read QUICKSTART.md for more examples")


if __name__ == "__main__":
    demo_kt_planner()

# Made with Bob
