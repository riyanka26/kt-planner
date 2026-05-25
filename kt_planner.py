#!/usr/bin/env python3
"""
KT (Knowledge Transfer) Planner
A comprehensive tool to create, organize, track, and manage KT sessions.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum


class KTStatus(Enum):
    """Status of a KT session"""
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    POSTPONED = "Postponed"


class KTPriority(Enum):
    """Priority levels for KT sessions"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class KTSession:
    """Represents a single KT session"""
    
    def __init__(self, session_id: str, title: str, description: str,
                 trainer: str, trainee: str, scheduled_date: str,
                 duration_hours: float, topics: List[str],
                 priority: str = "Medium", status: str = "Planned",
                 prerequisites: Optional[List[str]] = None, materials: Optional[List[str]] = None,
                 notes: str = "", completion_percentage: int = 0,
                 participants: Optional[List[str]] = None,
                 time_preference: Optional[str] = None,
                 reminders: Optional[List[Dict]] = None,
                 attendance: Optional[Dict] = None,
                 documents: Optional[List[Dict]] = None):
        self.session_id = session_id
        self.title = title
        self.description = description
        self.trainer = trainer
        self.trainee = trainee
        self.scheduled_date = scheduled_date
        self.duration_hours = duration_hours
        self.topics = topics
        self.priority = priority
        self.status = status
        self.prerequisites = prerequisites or []
        self.materials = materials or []
        self.notes = notes
        self.completion_percentage = completion_percentage
        self.participants = participants or []  # List of participant names
        self.time_preference = time_preference  # e.g., "3 PM - 5 PM"
        self.reminders = reminders or []  # List of reminder dicts with 'type' and 'sent' status
        self.attendance = attendance or {}  # Dict with 'attended', 'missed', 'follow_up'
        self.documents = documents or []  # List of document dicts with 'name', 'url', 'uploaded_at'
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'title': self.title,
            'description': self.description,
            'trainer': self.trainer,
            'trainee': self.trainee,
            'scheduled_date': self.scheduled_date,
            'duration_hours': self.duration_hours,
            'topics': self.topics,
            'priority': self.priority,
            'status': self.status,
            'prerequisites': self.prerequisites,
            'materials': self.materials,
            'notes': self.notes,
            'completion_percentage': self.completion_percentage,
            'participants': self.participants,
            'time_preference': self.time_preference,
            'reminders': self.reminders,
            'attendance': self.attendance,
            'documents': self.documents,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KTSession':
        """Create session from dictionary"""
        session = cls(
            session_id=data['session_id'],
            title=data['title'],
            description=data['description'],
            trainer=data['trainer'],
            trainee=data['trainee'],
            scheduled_date=data['scheduled_date'],
            duration_hours=data['duration_hours'],
            topics=data['topics'],
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'Planned'),
            prerequisites=data.get('prerequisites', []),
            materials=data.get('materials', []),
            notes=data.get('notes', ''),
            completion_percentage=data.get('completion_percentage', 0),
            participants=data.get('participants', []),
            time_preference=data.get('time_preference'),
            reminders=data.get('reminders', []),
            attendance=data.get('attendance', {}),
            documents=data.get('documents', [])
        )
        session.created_at = data.get('created_at', session.created_at)
        session.updated_at = data.get('updated_at', session.updated_at)
        return session
    
    def update_status(self, new_status: str):
        """Update session status"""
        self.status = new_status
        self.updated_at = datetime.now().isoformat()
    
    def update_progress(self, percentage: int):
        """Update completion percentage"""
        self.completion_percentage = max(0, min(100, percentage))
        self.updated_at = datetime.now().isoformat()
        if self.completion_percentage == 100:
            self.status = KTStatus.COMPLETED.value
    
    def add_note(self, note: str):
        """Add a note to the session"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notes += f"\n[{timestamp}] {note}"
        self.updated_at = datetime.now().isoformat()
    
    def add_reminder(self, reminder_type: str):
        """Add a reminder (1_day_before or 1_hour_before)"""
        reminder = {
            'type': reminder_type,
            'sent': False,
            'created_at': datetime.now().isoformat()
        }
        self.reminders.append(reminder)
        self.updated_at = datetime.now().isoformat()
    
    def mark_reminder_sent(self, reminder_type: str):
        """Mark a reminder as sent"""
        for reminder in self.reminders:
            if reminder['type'] == reminder_type:
                reminder['sent'] = True
                reminder['sent_at'] = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def record_attendance(self, attended: List[str], missed: List[str], follow_up: Optional[str] = None):
        """Record attendance for the session"""
        self.attendance = {
            'attended': attended,
            'missed': missed,
            'follow_up': follow_up or '',
            'recorded_at': datetime.now().isoformat()
        }
        self.updated_at = datetime.now().isoformat()
    
    def add_document(self, name: str, url: str, description: Optional[str] = None):
        """Add a document to the session"""
        document = {
            'name': name,
            'url': url,
            'description': description or '',
            'uploaded_at': datetime.now().isoformat()
        }
        self.documents.append(document)
        self.updated_at = datetime.now().isoformat()


class KTPlanner:
    """Main KT Planner class for managing KT sessions"""
    
    def __init__(self, data_file: str = "kt_sessions.json"):
        self.data_file = data_file
        self.sessions: Dict[str, KTSession] = {}
        self.load_sessions()
    
    def load_sessions(self):
        """Load sessions from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.sessions = {
                        sid: KTSession.from_dict(sdata)
                        for sid, sdata in data.items()
                    }
            except Exception as e:
                print(f"Error loading sessions: {e}")
                self.sessions = {}
        else:
            self.sessions = {}
    
    def save_sessions(self):
        """Save sessions to JSON file"""
        try:
            data = {sid: session.to_dict() for sid, session in self.sessions.items()}
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def create_session(self, title: str, description: str, trainer: str,
                      trainee: str, scheduled_date: str, duration_hours: float,
                      topics: List[str], priority: str = "Medium",
                      prerequisites: Optional[List[str]] = None,
                      materials: Optional[List[str]] = None,
                      participants: Optional[List[str]] = None,
                      time_preference: Optional[str] = None) -> KTSession:
        """Create a new KT session"""
        session_id = f"KT-{len(self.sessions) + 1:04d}"
        session = KTSession(
            session_id=session_id,
            title=title,
            description=description,
            trainer=trainer,
            trainee=trainee,
            scheduled_date=scheduled_date,
            duration_hours=duration_hours,
            topics=topics,
            priority=priority,
            prerequisites=prerequisites,
            materials=materials,
            participants=participants,
            time_preference=time_preference
        )
        self.sessions[session_id] = session
        self.save_sessions()
        return session
    
    def get_session(self, session_id: str) -> Optional[KTSession]:
        """Get a session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, **kwargs):
        """Update session attributes"""
        session = self.get_session(session_id)
        if session:
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            session.updated_at = datetime.now().isoformat()
            self.save_sessions()
            return session
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()
            return True
        return False
    
    def list_sessions(self, status: Optional[str] = None,
                     trainer: Optional[str] = None,
                     trainee: Optional[str] = None,
                     priority: Optional[str] = None) -> List[KTSession]:
        """List sessions with optional filters"""
        sessions = list(self.sessions.values())
        
        if status:
            sessions = [s for s in sessions if s.status == status]
        if trainer:
            sessions = [s for s in sessions if s.trainer.lower() == trainer.lower()]
        if trainee:
            sessions = [s for s in sessions if s.trainee.lower() == trainee.lower()]
        if priority:
            sessions = [s for s in sessions if s.priority == priority]
        
        return sessions
    
    def get_upcoming_sessions(self, days: int = 7) -> List[KTSession]:
        """Get sessions scheduled in the next N days"""
        today = datetime.now().date()
        future_date = today + timedelta(days=days)
        
        upcoming = []
        for session in self.sessions.values():
            try:
                session_date = datetime.fromisoformat(session.scheduled_date).date()
                if today <= session_date <= future_date and session.status != KTStatus.COMPLETED.value:
                    upcoming.append(session)
            except:
                pass
        
        return sorted(upcoming, key=lambda s: s.scheduled_date)
    
    def get_overdue_sessions(self) -> List[KTSession]:
        """Get sessions that are past their scheduled date but not completed"""
        today = datetime.now().date()
        overdue = []
        
        for session in self.sessions.values():
            try:
                session_date = datetime.fromisoformat(session.scheduled_date).date()
                if session_date < today and session.status not in [KTStatus.COMPLETED.value, KTStatus.CANCELLED.value]:
                    overdue.append(session)
            except:
                pass
        
        return sorted(overdue, key=lambda s: s.scheduled_date)
    
    def get_statistics(self) -> Dict:
        """Get statistics about KT sessions"""
        total = len(self.sessions)
        by_status = {}
        by_priority = {}
        
        for session in self.sessions.values():
            by_status[session.status] = by_status.get(session.status, 0) + 1
            by_priority[session.priority] = by_priority.get(session.priority, 0) + 1
        
        avg_completion = sum(s.completion_percentage for s in self.sessions.values()) / total if total > 0 else 0
        
        return {
            'total_sessions': total,
            'by_status': by_status,
            'by_priority': by_priority,
            'average_completion': round(avg_completion, 2),
            'upcoming_count': len(self.get_upcoming_sessions()),
            'overdue_count': len(self.get_overdue_sessions())
        }
    
    def is_weekend(self, date: datetime) -> bool:
        """Check if a date falls on weekend"""
        return date.weekday() >= 5  # Saturday=5, Sunday=6
    
    def get_next_weekday(self, date: datetime) -> datetime:
        """Get next weekday if date is weekend"""
        while self.is_weekend(date):
            date += timedelta(days=1)
        return date
    
    def schedule_sessions(self, topics: List[str], trainer: str, participants: List[str],
                         start_date: str, end_date: str, duration_hours: float,
                         time_preference: Optional[str] = None, sessions_per_day: int = 1,
                         buffer_hours: int = 2) -> List[KTSession]:
        """
        Schedule multiple KT sessions with smart scheduling rules
        
        Args:
            topics: List of topics to cover
            trainer: Trainer name
            participants: List of participant names
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            duration_hours: Duration of each session
            time_preference: Preferred time slot (e.g., "3 PM - 5 PM")
            sessions_per_day: Maximum sessions per day
            buffer_hours: Buffer time between sessions
        
        Returns:
            List of created KTSession objects
        """
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        # Skip weekends for start date
        current_date = self.get_next_weekday(start)
        
        created_sessions = []
        sessions_today = 0
        last_session_end = None
        
        for i, topic in enumerate(topics):
            # Check if we need to move to next day
            if sessions_today >= sessions_per_day:
                current_date += timedelta(days=1)
                current_date = self.get_next_weekday(current_date)
                sessions_today = 0
                last_session_end = None
            
            # Check if we're within date range
            if current_date.date() > end.date():
                print(f"Warning: Not enough days to schedule all sessions. {len(topics) - i} topics remaining.")
                break
            
            # Determine session time
            if time_preference:
                # Parse time preference (e.g., "3 PM - 5 PM")
                time_parts = time_preference.split('-')[0].strip()
                try:
                    if 'PM' in time_parts.upper():
                        hour = int(time_parts.split()[0])
                        if hour != 12:
                            hour += 12
                    else:
                        hour = int(time_parts.split()[0])
                    session_time = current_date.replace(hour=hour, minute=0, second=0)
                except:
                    session_time = current_date.replace(hour=14, minute=0, second=0)  # Default 2 PM
            else:
                session_time = current_date.replace(hour=14, minute=0, second=0)  # Default 2 PM
            
            # Add buffer time if there was a previous session today
            if last_session_end:
                session_time = max(session_time, last_session_end + timedelta(hours=buffer_hours))
            
            # Create session
            session = self.create_session(
                title=f"KT Session: {topic}",
                description=f"Knowledge transfer session covering {topic}",
                trainer=trainer,
                trainee=", ".join(participants),
                scheduled_date=session_time.strftime("%Y-%m-%d %H:%M"),
                duration_hours=duration_hours,
                topics=[topic],
                participants=participants,
                time_preference=time_preference
            )
            
            created_sessions.append(session)
            sessions_today += 1
            last_session_end = session_time + timedelta(hours=duration_hours)
        
        return created_sessions
    
    def setup_reminders(self, session_id: str):
        """Setup reminders for a session (1 day before and 1 hour before)"""
        session = self.get_session(session_id)
        if session:
            session.add_reminder('1_day_before')
            session.add_reminder('1_hour_before')
            self.save_sessions()
            return True
        return False
    
    def get_pending_reminders(self) -> List[Dict]:
        """Get all pending reminders that need to be sent"""
        pending = []
        now = datetime.now()
        
        for session in self.sessions.values():
            try:
                session_time = datetime.fromisoformat(session.scheduled_date)
                
                for reminder in session.reminders:
                    if not reminder['sent']:
                        if reminder['type'] == '1_day_before':
                            reminder_time = session_time - timedelta(days=1)
                            if now >= reminder_time:
                                pending.append({
                                    'session_id': session.session_id,
                                    'session_title': session.title,
                                    'reminder_type': '1_day_before',
                                    'scheduled_date': session.scheduled_date,
                                    'message': f"Reminder: KT session '{session.title}' is scheduled for tomorrow at {session.scheduled_date}"
                                })
                        elif reminder['type'] == '1_hour_before':
                            reminder_time = session_time - timedelta(hours=1)
                            if now >= reminder_time:
                                pending.append({
                                    'session_id': session.session_id,
                                    'session_title': session.title,
                                    'reminder_type': '1_hour_before',
                                    'scheduled_date': session.scheduled_date,
                                    'message': f"Reminder: KT session '{session.title}' starts in 1 hour at {session.scheduled_date}"
                                })
            except:
                pass
        
        return pending
    
    def get_progress_summary(self) -> Dict:
        """Get comprehensive progress summary"""
        total = len(self.sessions)
        completed = len([s for s in self.sessions.values() if s.status == KTStatus.COMPLETED.value])
        in_progress = len([s for s in self.sessions.values() if s.status == KTStatus.IN_PROGRESS.value])
        pending = len([s for s in self.sessions.values() if s.status == KTStatus.PLANNED.value])
        
        # Document statistics
        total_docs = sum(len(s.documents) for s in self.sessions.values())
        sessions_with_docs = len([s for s in self.sessions.values() if s.documents])
        
        # Attendance statistics
        total_attended = 0
        total_missed = 0
        for session in self.sessions.values():
            if session.attendance:
                total_attended += len(session.attendance.get('attended', []))
                total_missed += len(session.attendance.get('missed', []))
        
        return {
            'total_sessions': total,
            'completed_sessions': completed,
            'in_progress_sessions': in_progress,
            'pending_sessions': pending,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 2),
            'total_documents': total_docs,
            'sessions_with_documents': sessions_with_docs,
            'total_attended': total_attended,
            'total_missed': total_missed,
            'attendance_rate': round((total_attended / (total_attended + total_missed) * 100) if (total_attended + total_missed) > 0 else 0, 2)
        }
    
    def break_down_topic(self, topic: str, num_subtopics: int = 5) -> List[str]:
        """
        Break down a high-level topic into subtopics
        This is a simple implementation - can be enhanced with AI
        """
        # Common patterns for breaking down topics
        subtopic_templates = [
            f"{topic} - Introduction and Basics",
            f"{topic} - Core Concepts",
            f"{topic} - Advanced Features",
            f"{topic} - Best Practices",
            f"{topic} - Real-world Applications",
            f"{topic} - Common Pitfalls and Solutions",
            f"{topic} - Hands-on Practice",
            f"{topic} - Q&A and Review"
        ]
        
        return subtopic_templates[:num_subtopics]
    
    def generate_agenda(self, session_id: str) -> str:
        """Generate a KT session agenda"""
        session = self.get_session(session_id)
        if not session:
            return "Session not found"
        
        agenda = f"""
KT SESSION AGENDA
================

Session ID: {session.session_id}
Title: {session.title}
Date: {session.scheduled_date}
Duration: {session.duration_hours} hours
Trainer: {session.trainer}
Participants: {', '.join(session.participants) if session.participants else session.trainee}

OBJECTIVES
----------
{session.description}

TOPICS TO COVER
---------------
"""
        for i, topic in enumerate(session.topics, 1):
            agenda += f"{i}. {topic}\n"
        
        if session.prerequisites:
            agenda += "\nPREREQUISITES\n-------------\n"
            for prereq in session.prerequisites:
                agenda += f"• {prereq}\n"
        
        if session.materials:
            agenda += "\nMATERIALS NEEDED\n----------------\n"
            for material in session.materials:
                agenda += f"• {material}\n"
        
        agenda += "\nSESSION STRUCTURE\n-----------------\n"
        agenda += f"• Introduction (10 mins)\n"
        agenda += f"• Main Content ({int(session.duration_hours * 60 - 30)} mins)\n"
        agenda += f"• Q&A and Wrap-up (20 mins)\n"
        
        return agenda


if __name__ == "__main__":
    print("KT Planner - Use the CLI interface (kt_cli.py) to interact with the planner")

# Made with Bob
