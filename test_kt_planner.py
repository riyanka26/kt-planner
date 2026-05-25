#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for KT Planner
Run this to verify the application works correctly
"""

import os
import sys
import json
from datetime import datetime, timedelta
from kt_planner import KTPlanner, KTSession, KTStatus, KTPriority

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_session_creation():
    """Test creating a KT session"""
    print("Testing session creation...")
    session = KTSession(
        session_id="TEST-001",
        title="Test Session",
        description="Test description",
        trainer="Alice",
        trainee="Bob",
        scheduled_date="2026-06-01 10:00",
        duration_hours=2.5,
        topics=["Topic 1", "Topic 2"],
        priority="High"
    )
    
    assert session.session_id == "TEST-001"
    assert session.title == "Test Session"
    assert session.status == "Planned"
    assert session.completion_percentage == 0
    print("[PASS] Session creation test passed")


def test_session_to_dict():
    """Test session serialization"""
    print("Testing session serialization...")
    session = KTSession(
        session_id="TEST-002",
        title="Test Session 2",
        description="Test description 2",
        trainer="Carol",
        trainee="David",
        scheduled_date="2026-06-02 14:00",
        duration_hours=3,
        topics=["Topic A", "Topic B"],
        priority="Medium"
    )
    
    data = session.to_dict()
    assert isinstance(data, dict)
    assert data['session_id'] == "TEST-002"
    assert data['title'] == "Test Session 2"
    print("[PASS] Session serialization test passed")


def test_session_from_dict():
    """Test session deserialization"""
    print("Testing session deserialization...")
    data = {
        'session_id': 'TEST-003',
        'title': 'Test Session 3',
        'description': 'Test description 3',
        'trainer': 'Eve',
        'trainee': 'Frank',
        'scheduled_date': '2026-06-03 09:00',
        'duration_hours': 1.5,
        'topics': ['Topic X', 'Topic Y'],
        'priority': 'Low',
        'status': 'Planned',
        'prerequisites': [],
        'materials': [],
        'notes': '',
        'completion_percentage': 0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    session = KTSession.from_dict(data)
    assert session.session_id == "TEST-003"
    assert session.title == "Test Session 3"
    assert len(session.topics) == 2
    print("[PASS] Session deserialization test passed")


def test_session_update_status():
    """Test updating session status"""
    print("Testing session status update...")
    session = KTSession(
        session_id="TEST-004",
        title="Test Session 4",
        description="Test",
        trainer="Alice",
        trainee="Bob",
        scheduled_date="2026-06-04 10:00",
        duration_hours=2,
        topics=["Topic 1"]
    )
    
    session.update_status(KTStatus.IN_PROGRESS.value)
    assert session.status == KTStatus.IN_PROGRESS.value
    print("[PASS] Session status update test passed")


def test_session_update_progress():
    """Test updating session progress"""
    print("Testing session progress update...")
    session = KTSession(
        session_id="TEST-005",
        title="Test Session 5",
        description="Test",
        trainer="Alice",
        trainee="Bob",
        scheduled_date="2026-06-05 10:00",
        duration_hours=2,
        topics=["Topic 1"]
    )
    
    session.update_progress(50)
    assert session.completion_percentage == 50
    
    session.update_progress(100)
    assert session.completion_percentage == 100
    assert session.status == KTStatus.COMPLETED.value
    print("[PASS] Session progress update test passed")


def test_session_add_note():
    """Test adding notes to session"""
    print("Testing adding notes...")
    session = KTSession(
        session_id="TEST-006",
        title="Test Session 6",
        description="Test",
        trainer="Alice",
        trainee="Bob",
        scheduled_date="2026-06-06 10:00",
        duration_hours=2,
        topics=["Topic 1"]
    )
    
    session.add_note("This is a test note")
    assert "This is a test note" in session.notes
    print("[PASS] Adding notes test passed")


def test_planner_create_session():
    """Test creating session through planner"""
    print("Testing planner session creation...")
    test_file = "test_sessions.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    planner = KTPlanner(data_file=test_file)
    
    session = planner.create_session(
        title="Planner Test Session",
        description="Testing planner",
        trainer="Alice",
        trainee="Bob",
        scheduled_date="2026-06-07 10:00",
        duration_hours=2,
        topics=["Topic 1", "Topic 2"],
        priority="High"
    )
    
    assert session.session_id == "KT-0001"
    assert len(planner.sessions) == 1
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("[PASS] Planner session creation test passed")


def test_planner_save_load():
    """Test saving and loading sessions"""
    print("Testing save and load...")
    test_file = "test_sessions_save_load.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create planner and add sessions
    planner1 = KTPlanner(data_file=test_file)
    planner1.create_session(
        title="Session 1",
        description="Test 1",
        trainer="Alice",
        trainee="Bob",
        scheduled_date="2026-06-08 10:00",
        duration_hours=2,
        topics=["Topic 1"]
    )
    planner1.create_session(
        title="Session 2",
        description="Test 2",
        trainer="Carol",
        trainee="David",
        scheduled_date="2026-06-09 14:00",
        duration_hours=3,
        topics=["Topic 2"]
    )
    
    # Load in new planner instance
    planner2 = KTPlanner(data_file=test_file)
    assert len(planner2.sessions) == 2
    assert "KT-0001" in planner2.sessions
    assert "KT-0002" in planner2.sessions
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("[PASS] Save and load test passed")


def test_planner_list_sessions():
    """Test listing and filtering sessions"""
    print("Testing session listing and filtering...")
    test_file = "test_sessions_list.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    planner = KTPlanner(data_file=test_file)
    
    # Create multiple sessions
    s1 = planner.create_session(
        title="Session 1", description="Test", trainer="Alice", trainee="Bob",
        scheduled_date="2026-06-10 10:00", duration_hours=2, topics=["T1"], priority="High"
    )
    s2 = planner.create_session(
        title="Session 2", description="Test", trainer="Carol", trainee="David",
        scheduled_date="2026-06-11 14:00", duration_hours=3, topics=["T2"], priority="Low"
    )
    s3 = planner.create_session(
        title="Session 3", description="Test", trainer="Alice", trainee="Eve",
        scheduled_date="2026-06-12 09:00", duration_hours=1, topics=["T3"], priority="High"
    )
    
    # Update one session status
    s1.update_status(KTStatus.IN_PROGRESS.value)
    planner.save_sessions()
    
    # Test listing all
    all_sessions = planner.list_sessions()
    assert len(all_sessions) == 3
    
    # Test filtering by status
    in_progress = planner.list_sessions(status=KTStatus.IN_PROGRESS.value)
    assert len(in_progress) == 1
    
    # Test filtering by trainer
    alice_sessions = planner.list_sessions(trainer="Alice")
    assert len(alice_sessions) == 2
    
    # Test filtering by priority
    high_priority = planner.list_sessions(priority="High")
    assert len(high_priority) == 2
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("[PASS] Session listing and filtering test passed")


def test_planner_upcoming_sessions():
    """Test getting upcoming sessions"""
    print("Testing upcoming sessions...")
    test_file = "test_sessions_upcoming.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    planner = KTPlanner(data_file=test_file)
    
    # Create sessions with different dates
    today = datetime.now()
    planner.create_session(
        title="Tomorrow", description="Test", trainer="Alice", trainee="Bob",
        scheduled_date=(today + timedelta(days=1)).strftime("%Y-%m-%d 10:00"),
        duration_hours=2, topics=["T1"]
    )
    planner.create_session(
        title="Next Week", description="Test", trainer="Carol", trainee="David",
        scheduled_date=(today + timedelta(days=5)).strftime("%Y-%m-%d 14:00"),
        duration_hours=3, topics=["T2"]
    )
    planner.create_session(
        title="Far Future", description="Test", trainer="Eve", trainee="Frank",
        scheduled_date=(today + timedelta(days=30)).strftime("%Y-%m-%d 09:00"),
        duration_hours=1, topics=["T3"]
    )
    
    # Get upcoming sessions (next 7 days)
    upcoming = planner.get_upcoming_sessions(days=7)
    assert len(upcoming) == 2  # Should get first two sessions
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("[PASS] Upcoming sessions test passed")


def test_planner_statistics():
    """Test statistics generation"""
    print("Testing statistics...")
    test_file = "test_sessions_stats.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    planner = KTPlanner(data_file=test_file)
    
    # Create sessions with different statuses and priorities
    s1 = planner.create_session(
        title="S1", description="Test", trainer="Alice", trainee="Bob",
        scheduled_date="2026-06-15 10:00", duration_hours=2, topics=["T1"], priority="High"
    )
    s2 = planner.create_session(
        title="S2", description="Test", trainer="Carol", trainee="David",
        scheduled_date="2026-06-16 14:00", duration_hours=3, topics=["T2"], priority="Low"
    )
    s3 = planner.create_session(
        title="S3", description="Test", trainer="Eve", trainee="Frank",
        scheduled_date="2026-06-17 09:00", duration_hours=1, topics=["T3"], priority="High"
    )
    
    s1.update_status(KTStatus.COMPLETED.value)
    s1.update_progress(100)
    s2.update_status(KTStatus.IN_PROGRESS.value)
    s2.update_progress(50)
    planner.save_sessions()
    
    stats = planner.get_statistics()
    
    assert stats['total_sessions'] == 3
    assert stats['by_status'][KTStatus.COMPLETED.value] == 1
    assert stats['by_status'][KTStatus.IN_PROGRESS.value] == 1
    assert stats['by_priority']['High'] == 2
    assert stats['by_priority']['Low'] == 1
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("[PASS] Statistics test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("KT Planner Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_session_creation,
        test_session_to_dict,
        test_session_from_dict,
        test_session_update_status,
        test_session_update_progress,
        test_session_add_note,
        test_planner_create_session,
        test_planner_save_load,
        test_planner_list_sessions,
        test_planner_upcoming_sessions,
        test_planner_statistics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    if failed == 0:
        print("SUCCESS: All tests passed! The KT Planner is working correctly.")
        return True
    else:
        print("WARNING: Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

# Made with Bob
