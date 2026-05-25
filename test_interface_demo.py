#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive demonstration of KT Planner interface
This script creates sample sessions and demonstrates all features
"""

import sys
from datetime import datetime, timedelta
from kt_planner import KTPlanner, KTStatus, KTPriority

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_session_details(session):
    """Print detailed session information"""
    print(f"Session ID: {session.session_id}")
    print(f"Title: {session.title}")
    print(f"Trainer: {session.trainer} -> Trainee: {session.trainee}")
    print(f"Scheduled: {session.scheduled_date}")
    print(f"Duration: {session.duration_hours} hours")
    print(f"Status: {session.status}")
    print(f"Priority: {session.priority}")
    print(f"Progress: {session.completion_percentage}%")
    print(f"Topics: {', '.join(session.topics)}")
    if session.notes:
        print(f"Notes: {session.notes}")
    print()

def main():
    print_header("KT Planner Interface Demonstration")
    
    # Initialize planner
    print("[1] Initializing KT Planner...")
    planner = KTPlanner(data_file="demo_sessions.json")
    print("    Planner initialized successfully!\n")
    
    # Create sample sessions
    print_header("Creating Sample Sessions")
    
    today = datetime.now()
    
    print("[2] Creating Session 1: Python Advanced Concepts...")
    session1 = planner.create_session(
        title="Python Advanced Concepts",
        description="Deep dive into decorators, generators, and context managers",
        trainer="Alice Smith",
        trainee="Bob Johnson",
        scheduled_date=(today + timedelta(days=2)).strftime("%Y-%m-%d 10:00"),
        duration_hours=3.0,
        topics=["Decorators", "Generators", "Context Managers", "Metaclasses"],
        priority="High",
        prerequisites=["Basic Python", "OOP Concepts"],
        materials=["Python Documentation", "Code Examples"]
    )
    print(f"    Created: {session1.session_id}")
    
    print("\n[3] Creating Session 2: Database Design...")
    session2 = planner.create_session(
        title="Database Design Principles",
        description="Learn normalization, indexing, and query optimization",
        trainer="Carol Davis",
        trainee="David Wilson",
        scheduled_date=(today + timedelta(days=5)).strftime("%Y-%m-%d 14:00"),
        duration_hours=2.5,
        topics=["Normalization", "Indexing", "Query Optimization"],
        priority="Medium",
        prerequisites=["SQL Basics"],
        materials=["Database Design Book", "Sample Schemas"]
    )
    print(f"    Created: {session2.session_id}")
    
    print("\n[4] Creating Session 3: API Development...")
    session3 = planner.create_session(
        title="RESTful API Development",
        description="Building scalable REST APIs with best practices",
        trainer="Eve Martinez",
        trainee="Frank Brown",
        scheduled_date=(today + timedelta(days=7)).strftime("%Y-%m-%d 09:00"),
        duration_hours=4.0,
        topics=["REST Principles", "Authentication", "Rate Limiting", "Documentation"],
        priority="High",
        prerequisites=["HTTP Basics", "JSON"],
        materials=["API Design Guide", "Postman Collection"]
    )
    print(f"    Created: {session3.session_id}")
    
    # List all sessions
    print_header("Listing All Sessions")
    print("[5] Retrieving all sessions...")
    all_sessions = planner.list_sessions()
    print(f"    Total sessions: {len(all_sessions)}\n")
    
    for session in all_sessions:
        print_session_details(session)
    
    # Update session status
    print_header("Updating Session Status")
    print(f"[6] Starting session {session1.session_id}...")
    session1.update_status(KTStatus.IN_PROGRESS.value)
    planner.save_sessions()
    print(f"    Status updated to: {session1.status}")
    
    # Update progress
    print_header("Tracking Progress")
    print(f"[7] Updating progress for {session1.session_id}...")
    session1.update_progress(50)
    planner.save_sessions()
    print(f"    Progress: {session1.completion_percentage}%")
    
    # Add notes
    print_header("Adding Session Notes")
    print(f"[8] Adding notes to {session1.session_id}...")
    session1.add_note("Covered decorators and generators. Students showing good understanding.")
    planner.save_sessions()
    print(f"    Note added successfully")
    print(f"    Current notes: {session1.notes}")
    
    # Filter sessions
    print_header("Filtering Sessions")
    print("[9] Filtering by priority: High...")
    high_priority = planner.list_sessions(priority="High")
    print(f"    Found {len(high_priority)} high-priority sessions:")
    for session in high_priority:
        print(f"    - {session.session_id}: {session.title}")
    
    print("\n[10] Filtering by trainer: Alice Smith...")
    alice_sessions = planner.list_sessions(trainer="Alice Smith")
    print(f"    Found {len(alice_sessions)} sessions by Alice:")
    for session in alice_sessions:
        print(f"    - {session.session_id}: {session.title}")
    
    print("\n[11] Filtering by status: In Progress...")
    in_progress = planner.list_sessions(status=KTStatus.IN_PROGRESS.value)
    print(f"    Found {len(in_progress)} sessions in progress:")
    for session in in_progress:
        print(f"    - {session.session_id}: {session.title}")
    
    # Upcoming sessions
    print_header("Upcoming Sessions")
    print("[12] Getting sessions in next 7 days...")
    upcoming = planner.get_upcoming_sessions(days=7)
    print(f"    Found {len(upcoming)} upcoming sessions:")
    for session in upcoming:
        print(f"    - {session.session_id}: {session.title} on {session.scheduled_date}")
    
    # Statistics
    print_header("Statistics Dashboard")
    print("[13] Generating statistics...")
    stats = planner.get_statistics()
    
    print(f"Total Sessions: {stats['total_sessions']}")
    print(f"Average Completion: {stats['average_completion']}%")
    print(f"Upcoming Sessions: {stats['upcoming_count']}")
    print(f"Overdue Sessions: {stats['overdue_count']}")
    
    print("\nBy Status:")
    for status, count in stats['by_status'].items():
        print(f"  - {status}: {count}")
    
    print("\nBy Priority:")
    for priority, count in stats['by_priority'].items():
        print(f"  - {priority}: {count}")
    
    # Complete a session
    print_header("Completing a Session")
    print(f"[14] Completing session {session1.session_id}...")
    session1.update_progress(100)
    planner.save_sessions()
    print(f"    Progress: {session1.completion_percentage}%")
    print(f"    Status: {session1.status}")
    
    # View specific session
    print_header("Viewing Session Details")
    print(f"[15] Retrieving details for {session1.session_id}...")
    retrieved_session = planner.get_session(session1.session_id)
    if retrieved_session:
        print_session_details(retrieved_session)
    
    # Final statistics
    print_header("Final Statistics")
    print("[16] Generating final statistics...")
    final_stats = planner.get_statistics()
    
    print(f"Total Sessions: {final_stats['total_sessions']}")
    print(f"Completed: {final_stats['by_status'].get('Completed', 0)}")
    print(f"In Progress: {final_stats['by_status'].get('In Progress', 0)}")
    print(f"Planned: {final_stats['by_status'].get('Planned', 0)}")
    print(f"Average Completion: {final_stats['average_completion']}%")
    
    print_header("Demonstration Complete!")
    print("All KT Planner features have been successfully demonstrated.")
    print(f"Session data saved to: demo_sessions.json")
    print("\nYou can now:")
    print("  - View sessions: python kt_cli.py list")
    print("  - View details: python kt_cli.py view KT-0001")
    print("  - Update status: python kt_cli.py status KT-0001 'Completed'")
    print("  - Check stats: python kt_cli.py stats")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
