"""SQLite Database Service - Enterprise Data Management"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class DatabaseService:
    """Professional database service with SQLite"""
    
    def __init__(self, db_path='/app/data/minetracker.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Ensure data directory exists
        Path('/app/data').mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self.connect()
        self.init_tables()
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return dict-like rows
            print(f"✅ Database connected: {self.db_path}")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
    
    def init_tables(self):
        """Initialize all database tables"""
        cursor = self.conn.cursor()
        
        # Personnel table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personnel (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                position TEXT,
                phone TEXT,
                email TEXT,
                emergency_contact TEXT,
                shift TEXT,
                entry_time TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Personnel location history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS location_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id TEXT NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                z REAL NOT NULL,
                zone_id TEXT,
                zone_name TEXT,
                heart_rate INTEGER,
                battery INTEGER,
                signal INTEGER,
                status TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES personnel(id)
            )
        """)
        
        # Anchors (Gateway devices)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anchors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                zone TEXT NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                z REAL DEFAULT 0,
                status TEXT DEFAULT 'online',
                battery INTEGER DEFAULT 100,
                signal_strength INTEGER DEFAULT 100,
                last_maintenance DATE,
                firmware_version TEXT,
                color TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tags (Personnel tracking devices)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                person_id TEXT,
                battery INTEGER DEFAULT 100,
                signal_strength INTEGER DEFAULT 100,
                firmware_version TEXT,
                status TEXT DEFAULT 'active',
                last_seen TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES personnel(id)
            )
        """)
        
        # Emergency events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emergency_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                entity_name TEXT,
                event_type TEXT NOT NULL,
                severity TEXT,
                x REAL,
                y REAL,
                z REAL,
                zone_name TEXT,
                description TEXT,
                status TEXT DEFAULT 'active',
                response_time INTEGER,
                resolved_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Alerts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                entity_name TEXT,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                acknowledged BOOLEAN DEFAULT 0,
                acknowledged_by TEXT,
                acknowledged_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # System logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_level TEXT NOT NULL,
                component TEXT,
                message TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Shifts/Vardiya
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shift_name TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                personnel_count INTEGER DEFAULT 0,
                supervisor TEXT,
                notes TEXT,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                generated_by TEXT,
                date_range_start DATE,
                date_range_end DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        print("✅ Database tables initialized")
    
    # Personnel operations
    def add_personnel(self, person_data):
        """Add new personnel"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO personnel 
            (id, first_name, last_name, position, phone, email, emergency_contact, shift, entry_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            person_data['id'],
            person_data['first_name'],
            person_data['last_name'],
            person_data.get('position', ''),
            person_data.get('phone', ''),
            person_data.get('email', ''),
            person_data.get('emergency_contact', ''),
            person_data.get('shift', ''),
            person_data.get('entry_time', '')
        ))
        self.conn.commit()
    
    def get_all_personnel(self):
        """Get all personnel"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM personnel")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_personnel_by_id(self, person_id):
        """Get personnel by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM personnel WHERE id = ?", (person_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Location history
    def add_location_record(self, location_data):
        """Add location history record"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO location_history 
            (person_id, x, y, z, zone_id, zone_name, heart_rate, battery, signal, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            location_data['person_id'],
            location_data['x'],
            location_data['y'],
            location_data['z'],
            location_data.get('zone_id', ''),
            location_data.get('zone_name', ''),
            location_data.get('heart_rate', 0),
            location_data.get('battery', 0),
            location_data.get('signal', 0),
            location_data.get('status', 'active')
        ))
        self.conn.commit()
    
    def get_location_history(self, person_id, limit=100):
        """Get location history for a person"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM location_history 
            WHERE person_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (person_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    # Anchor operations
    def add_anchor(self, anchor_data):
        """Add or update anchor"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO anchors 
            (id, name, zone, x, y, z, status, battery, signal_strength, firmware_version, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            anchor_data['id'],
            anchor_data['name'],
            anchor_data['zone'],
            anchor_data['x'],
            anchor_data['y'],
            anchor_data.get('z', 0),
            anchor_data.get('status', 'online'),
            anchor_data.get('battery', 100),
            anchor_data.get('signal_strength', 100),
            anchor_data.get('firmware_version', '1.0.0'),
            anchor_data.get('color', '#00D4FF')
        ))
        self.conn.commit()
    
    def get_all_anchors(self):
        """Get all anchors"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM anchors")
        return [dict(row) for row in cursor.fetchall()]
    
    def update_anchor_status(self, anchor_id, status, battery=None):
        """Update anchor status"""
        cursor = self.conn.cursor()
        if battery is not None:
            cursor.execute("""
                UPDATE anchors SET status = ?, battery = ? WHERE id = ?
            """, (status, battery, anchor_id))
        else:
            cursor.execute("""
                UPDATE anchors SET status = ? WHERE id = ?
            """, (status, anchor_id))
        self.conn.commit()
    
    # Tag operations
    def add_tag(self, tag_data):
        """Add or update tag"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO tags 
            (id, person_id, battery, signal_strength, firmware_version, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tag_data['id'],
            tag_data.get('person_id'),
            tag_data.get('battery', 100),
            tag_data.get('signal_strength', 100),
            tag_data.get('firmware_version', '1.0.0'),
            tag_data.get('status', 'active')
        ))
        self.conn.commit()
    
    def get_all_tags(self):
        """Get all tags"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tags")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_tag_by_person(self, person_id):
        """Get tag for a person"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tags WHERE person_id = ?", (person_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Emergency operations
    def add_emergency_event(self, event_data):
        """Add emergency event"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO emergency_events 
            (entity_type, entity_id, entity_name, event_type, severity, x, y, z, zone_name, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_data['entity_type'],
            event_data['entity_id'],
            event_data.get('entity_name', ''),
            event_data['event_type'],
            event_data.get('severity', 'high'),
            event_data.get('x'),
            event_data.get('y'),
            event_data.get('z'),
            event_data.get('zone_name', ''),
            event_data.get('description', '')
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_active_emergencies(self):
        """Get all active emergencies"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM emergency_events 
            WHERE status = 'active' 
            ORDER BY created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def resolve_emergency(self, event_id, response_time=None):
        """Resolve emergency event"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE emergency_events 
            SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP, response_time = ?
            WHERE id = ?
        """, (response_time, event_id))
        self.conn.commit()
    
    # Alert operations
    def add_alert(self, alert_data):
        """Add new alert"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO alerts 
            (alert_type, entity_type, entity_id, entity_name, severity, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            alert_data['alert_type'],
            alert_data.get('entity_type'),
            alert_data.get('entity_id'),
            alert_data.get('entity_name'),
            alert_data['severity'],
            alert_data['message']
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_alerts(self, limit=50):
        """Get recent alerts"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM alerts 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_unacknowledged_alerts(self):
        """Get unacknowledged alerts"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM alerts 
            WHERE acknowledged = 0 
            ORDER BY created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def acknowledge_alert(self, alert_id, acknowledged_by):
        """Acknowledge alert"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE alerts 
            SET acknowledged = 1, acknowledged_by = ?, acknowledged_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (acknowledged_by, alert_id))
        self.conn.commit()
    
    # System logs
    def add_log(self, level, component, message, details=None):
        """Add system log"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO system_logs (log_level, component, message, details)
            VALUES (?, ?, ?, ?)
        """, (level, component, message, details))
        self.conn.commit()
    
    def get_recent_logs(self, limit=100):
        """Get recent logs"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM system_logs 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    # Analytics
    def get_statistics(self, start_date=None, end_date=None):
        """Get system statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Personnel stats
        cursor.execute("SELECT COUNT(*) as total FROM personnel")
        stats['personnel_total'] = cursor.fetchone()['total']
        
        # Anchor stats
        cursor.execute("SELECT COUNT(*) as total FROM anchors WHERE status = 'online'")
        stats['anchors_online'] = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM anchors")
        stats['anchors_total'] = cursor.fetchone()['total']
        
        # Tag stats
        cursor.execute("SELECT COUNT(*) as total FROM tags WHERE status = 'active'")
        stats['tags_active'] = cursor.fetchone()['total']
        
        # Emergency stats
        cursor.execute("SELECT COUNT(*) as total FROM emergency_events WHERE status = 'active'")
        stats['emergencies_active'] = cursor.fetchone()['total']
        
        # Alert stats
        cursor.execute("SELECT COUNT(*) as total FROM alerts WHERE acknowledged = 0")
        stats['alerts_unacknowledged'] = cursor.fetchone()['total']
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")
