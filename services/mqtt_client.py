import json
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtNetwork import QTcpSocket

class MQTTClient(QObject):
    """MQTT client for real-time mine data communication"""
    
    message_received = pyqtSignal(str, dict)
    connection_changed = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.connected = False
        self.topics = [
            'mineguard/personnel/location',
            'mineguard/equipment/status',
            'mineguard/safety/alerts',
            'mineguard/environment/sensors'
        ]
        
        # Simulation timer for demo
        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self.simulate_data)
        
    def connect_to_broker(self):
        """Connect to MQTT broker"""
        # In production, this would connect to actual MQTT broker
        self.connected = True
        self.connection_changed.emit(True)
        
        # Start simulation for demo
        self.sim_timer.start(5000)  # Simulate data every 5 seconds
        
    def simulate_data(self):
        """Simulate incoming MQTT data for demo"""
        import random
        from datetime import datetime
        
        # Simulate personnel location updates
        personnel_data = {
            'person_id': f'WORKER_{random.randint(1, 150):03d}',
            'location': {
                'x': random.uniform(-500, 500),
                'y': random.uniform(-300, 300),
                'zone': f'SECTOR_{random.choice(["A", "B", "C", "D"])}'
            },
            'timestamp': datetime.now().isoformat(),
            'heart_rate': random.randint(60, 100),
            'temperature': round(random.uniform(36.0, 37.5), 1)
        }
        self.message_received.emit('personnel/location', personnel_data)
        
        # Simulate equipment status updates
        equipment_data = {
            'equipment_id': f'EQ_{random.randint(1, 50):03d}',
            'status': random.choice(['operational', 'maintenance', 'offline']),
            'location': {
                'x': random.uniform(-400, 400),
                'y': random.uniform(-200, 200)
            },
            'fuel_level': random.randint(10, 100),
            'operating_hours': random.randint(100, 5000),
            'last_maintenance': '2024-12-15T10:30:00Z'
        }
        self.message_received.emit('equipment/status', equipment_data)
        
        # Simulate environmental sensor data
        if random.random() < 0.3:  # 30% chance of alert
            alert_data = {
                'alert_type': random.choice(['temperature', 'gas_level', 'equipment_fault', 'personnel_emergency']),
                'severity': random.choice(['low', 'medium', 'high', 'critical']),
                'location': f'SECTOR_{random.choice(["A", "B", "C", "D"])}',
                'description': 'Automated safety alert triggered',
                'timestamp': datetime.now().isoformat()
            }
            self.message_received.emit('safety/alerts', alert_data)
