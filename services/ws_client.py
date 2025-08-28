from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWebSockets import QWebSocket
from PyQt6.QtCore import QUrl
import json

class WebSocketClient(QObject):
    """WebSocket client for real-time communication with mine server"""
    
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    message_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.websocket = QWebSocket()
        self.websocket.connected.connect(self.on_connected)
        self.websocket.disconnected.connect(self.on_disconnected)
        self.websocket.textMessageReceived.connect(self.on_message_received)
        
        # Heartbeat timer
        self.heartbeat_timer = QTimer()
        self.heartbeat_timer.timeout.connect(self.send_heartbeat)
        
    def connect_to_server(self):
        """Connect to WebSocket server"""
        # In production, connect to actual WebSocket server
        # self.websocket.open(QUrl("wss://api.mineguard.com/ws"))
        
        # For demo, simulate connection
        self.on_connected()
        
    def on_connected(self):
        """Handle WebSocket connection"""
        self.connected.emit()
        self.heartbeat_timer.start(30000)  # Send heartbeat every 30 seconds
        
    def on_disconnected(self):
        """Handle WebSocket disconnection"""
        self.disconnected.emit()
        self.heartbeat_timer.stop()
        
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
        self.send_message(heartbeat)
        
    def send_message(self, data):
        """Send message through WebSocket"""
        if self.websocket.state() == QWebSocket.State.ConnectedState:
            message = json.dumps(data)
            self.websocket.sendTextMessage(message)
