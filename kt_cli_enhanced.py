#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced KT Planner CLI with advanced features
"""

import sys
import argparse
from datetime import datetime
from typing import List
from kt_planner import KTPlanner, KTStatus, KTPriority
from kt_cli import KTCli

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class EnhancedKTCli(KTCli):
    """Enhanced CLI with additional features"""
    
    def record_attendance_interactive(self, session_id: str):
        """Record attendance for a session interactively"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        print(f"\n=== Record Attendance for {session_id} ===\n")
        print(f"Session: {session.title}")
        print(f"Participants: {', '.join(session.participants) if session.participants else session.trainee}")
        print()
        
        print("Enter names of attendees (one per line, empty line to finish):")
        attended = []
        while True:
            name = input("  Attended: ").strip()
            if not name:
                break
            attended.append(name)
        
        print("\nEnter names of those who missed (one per line, empty line to finish):")
        missed = []
        while True:
            name = input("  Missed: ").strip()
            if not name:
                break
            missed.append(name)
        
        follow_up = input("\nAny follow-up needed? (optional): ").strip()
        
        session.record_attendance(attended, missed, follow_up if follow_up else None)
        self.planner.save_sessions()
        
        print(f"\n[SUCCESS] Attendance recorded for {session_id}")
        print(f"  Attended: {len(attended)}")
        print(f"  Missed: {len(missed)}")
        if follow_up:
            print(f"  Follow-up: {follow_up}")
    
    def add_document_to_session(self, session_id: str, name: str, url: str, description: str = ""):
        """Add a document to a session"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        session.add_document(name, url, description)
        self.planner.save_sessions()
        print(f"\n[SUCCESS] Document '{name}' added to {session_id}")
    
    def show_session_documents(self, session_id: str):
        """Show all documents for a session"""
        session = self.planner.get_session(session_id)
        if not session:
            print(f"Session {session_id} not found.")
            return
        
        if not session.documents:
            print(f"\nNo documents uploaded for {session_id}")
            return
        
        print(f"\n=== Documents for {session_id} ===\n")
        for i, doc in enumerate(session.documents, 1):
            print(f"{i}. {doc['name']}")
            print(f"   URL: {doc['url']}")
            if doc.get('description'):
                print(f"   Description: {doc['description']}")
            print(f"   Uploaded: {doc['uploaded_at']}")
            print()
    
    def check_reminders(self):
        """Check and display pending reminders"""
        reminders = self.planner.get_pending_reminders()
        
        if not reminders:
            print("\n[SUCCESS] No pending reminders")
            return
        
        print(f"\n=== Pending Reminders ({len(reminders)}) ===\n")
        for reminder in reminders:
            print(f"[{reminder['reminder_type'].replace('_', ' ').title()}]")
            print(f"  Session: {reminder['session_id']} - {reminder['session_title']}")
            print(f"  Scheduled: {reminder['scheduled_date']}")
            print(f"  Message: {reminder['message']}")
            print()
    
    def show_progress_summary(self):
        """Show comprehensive progress summary"""
        summary = self.planner.get_progress_summary()
        
        print("\n=== KT Progress Summary ===\n")
        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Completed: {summary['completed_sessions']} ({summary['completion_rate']}%)")
        print(f"In Progress: {summary['in_progress_sessions']}")
        print(f"Pending: {summary['pending_sessions']}")
        print()
        print(f"Documents Uploaded: {summary['total_documents']}")
        print(f"Sessions with Documents: {summary['sessions_with_documents']}")
        print()
        print(f"Total Attendance: {summary['total_attended']}")
        print(f"Total Missed: {summary['total_missed']}")
        print(f"Attendance Rate: {summary['attendance_rate']}%")
        print()
    
    def generate_session_agenda(self, session_id: str):
        """Generate and display session agenda"""
        agenda = self.planner.generate_agenda(session_id)
        print(agenda)
    
    def breakdown_topic(self, topic: str, num_subtopics: int = 5):
        """Break down a topic into subtopics"""
        subtopics = self.planner.break_down_topic(topic, num_subtopics)
        
        print(f"\n=== Topic Breakdown: {topic} ===\n")
        for i, subtopic in enumerate(subtopics, 1):
            print(f"{i}. {subtopic}")
        print()


def main():
    """Main CLI entry point with enhanced features"""
    parser = argparse.ArgumentParser(description="Enhanced KT Planner - Knowledge Transfer Session Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Existing commands from base CLI
    create_parser = subparsers.add_parser('create', help='Create a new KT session')
    
    list_parser = subparsers.add_parser('list', help='List KT sessions')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--trainer', help='Filter by trainer')
    list_parser.add_argument('--trainee', help='Filter by trainee')
    list_parser.add_argument('--priority', help='Filter by priority')
    
    view_parser = subparsers.add_parser('view', help='View session details')
    view_parser.add_argument('session_id', help='Session ID')
    
    status_parser = subparsers.add_parser('status', help='Update session status')
    status_parser.add_argument('session_id', help='Session ID')
    status_parser.add_argument('new_status', help='New status', 
                              choices=[s.value for s in KTStatus])
    
    progress_parser = subparsers.add_parser('progress', help='Update session progress')
    progress_parser.add_argument('session_id', help='Session ID')
    progress_parser.add_argument('percentage', type=int, help='Completion percentage (0-100)')
    
    note_parser = subparsers.add_parser('note', help='Add a note to session')
    note_parser.add_argument('session_id', help='Session ID')
    note_parser.add_argument('note', help='Note text')
    
    upcoming_parser = subparsers.add_parser('upcoming', help='Show upcoming sessions')
    upcoming_parser.add_argument('--days', type=int, default=7, help='Number of days (default: 7)')
    
    overdue_parser = subparsers.add_parser('overdue', help='Show overdue sessions')
    
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    delete_parser = subparsers.add_parser('delete', help='Delete a session')
    delete_parser.add_argument('session_id', help='Session ID')
    
    # New enhanced commands
    attendance_parser = subparsers.add_parser('record-attendance', help='Record attendance for a session')
    attendance_parser.add_argument('session_id', help='Session ID')
    
    doc_parser = subparsers.add_parser('add-document', help='Add a document to a session')
    doc_parser.add_argument('session_id', help='Session ID')
    doc_parser.add_argument('name', help='Document name')
    doc_parser.add_argument('url', help='Document URL')
    doc_parser.add_argument('--description', help='Document description', default='')
    
    show_docs_parser = subparsers.add_parser('show-documents', help='Show documents for a session')
    show_docs_parser.add_argument('session_id', help='Session ID')
    
    reminders_parser = subparsers.add_parser('check-reminders', help='Check pending reminders')
    
    progress_summary_parser = subparsers.add_parser('progress-summary', help='Show comprehensive progress summary')
    
    agenda_parser = subparsers.add_parser('generate-agenda', help='Generate session agenda')
    agenda_parser.add_argument('session_id', help='Session ID')
    
    breakdown_parser = subparsers.add_parser('breakdown-topic', help='Break down a topic into subtopics')
    breakdown_parser.add_argument('topic', help='Topic to break down')
    breakdown_parser.add_argument('--num', type=int, default=5, help='Number of subtopics (default: 5)')
    
    wizard_parser = subparsers.add_parser('wizard', help='Launch interactive KT planning wizard')
    
    args = parser.parse_args()
    cli = EnhancedKTCli()
    
    # Handle commands
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
    elif args.command == 'record-attendance':
        cli.record_attendance_interactive(args.session_id)
    elif args.command == 'add-document':
        cli.add_document_to_session(args.session_id, args.name, args.url, args.description)
    elif args.command == 'show-documents':
        cli.show_session_documents(args.session_id)
    elif args.command == 'check-reminders':
        cli.check_reminders()
    elif args.command == 'progress-summary':
        cli.show_progress_summary()
    elif args.command == 'generate-agenda':
        cli.generate_session_agenda(args.session_id)
    elif args.command == 'breakdown-topic':
        cli.breakdown_topic(args.topic, args.num)
    elif args.command == 'wizard':
        print("Launching KT Planning Wizard...")
        print("Run: python kt_wizard.py")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# Made with Bob