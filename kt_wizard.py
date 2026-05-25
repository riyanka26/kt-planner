#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KT Planner Interactive Wizard
Guides users through creating comprehensive KT plans
"""

import sys
from datetime import datetime, timedelta
from typing import List, Optional
from kt_planner import KTPlanner, KTStatus, KTPriority

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class KTWizard:
    """Interactive wizard for creating KT plans"""
    
    def __init__(self):
        self.planner = KTPlanner()
        self.topics = []
        self.presenters = []
        self.participants = []
        self.start_date = None
        self.end_date = None
        self.duration = None
        self.time_preference = None
        self.num_sessions = None
        self.sessions_per_day = 1
    
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60 + "\n")
    
    def get_input(self, prompt: str, default: Optional[str] = None) -> str:
        """Get user input with optional default"""
        if default:
            response = input(f"{prompt} [{default}]: ").strip()
            return response if response else default
        return input(f"{prompt}: ").strip()
    
    def get_list_input(self, prompt: str, item_name: str = "item") -> List[str]:
        """Get list of items from user"""
        print(f"\n{prompt}")
        print(f"Enter {item_name}s one per line. Press Enter on empty line to finish.")
        items = []
        while True:
            item = input(f"  {len(items) + 1}. ").strip()
            if not item:
                break
            items.append(item)
        return items
    
    def collect_topics(self):
        """Collect KT topics from user"""
        self.print_header("Step 1: KT Topics")
        print("What topics do you want to cover in the KT sessions?")
        
        # Option to break down a high-level topic
        breakdown = self.get_input("Do you want to break down a high-level topic? (yes/no)", "no")
        
        if breakdown.lower() in ['yes', 'y']:
            high_level_topic = self.get_input("Enter the high-level topic")
            num_subtopics = int(self.get_input("How many subtopics?", "5"))
            self.topics = self.planner.break_down_topic(high_level_topic, num_subtopics)
            print(f"\nGenerated {len(self.topics)} subtopics:")
            for i, topic in enumerate(self.topics, 1):
                print(f"  {i}. {topic}")
            
            modify = self.get_input("\nWould you like to modify these? (yes/no)", "no")
            if modify.lower() in ['yes', 'y']:
                self.topics = self.get_list_input("Enter your topics", "topic")
        else:
            self.topics = self.get_list_input("Enter your topics", "topic")
        
        if not self.topics:
            print("Error: At least one topic is required!")
            sys.exit(1)
        
        print(f"\n[SUCCESS] Collected {len(self.topics)} topics")
    
    def collect_presenters(self):
        """Collect presenter information"""
        self.print_header("Step 2: Presenter(s)")
        print("Who will be presenting/training?")
        
        single_presenter = self.get_input("Is there a single presenter for all sessions? (yes/no)", "yes")
        
        if single_presenter.lower() in ['yes', 'y']:
            presenter = self.get_input("Enter presenter name")
            self.presenters = [presenter] * len(self.topics)
        else:
            print(f"\nYou have {len(self.topics)} topics. Assign a presenter to each:")
            for i, topic in enumerate(self.topics, 1):
                presenter = self.get_input(f"  {i}. {topic} - Presenter")
                self.presenters.append(presenter)
        
        print(f"\n[SUCCESS] Assigned presenters")
    
    def collect_participants(self):
        """Collect participant list"""
        self.print_header("Step 3: Participants")
        self.participants = self.get_list_input(
            "Who will be attending these KT sessions?",
            "participant"
        )
        
        if not self.participants:
            print("Warning: No participants specified. Using 'TBD'")
            self.participants = ["TBD"]
        
        print(f"\n[SUCCESS] Added {len(self.participants)} participants")
    
    def collect_date_range(self):
        """Collect preferred date range"""
        self.print_header("Step 4: Date Range")
        print("When would you like to schedule these sessions?")
        
        while True:
            start_str = self.get_input("Start date (YYYY-MM-DD)")
            try:
                self.start_date = datetime.strptime(start_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        while True:
            end_str = self.get_input("End date (YYYY-MM-DD)")
            try:
                self.end_date = datetime.strptime(end_str, "%Y-%m-%d")
                if self.end_date >= self.start_date:
                    break
                print("End date must be after start date")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        days_available = (self.end_date - self.start_date).days + 1
        print(f"\n[SUCCESS] Date range: {days_available} days")
    
    def collect_duration(self):
        """Collect session duration"""
        self.print_header("Step 5: Session Duration")
        print("How long should each session be?")
        print("  1. 30 minutes")
        print("  2. 1 hour")
        print("  3. 2 hours")
        print("  4. Custom")
        
        choice = self.get_input("Select option (1-4)", "2")
        
        duration_map = {
            '1': 0.5,
            '2': 1.0,
            '3': 2.0
        }
        
        if choice in duration_map:
            self.duration = duration_map[choice]
        else:
            while True:
                try:
                    self.duration = float(self.get_input("Enter duration in hours"))
                    if self.duration > 0:
                        break
                    print("Duration must be positive")
                except ValueError:
                    print("Invalid number")
        
        print(f"\n[SUCCESS] Session duration: {self.duration} hours")
    
    def collect_time_preference(self):
        """Collect time preferences"""
        self.print_header("Step 6: Time Preferences")
        print("Do you have a preferred time slot for sessions?")
        print("Examples: '9 AM - 11 AM', '2 PM - 4 PM', '3 PM - 5 PM'")
        
        has_preference = self.get_input("Specify time preference? (yes/no)", "no")
        
        if has_preference.lower() in ['yes', 'y']:
            self.time_preference = self.get_input("Enter time preference (e.g., '3 PM - 5 PM')")
        else:
            self.time_preference = None
        
        print(f"\n[SUCCESS] Time preference: {self.time_preference or 'Flexible'}")
    
    def collect_sessions_per_day(self):
        """Collect number of sessions per day"""
        self.print_header("Step 7: Sessions Per Day")
        print("How many sessions would you like per day?")
        
        while True:
            try:
                self.sessions_per_day = int(self.get_input("Sessions per day", "1"))
                if self.sessions_per_day > 0:
                    break
                print("Must be at least 1")
            except ValueError:
                print("Invalid number")
        
        print(f"\n[SUCCESS] {self.sessions_per_day} session(s) per day")
    
    def generate_schedule(self):
        """Generate the KT schedule"""
        self.print_header("Generating KT Schedule")
        print("Creating sessions with smart scheduling...")
        
        # Use the first presenter if all are the same, otherwise use "Multiple"
        trainer = self.presenters[0] if len(set(self.presenters)) == 1 else "Multiple Presenters"
        
        try:
            sessions = self.planner.schedule_sessions(
                topics=self.topics,
                trainer=trainer,
                participants=self.participants,
                start_date=self.start_date.strftime("%Y-%m-%d"),
                end_date=self.end_date.strftime("%Y-%m-%d"),
                duration_hours=self.duration,
                time_preference=self.time_preference,
                sessions_per_day=self.sessions_per_day,
                buffer_hours=2
            )
            
            # Assign specific presenters if different
            if len(set(self.presenters)) > 1:
                for i, session in enumerate(sessions):
                    if i < len(self.presenters):
                        session.trainer = self.presenters[i]
                        self.planner.save_sessions()
            
            return sessions
        except Exception as e:
            print(f"Error generating schedule: {e}")
            return []
    
    def display_schedule(self, sessions: List):
        """Display the generated schedule"""
        self.print_header("KT Schedule Generated")
        print(f"Total Sessions: {len(sessions)}\n")
        
        for i, session in enumerate(sessions, 1):
            print(f"{i}. {session.title}")
            print(f"   Presenter: {session.trainer}")
            print(f"   Date & Time: {session.scheduled_date}")
            print(f"   Duration: {session.duration_hours} hours")
            print(f"   Participants: {', '.join(session.participants)}")
            if session.time_preference:
                print(f"   Time Slot: {session.time_preference}")
            print()
    
    def setup_reminders(self, sessions: List):
        """Setup reminders for sessions"""
        self.print_header("Reminder Setup")
        setup = self.get_input("Would you like reminders to be scheduled? (yes/no)", "yes")
        
        if setup.lower() in ['yes', 'y']:
            for session in sessions:
                self.planner.setup_reminders(session.session_id)
            print(f"\n[SUCCESS] Reminders set up for all {len(sessions)} sessions")
            print("  - 1 day before each session")
            print("  - 1 hour before each session")
        else:
            print("\n[SKIPPED] No reminders set up")
    
    def setup_document_tracking(self):
        """Setup document upload tracking"""
        self.print_header("Document Upload List")
        setup = self.get_input("Would you like me to generate a KT document upload list? (yes/no)", "yes")
        
        if setup.lower() in ['yes', 'y']:
            print("\n[SUCCESS] Document upload tracking enabled")
            print("\nAfter each session, you can upload documents using:")
            print("  python kt_cli.py add-document <session-id> <document-name> <url>")
        else:
            print("\n[SKIPPED] Document tracking not enabled")
    
    def setup_attendance_tracking(self):
        """Setup attendance tracking"""
        self.print_header("Attendance Tracking")
        setup = self.get_input("Should I create an attendance tracker? (yes/no)", "yes")
        
        if setup.lower() in ['yes', 'y']:
            print("\n[SUCCESS] Attendance tracking enabled")
            print("\nAfter each session, you can record attendance using:")
            print("  python kt_cli.py record-attendance <session-id>")
        else:
            print("\n[SKIPPED] Attendance tracking not enabled")
    
    def show_next_steps(self, sessions: List):
        """Show next steps to user"""
        self.print_header("Next Steps")
        print("Your KT plan has been created successfully!")
        print("\nUseful Commands:")
        print(f"  - View all sessions: python kt_cli.py list")
        print(f"  - View session details: python kt_cli.py view <session-id>")
        print(f"  - Update status: python kt_cli.py status <session-id> 'In Progress'")
        print(f"  - Update progress: python kt_cli.py progress <session-id> <percentage>")
        print(f"  - Add notes: python kt_cli.py note <session-id> '<note text>'")
        print(f"  - View statistics: python kt_cli.py stats")
        print(f"  - View progress: python kt_cli.py progress-summary")
        print(f"  - Check reminders: python kt_cli.py check-reminders")
        print(f"\nFirst session: {sessions[0].session_id} on {sessions[0].scheduled_date}")
    
    def run(self):
        """Run the interactive wizard"""
        self.print_header("KT Planner Interactive Wizard")
        print("Welcome! This wizard will help you create a comprehensive KT plan.")
        print("Let's get started!\n")
        
        try:
            # Collect all information
            self.collect_topics()
            self.collect_presenters()
            self.collect_participants()
            self.collect_date_range()
            self.collect_duration()
            self.collect_time_preference()
            self.collect_sessions_per_day()
            
            # Generate schedule
            sessions = self.generate_schedule()
            
            if not sessions:
                print("\n[ERROR] Failed to generate schedule")
                return
            
            # Display schedule
            self.display_schedule(sessions)
            
            # Setup additional features
            self.setup_reminders(sessions)
            self.setup_document_tracking()
            self.setup_attendance_tracking()
            
            # Show next steps
            self.show_next_steps(sessions)
            
            self.print_header("Setup Complete!")
            print("Your KT plan is ready. Good luck with your knowledge transfer sessions!")
            
        except KeyboardInterrupt:
            print("\n\n[CANCELLED] Wizard cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERROR] An error occurred: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point"""
    wizard = KTWizard()
    wizard.run()


if __name__ == "__main__":
    main()

# Made with Bob