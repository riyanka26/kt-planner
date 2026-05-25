#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for enhanced KT Planner features
"""

import sys
import os
from datetime import datetime, timedelta
from kt_planner import KTPlanner, KTStatus

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def test_enhanced_session_creation():
    """Test creating sessions with new fields"""
    print_header("Test 1: Enhanced Session Creation")
    
    planner = KTPlanner(data_file="test_enhanced.json")
    
    session = planner.create_session(
        title="Test Enhanced Session",
        description="Testing new features",
        trainer="Alice",
        trainee="Bob",
        scheduled_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d 14:00"),
        duration_hours=2.0,
        topics=["Topic 1", "Topic 2"],
        participants=["Bob", "Carol", "David"],
        time_preference="2 PM - 4 PM"
    )
    
    assert session.participants == ["Bob", "Carol", "David"]
    assert session.time_preference == "2 PM - 4 PM"
    assert session.reminders == []
    assert session.attendance == {}
    assert session.documents == []
    
    print(f"[PASS] Created session {session.session_id} with enhanced fields")
    print(f"  Participants: {session.participants}")
    print(f"  Time Preference: {session.time_preference}")
    
    # Cleanup
    if os.path.exists("test_enhanced.json"):
        os.remove("test_enhanced.json")
    
    return True


def test_reminders():
    """Test reminder functionality"""
    print_header("Test 2: Reminder System")
    
    planner = KTPlanner(data_file="test_reminders.json")
    
    session = planner.create_session(
        title="Test Reminders",
        description="Testing reminders",
        trainer="Alice",
        trainee="Bob",
        scheduled_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 14:00"),
        duration_hours=1.0,
        topics=["Topic 1"]
    )
    
    # Setup reminders
    planner.setup_reminders(session.session_id)
    
    # Reload session
    session = planner.get_session(session.session_id)
    
    assert len(session.reminders) == 2
    assert any(r['type'] == '1_day_before' for r in session.reminders)
    assert any(r['type'] == '1_hour_before' for r in session.reminders)
    
    print(f"[PASS] Reminders set up successfully")
    print(f"  Total reminders: {len(session.reminders)}")
    for reminder in session.reminders:
        print(f"  - {reminder['type']}: sent={reminder['sent']}")
    
    # Cleanup
    if os.path.exists("test_reminders.json"):
        os.remove("test_reminders.json")
    
    return True


def test_attendance():
    """Test attendance tracking"""
    print_header("Test 3: Attendance Tracking")
    
    planner = KTPlanner(data_file="test_attendance.json")
    
    session = planner.create_session(
        title="Test Attendance",
        description="Testing attendance",
        trainer="Alice",
        trainee="Bob",
        scheduled_date=datetime.now().strftime("%Y-%m-%d 14:00"),
        duration_hours=1.0,
        topics=["Topic 1"],
        participants=["Bob", "Carol", "David"]
    )
    
    # Record attendance
    session.record_attendance(
        attended=["Bob", "Carol"],
        missed=["David"],
        follow_up="Schedule makeup session for David"
    )
    planner.save_sessions()
    
    # Reload and verify
    session = planner.get_session(session.session_id)
    
    assert len(session.attendance['attended']) == 2
    assert len(session.attendance['missed']) == 1
    assert session.attendance['follow_up'] == "Schedule makeup session for David"
    
    print(f"[PASS] Attendance recorded successfully")
    print(f"  Attended: {session.attendance['attended']}")
    print(f"  Missed: {session.attendance['missed']}")
    print(f"  Follow-up: {session.attendance['follow_up']}")
    
    # Cleanup
    if os.path.exists("test_attendance.json"):
        os.remove("test_attendance.json")
    
    return True


def test_documents():
    """Test document management"""
    print_header("Test 4: Document Management")
    
    planner = KTPlanner(data_file="test_documents.json")
    
    session = planner.create_session(
        title="Test Documents",
        description="Testing documents",
        trainer="Alice",
        trainee="Bob",
        scheduled_date=datetime.now().strftime("%Y-%m-%d 14:00"),
        duration_hours=1.0,
        topics=["Topic 1"]
    )
    
    # Add documents
    session.add_document("Slides", "https://example.com/slides.pdf", "Main slides")
    session.add_document("Code", "https://github.com/example/repo", "Code examples")
    planner.save_sessions()
    
    # Reload and verify
    session = planner.get_session(session.session_id)
    
    assert len(session.documents) == 2
    assert session.documents[0]['name'] == "Slides"
    assert session.documents[1]['name'] == "Code"
    
    print(f"[PASS] Documents added successfully")
    print(f"  Total documents: {len(session.documents)}")
    for doc in session.documents:
        print(f"  - {doc['name']}: {doc['url']}")
    
    # Cleanup
    if os.path.exists("test_documents.json"):
        os.remove("test_documents.json")
    
    return True


def test_smart_scheduling():
    """Test smart scheduling"""
    print_header("Test 5: Smart Scheduling")
    
    planner = KTPlanner(data_file="test_scheduling.json")
    
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=14)
    
    sessions = planner.schedule_sessions(
        topics=["Topic 1", "Topic 2", "Topic 3"],
        trainer="Alice",
        participants=["Bob", "Carol"],
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        duration_hours=2.0,
        time_preference="2 PM - 4 PM",
        sessions_per_day=1,
        buffer_hours=2
    )
    
    assert len(sessions) == 3
    
    # Check no weekends
    for session in sessions:
        session_date = datetime.fromisoformat(session.scheduled_date)
        assert session_date.weekday() < 5, "Session scheduled on weekend!"
    
    print(f"[PASS] Smart scheduling working correctly")
    print(f"  Scheduled {len(sessions)} sessions")
    print(f"  All sessions on weekdays: YES")
    for session in sessions:
        print(f"  - {session.session_id}: {session.scheduled_date}")
    
    # Cleanup
    if os.path.exists("test_scheduling.json"):
        os.remove("test_scheduling.json")
    
    return True


def test_progress_summary():
    """Test progress summary"""
    print_header("Test 6: Progress Summary")
    
    planner = KTPlanner(data_file="test_progress.json")
    
    # Create multiple sessions with different statuses
    s1 = planner.create_session(
        title="Session 1", description="Test", trainer="Alice", trainee="Bob",
        scheduled_date=datetime.now().strftime("%Y-%m-%d 14:00"),
        duration_hours=1.0, topics=["T1"], participants=["Bob", "Carol"]
    )
    s1.update_status(KTStatus.COMPLETED.value)
    s1.update_progress(100)
    s1.record_attendance(["Bob", "Carol"], [], "")
    s1.add_document("Doc1", "url1")
    
    s2 = planner.create_session(
        title="Session 2", description="Test", trainer="Alice", trainee="Bob",
        scheduled_date=datetime.now().strftime("%Y-%m-%d 15:00"),
        duration_hours=1.0, topics=["T2"], participants=["Bob"]
    )
    s2.update_status(KTStatus.IN_PROGRESS.value)
    s2.update_progress(50)
    
    planner.save_sessions()
    
    # Get summary
    summary = planner.get_progress_summary()
    
    assert summary['total_sessions'] == 2
    assert summary['completed_sessions'] == 1
    assert summary['in_progress_sessions'] == 1
    assert summary['total_documents'] == 1
    assert summary['total_attended'] == 2
    
    print(f"[PASS] Progress summary generated successfully")
    print(f"  Total Sessions: {summary['total_sessions']}")
    print(f"  Completed: {summary['completed_sessions']}")
    print(f"  Completion Rate: {summary['completion_rate']}%")
    print(f"  Documents: {summary['total_documents']}")
    print(f"  Attendance Rate: {summary['attendance_rate']}%")
    
    # Cleanup
    if os.path.exists("test_progress.json"):
        os.remove("test_progress.json")
    
    return True


def test_topic_breakdown():
    """Test topic breakdown"""
    print_header("Test 7: Topic Breakdown")
    
    planner = KTPlanner()
    
    subtopics = planner.break_down_topic("Python Programming", 5)
    
    assert len(subtopics) == 5
    assert all("Python Programming" in topic for topic in subtopics)
    
    print(f"[PASS] Topic breakdown working correctly")
    print(f"  Generated {len(subtopics)} subtopics:")
    for i, topic in enumerate(subtopics, 1):
        print(f"  {i}. {topic}")
    
    return True


def test_agenda_generation():
    """Test agenda generation"""
    print_header("Test 8: Agenda Generation")
    
    planner = KTPlanner(data_file="test_agenda.json")
    
    session = planner.create_session(
        title="Test Agenda",
        description="Testing agenda generation",
        trainer="Alice",
        trainee="Bob",
        scheduled_date=datetime.now().strftime("%Y-%m-%d 14:00"),
        duration_hours=2.0,
        topics=["Topic 1", "Topic 2"],
        prerequisites=["Prereq 1"],
        materials=["Material 1"],
        participants=["Bob", "Carol"]
    )
    
    agenda = planner.generate_agenda(session.session_id)
    
    assert "KT SESSION AGENDA" in agenda
    assert session.title in agenda
    assert "Topic 1" in agenda
    assert "Prereq 1" in agenda
    
    print(f"[PASS] Agenda generated successfully")
    print(f"  Length: {len(agenda)} characters")
    print(f"  Contains session details: YES")
    
    # Cleanup
    if os.path.exists("test_agenda.json"):
        os.remove("test_agenda.json")
    
    return True


def run_all_tests():
    """Run all enhanced feature tests"""
    print_header("Enhanced KT Planner Feature Tests")
    
    tests = [
        test_enhanced_session_creation,
        test_reminders,
        test_attendance,
        test_documents,
        test_smart_scheduling,
        test_progress_summary,
        test_topic_breakdown,
        test_agenda_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print_header("Test Results")
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n[SUCCESS] All enhanced features working correctly!")
        return True
    else:
        print(f"\n[WARNING] {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

# Made with Bob