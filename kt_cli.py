#!/usr/bin/env python3
"""
KT Planner CLI - Command Line Interface for managing KT sessions
"""

import sys
import argparse
from datetime import datetime
from typing import List
from kt_planner import KTPlanner, KTStatus, KTPriority


class KTCli:
    """Command Line Interface for KT Planner"""
    
    def __init__(self):
        self.planner = KTPlanner()
    
    def create_session_interactive(self):
        """Create a new KT session interactively"""
        print("\n=== Create New KT Session ===\n")
        
        title = input("Session Title: ").strip()
        description = input("Description: ").strip()
        trainer = input("Trainer Name: ").strip()
        trainee = input("Trainee Name: ").strip()
        
        # Get scheduled date
        while True:
            date_str = input("Scheduled Date (YYYY-MM-DD HH:MM): ").strip()
            try:
                datetime.fromisoformat(date_str)
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD HH:MM")
        
        # Get duration
        while True:
            try:
                duration = float(input("Duration (hours): ").strip())
                break
            except ValueError:
                print("Invalid duration. Please enter a number.")
        
        # Get topics
        print("Enter topics (one per line, empty line to finish):")
        topics = []
        while True:
            topic = input("  - ").strip()
            if not topic:
                break
            topics.append(topic)
        
        # Get priority
        print(f"\nPriority levels: {', '.join([p.value for p in KTPriority])}")
        priority = input("Priority (default: Medium): ").strip() or "Medium"
        
        # Get prerequisites (optional)
        print("\nEnter prerequisites (one per line, empty line to finish):")
        prerequisites = []
        while True:
            prereq = input("  - ").strip()
            if not prereq:
                break
            prerequisites.append(prereq)
        
        # Get materials (optional)
        print("\nEnter materials/resources (one per line, empty line to finish):")
        materials = []
        while True:
            material = input("  - ").strip()
            if not material:
                break
            materials.append(material)
        
        # Create session
        session = self.planner.create_session(
            title=title,
            description=description,
            trainer=trainer,
            trainee=trainee,
            scheduled_date=date_str,
            duration_hours=duration,
            topics=topics,
            priority=priority,
            prerequisites=prerequisites if prerequisites else None,
            materials=materials if materials else None
        )
        
        print(f"\n✓ Session created successfully! ID: {session.session_id}")
        self.display_session(session)
    
    def display_session(self, session):
        """Display a single session details"""
        print(f"\n{'='*60}")
        print(f"Session ID: {session.session_id}")
        print(f"Title: {session.title}")
        print(f"Description: {session.description}")
        print(f"Trainer: {session.trainer}")
        print(f"Trainee: {session.trainee}")
        print(f"Scheduled: {session.scheduled_date}")
        print(f"Duration: {session.duration_hours} hours")
        print(f"Status: {session.status}")
        print(f"Priority: {session.priority}")
        print(f"Completion: {session.completion_percentage}%")
        print(f"\nTopics:")
        for topic in session.topics:
            print(f"  • {topic}")
        
        if session.prerequisites:
            print(f"\nPrerequisites:")
            for prereq in session.prerequisites:
                print(f"  • {prereq}")
        
        if session.materials:
            print(f"\nMaterials:")
            for material in session.materials:
                print(f"  • {material}")
        
        if session.notes:
            print(f"\nNotes:{session.notes}")
        
        print(f"{'='*60}\n")
    
    def list_sessions(self, status=None, trainer=None, trainee=None, priority=None):
        """List sessions with optional filters"""
        sessions = self.planner.list_sessions(status, trainer, trainee, priority)
        
        if not sessions:
            print("\nNo sessions found.")
            return
        
        print(f"\n{'='*80}")
        print(f"{'ID':<12} {'Title':<25} {'Trainer':<15} {'Status':<15} {'Date':<15}")
        print(f"{'='*80}")
        
        for session in sessions:
            date_str = session.scheduled_date[:10] if len(session.scheduled_date) >= 10 else session.scheduled_date
            print(f"{session.session_id:<12} {session.title[:24]:<25} {session.trainer[:14]:<15} {session.status:<15} {date_str:<15}")
        
        print(f"{'='*80}\n")
        print(f"Total: {len(sessions)} session(s)")
    
    def update_session_status(self, session_id: str, new_status: str):
        """Update session status"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        session.update_status(new_status)
        self.planner.save_sessions()
        print(f"✓ Session {session_id} status updated to: {new_status}")
    
    def update_session_progress(self, session_id: str, percentage: int):
        """Update session completion percentage"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        session.update_progress(percentage)
        self.planner.save_sessions()
        print(f"✓ Session {session_id} progress updated to: {percentage}%")
        if percentage == 100:
            print(f"✓ Session marked as completed!")
    
    def add_session_note(self, session_id: str, note: str):
        """Add a note to a session"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        session.add_note(note)
        self.planner.save_sessions()
        print(f"✓ Note added to session {session_id}")
    
    def show_upcoming_sessions(self, days: int = 7):
        """Show upcoming sessions"""
        sessions = self.planner.get_upcoming_sessions(days)
        
        if not sessions:
            print(f"\nNo sessions scheduled in the next {days} days.")
            return
        
        print(f"\n=== Upcoming Sessions (Next {days} Days) ===\n")
        for session in sessions:
            print(f"• {session.session_id} - {session.title}")
            print(f"  Scheduled: {session.scheduled_date}")
            print(f"  Trainer: {session.trainer} → Trainee: {session.trainee}")
            print(f"  Status: {session.status} | Priority: {session.priority}\n")
    
    def show_overdue_sessions(self):
        """Show overdue sessions"""
        sessions = self.planner.get_overdue_sessions()
        
        if not sessions:
            print("\n✓ No overdue sessions!")
            return
        
        print(f"\n=== Overdue Sessions ===\n")
        for session in sessions:
            print(f"• {session.session_id} - {session.title}")
            print(f"  Scheduled: {session.scheduled_date}")
            print(f"  Trainer: {session.trainer} → Trainee: {session.trainee}")
            print(f"  Status: {session.status} | Priority: {session.priority}\n")
    
    def show_statistics(self):
        """Show statistics"""
        stats = self.planner.get_statistics()
        
        print("\n=== KT Planner Statistics ===\n")
        print(f"Total Sessions: {stats['total_sessions']}")
        print(f"Average Completion: {stats['average_completion']}%")
        print(f"Upcoming Sessions: {stats['upcoming_count']}")
        print(f"Overdue Sessions: {stats['overdue_count']}")
        
        print("\nBy Status:")
        for status, count in stats['by_status'].items():
            print(f"  • {status}: {count}")
        
        print("\nBy Priority:")
        for priority, count in stats['by_priority'].items():
            print(f"  • {priority}: {count}")
        print()
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        confirm = input(f"Are you sure you want to delete session {session_id} - {session.title}? (yes/no): ")
        if confirm.lower() == 'yes':
            self.planner.delete_session(session_id)
            print(f"✓ Session {session_id} deleted successfully.")
        else:
            print("Deletion cancelled.")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="KT Planner - Knowledge Transfer Session Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create session
    create_parser = subparsers.add_parser('create', help='Create a new KT session')
    
    # List sessions
    list_parser = subparsers.add_parser('list', help='List KT sessions')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--trainer', help='Filter by trainer')
    list_parser.add_argument('--trainee', help='Filter by trainee')
    list_parser.add_argument('--priority', help='Filter by priority')
    
    # View session
    view_parser = subparsers.add_parser('view', help='View session details')
    view_parser.add_argument('session_id', help='Session ID')
    
    # Update status
    status_parser = subparsers.add_parser('status', help='Update session status')
    status_parser.add_argument('session_id', help='Session ID')
    status_parser.add_argument('new_status', help='New status', 
                              choices=[s.value for s in KTStatus])
    
    # Update progress
    progress_parser = subparsers.add_parser('progress', help='Update session progress')
    progress_parser.add_argument('session_id', help='Session ID')
    progress_parser.add_argument('percentage', type=int, help='Completion percentage (0-100)')
    
    # Add note
    note_parser = subparsers.add_parser('note', help='Add a note to session')
    note_parser.add_argument('session_id', help='Session ID')
    note_parser.add_argument('note', help='Note text')
    
    # Upcoming sessions
    upcoming_parser = subparsers.add_parser('upcoming', help='Show upcoming sessions')
    upcoming_parser.add_argument('--days', type=int, default=7, help='Number of days (default: 7)')
    
    # Overdue sessions
    overdue_parser = subparsers.add_parser('overdue', help='Show overdue sessions')
    
    # Statistics
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    # Delete session
    delete_parser = subparsers.add_parser('delete', help='Delete a session')
    delete_parser.add_argument('session_id', help='Session ID')
    
    args = parser.parse_args()
    cli = KTCli()
    
    if args.command == 'create':
        cli.create_session_interactive()
    elif args.command == 'list':
        cli.list_sessions(args.status, args.trainer, args.trainee, args.priority)
    elif args.command == 'view':
        session = cli.planner.get_session(args.session_id)
        if session:
            cli.display_session(session)
        else:
            print(f"Session {args.session_id} not found.")
    elif args.command == 'status':
        cli.update_session_status(args.session_id, args.new_status)
    elif args.command == 'progress':
        cli.update_session_progress(args.session_id, args.percentage)
    elif args.command == 'note':
        cli.add_session_note(args.session_id, args.note)
    elif args.command == 'upcoming':
        cli.show_upcoming_sessions(args.days)
    elif args.command == 'overdue':
        cli.show_overdue_sessions()
    elif args.command == 'stats':
        cli.show_statistics()
    elif args.command == 'delete':
        cli.delete_session(args.session_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# Made with Bob
