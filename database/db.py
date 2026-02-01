import sqlite3
import json
from datetime import datetime

DB_PATH = "incidents.db"

def init_db():
    start_time = datetime.now()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            incident_type TEXT,
            severity TEXT,
            reason TEXT,
            action TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
    # Check if empty (mock data for demo)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT count(*) FROM incidents')
    if c.fetchone()[0] == 0:
        # Seed some data
        mock_data = [
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "MEMORY_LEAK", "HIGH", "Garbage Collection Failure", "RESTART_SERVICE", "RESOLVED"),
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "API_TIMEOUT", "MEDIUM", "Latency > 500ms", "SCALE_UP", "RESOLVED"),
        ]
        c.executemany('INSERT INTO incidents (timestamp, incident_type, severity, reason, action, status) VALUES (?,?,?,?,?,?)', mock_data)
        conn.commit()
    conn.close()

def log_incident(report):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Extract details safely
    incident_type = report.get('incident_type', 'UNKNOWN')
    
    # Handle structure diffs between app.py and agent.py
    if 'decision' in report:
        severity = report['decision'].get('severity', 'UNKNOWN')
        action = report['decision'].get('action', 'UNKNOWN')
        reason = report['decision'].get('reason', 'UNKNOWN')
    else:
        severity = "UNKNOWN"
        action = "UNKNOWN"
        reason = "UNKNOWN"
        
    status = "ACTIVE" if severity == "CRITICAL" else "RESOLVED"
    
    c.execute('''
        INSERT INTO incidents (timestamp, incident_type, severity, reason, action, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), incident_type, severity, reason, action, status))
    
    conn.commit()
    conn.close()

def fetch_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM incidents ORDER BY id DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Initialize on module load
init_db()
