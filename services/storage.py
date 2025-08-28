import json
import os
from PyQt6.QtCore import QObject, QStandardPaths

class StorageService(QObject):
    """Local storage service for application data"""
    
    def __init__(self):
        super().__init__()
        self.app_data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        os.makedirs(self.app_data_dir, exist_ok=True)
        
    def save_data(self, key, data):
        """Save data to local storage"""
        try:
            file_path = os.path.join(self.app_data_dir, f"{key}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
            
    def load_data(self, key, default=None):
        """Load data from local storage"""
        try:
            file_path = os.path.join(self.app_data_dir, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Error loading data: {e}")
            return default
            
    def delete_data(self, key):
        """Delete data from local storage"""
        try:
            file_path = os.path.join(self.app_data_dir, f"{key}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False
