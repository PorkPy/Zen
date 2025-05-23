import sqlite3
import json
import hashlib
from datetime import datetime
import os

class ReportDatabase:
    def __init__(self, db_path="reports.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                report_type TEXT NOT NULL,
                child_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT NOT NULL,
                current_section INTEGER DEFAULT 0,
                is_completed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_report_id(self, child_name, report_type):
        """Generate a unique report ID"""
        timestamp = str(datetime.now().timestamp())
        unique_string = f"{child_name}_{report_type}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    def save_report(self, report_id, report_type, child_name, data, current_section, is_completed=False):
        """Save or update a report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert data dict to JSON string
        data_json = json.dumps(data)
        
        # Check if report exists
        cursor.execute('SELECT id FROM reports WHERE id = ?', (report_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update existing report
            cursor.execute('''
                UPDATE reports 
                SET data = ?, current_section = ?, updated_at = CURRENT_TIMESTAMP, is_completed = ?
                WHERE id = ?
            ''', (data_json, current_section, is_completed, report_id))
        else:
            # Create new report
            cursor.execute('''
                INSERT INTO reports (id, report_type, child_name, data, current_section, is_completed)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (report_id, report_type, child_name, data_json, current_section, is_completed))
        
        conn.commit()
        conn.close()
        return report_id
    
    def load_report(self, report_id):
        """Load a report by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT report_type, child_name, data, current_section, is_completed, updated_at
            FROM reports WHERE id = ?
        ''', (report_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            report_type, child_name, data_json, current_section, is_completed, updated_at = result
            data = json.loads(data_json)
            return {
                "report_type": report_type,
                "child_name": child_name,
                "data": data,
                "current_section": current_section,
                "is_completed": is_completed,
                "updated_at": updated_at
            }
        return None
    
    def list_reports(self, limit=10):
        """List recent reports"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, report_type, child_name, updated_at, is_completed
            FROM reports 
            ORDER BY updated_at DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "report_type": row[1], 
                "child_name": row[2],
                "updated_at": row[3],
                "is_completed": row[4]
            }
            for row in results
        ]
    
    def delete_report(self, report_id):
        """Delete a report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted