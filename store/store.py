from PyQt6.QtCore import QObject, pyqtSignal
import json

class Store(QObject):
    """Global application state store"""
    
    state_changed = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.state = {
            'user': {
                'authenticated': False,
                'username': None,
                'role': None,
                'permissions': []
            },
            'personnel': {
                'active_count': 0,
                'on_shift': [],
                'alerts': []
            },
            'equipment': {
                'operational': 0,
                'maintenance': 0,
                'critical': 0,
                'offline': 0,
                'locations': {}
            },
            'safety': {
                'active_alerts': [],
                'incident_count': 0,
                'emergency_status': 'normal'
            },
            'environment': {
                'temperature': 22.0,
                'air_quality': 'good',
                'gas_levels': {}
            },
            'system': {
                'connected': True,
                'last_update': None,
                'services_status': {}
            }
        }
        
    def get_state(self, key=None):
        """Get application state"""
        if key is None:
            return self.state
        return self.state.get(key, {})
        
    def update_state(self, key, data):
        """Update application state"""
        if key in self.state:
            if isinstance(self.state[key], dict) and isinstance(data, dict):
                self.state[key].update(data)
            else:
                self.state[key] = data
            self.state_changed.emit(key, self.state[key])
            
    def reset_state(self):
        """Reset application state"""
        self.__init__()