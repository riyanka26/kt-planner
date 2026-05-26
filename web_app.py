"""
KT Planner Web Application
Flask-based web interface for the KT Planner system
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from kt_planner import KTPlanner, KTSession
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

# Initialize planner
planner = KTPlanner()

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all KT sessions"""
    try:
        sessions = planner.list_sessions()
        return jsonify({
            'success': True,
            'sessions': sessions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create a new KT session"""
    try:
        data = request.json
        
        # Create session using planner's create_session method
        session = planner.create_session(
            title=data['title'],
            description=data.get('description', ''),
            trainer=data['trainer'],
            trainee=data.get('trainee', ''),
            scheduled_date=data['scheduled_date'],
            duration_hours=float(data['duration_hours']),
            topics=data.get('topics', []),
            priority=data.get('priority', 'Medium'),
            participants=data.get('participants', []),
            time_preference=data.get('time_preference')
        )
        
        return jsonify({
            'success': True,
            'message': 'Session created successfully',
            'session_id': session.session_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific session"""
    try:
        session = planner.get_session(session_id)
        if session:
            return jsonify({
                'success': True,
                'session': session.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>', methods=['PUT'])
def update_session(session_id):
    """Update a session"""
    try:
        data = request.json
        session = planner.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Update fields using planner's update_session method
        update_fields = {}
        if 'title' in data:
            update_fields['title'] = data['title']
        if 'trainer' in data:
            update_fields['trainer'] = data['trainer']
        if 'trainee' in data:
            update_fields['trainee'] = data['trainee']
        if 'scheduled_date' in data:
            update_fields['scheduled_date'] = data['scheduled_date']
        if 'duration_hours' in data:
            update_fields['duration_hours'] = float(data['duration_hours'])
        if 'status' in data:
            update_fields['status'] = data['status']
        if 'participants' in data:
            update_fields['participants'] = data['participants']
        if 'description' in data:
            update_fields['description'] = data['description']
        if 'topics' in data:
            update_fields['topics'] = data['topics']
        
        planner.update_session(session_id, **update_fields)
        
        return jsonify({
            'success': True,
            'message': 'Session updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session"""
    try:
        success = planner.delete_session(session_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Session deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>/attendance', methods=['POST'])
def record_attendance(session_id):
    """Record attendance for a session"""
    try:
        data = request.json
        session = planner.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session.record_attendance(
            attended=data.get('attended', []),
            missed=data.get('missed', []),
            follow_up=data.get('follow_up')
        )
        planner.save_sessions()
        
        return jsonify({
            'success': True,
            'message': 'Attendance recorded successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/sessions/<session_id>/documents', methods=['POST'])
def add_document(session_id):
    """Add a document to a session"""
    try:
        data = request.json
        session = planner.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session.add_document(
            name=data['name'],
            url=data['url'],
            description=data.get('description', '')
        )
        planner.save_sessions()
        
        return jsonify({
            'success': True,
            'message': 'Document added successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    """Get pending reminders"""
    try:
        reminders = planner.get_pending_reminders()
        return jsonify({
            'success': True,
            'reminders': reminders
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get progress summary"""
    try:
        summary = planner.get_progress_summary()
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/schedule', methods=['POST'])
def schedule_sessions():
    """Auto-schedule multiple sessions"""
    try:
        data = request.json
        
        topics = data['topics']
        trainer = data['trainer']
        participants = data.get('participants', [])
        start_date = data['start_date']
        end_date = data['end_date']
        duration_hours = float(data['duration_hours'])
        time_preference = data.get('time_preference')
        
        sessions = planner.schedule_sessions(
            topics=topics,
            trainer=trainer,
            participants=participants,
            start_date=start_date,
            end_date=end_date,
            duration_hours=duration_hours,
            time_preference=time_preference
        )
        
        return jsonify({
            'success': True,
            'message': f'{len(sessions)} sessions scheduled successfully',
            'sessions': [s.to_dict() for s in sessions]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ai/breakdown', methods=['POST'])
def breakdown_topic():
    """Break down a topic into subtopics"""
    try:
        data = request.json
        topic = data['topic']
        num_sessions = int(data.get('num_sessions', 3))
        
        subtopics = planner.break_down_topic(topic, num_sessions)
        
        return jsonify({
            'success': True,
            'subtopics': subtopics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ai/agenda', methods=['POST'])
def generate_agenda():
    """Generate agenda for a session"""
    try:
        data = request.json
        session_id = data['session_id']
        
        agenda = planner.generate_agenda(session_id)
        
        return jsonify({
            'success': True,
            'agenda': agenda
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    # Run on all network interfaces (0.0.0.0) to allow global access
    # Access via: http://localhost:5000 or http://YOUR_IP:5000
    import sys
    import io
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "="*60)
    print("KT Planner Web Server Starting...")
    print("="*60)
    print("\nAccess the web interface at:")
    print("   * Local:    http://localhost:5000")
    print("   * Local:    http://127.0.0.1:5000")
    print("\nTo access from other devices on your network:")
    print("   * Find your IP address (run: ipconfig)")
    print("   * Use:      http://YOUR_IP_ADDRESS:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
