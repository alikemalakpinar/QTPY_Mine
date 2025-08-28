# services/ws_client.py - Fixed WebSocket client
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import json

class WebSocketClient(QObject):
    """WebSocket client for real-time communication with mine server"""
    
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    message_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.is_connected = False
        
        # Heartbeat timer
        self.heartbeat_timer = QTimer()
        self.heartbeat_timer.timeout.connect(self.send_heartbeat)
        
    def connect_to_server(self):
        """Connect to WebSocket server"""
        # In production, connect to actual WebSocket server
        # For demo, simulate connection
        self.on_connected()
        
    def on_connected(self):
        """Handle WebSocket connection"""
        self.is_connected = True
        self.connected.emit()
        self.heartbeat_timer.start(30000)  # Send heartbeat every 30 seconds
        print("✅ WebSocket Connected (Simulated)")
        
    def on_disconnected(self):
        """Handle WebSocket disconnection"""
        self.is_connected = False
        self.disconnected.emit()
        self.heartbeat_timer.stop()
        print("❌ WebSocket Disconnected")
        
    def on_message_received(self, message):
        """Handle received WebSocket message"""
        try:
            data = json.loads(message)
            self.message_received.emit(data)
        except json.JSONDecodeError:
            pass
            
    def send_heartbeat(self):
        """Send heartbeat to keep connection alive"""
        heartbeat = {
            'type': 'heartbeat',
            'timestamp': QTimer().remainingTime()
        }
        # For demo, just print heartbeat
        print("💓 Heartbeat sent")
        
    def send_message(self, data):
        """Send message through WebSocket"""
        if self.is_connected:
            message = json.dumps(data)
            print(f"📤 Sending: {message[:100]}...")
            # In production, would send actual WebSocket message
            return True
        return False