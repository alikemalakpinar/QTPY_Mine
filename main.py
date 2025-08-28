import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from app.app import MineGuardApp
from services.storage import StorageService
from store.store import Store

def main():
    """Initialize and run the Mining Safety Management System"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MineGuard Safety System")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("MineGuard Solutions")
    
    # Initialize services
    storage = StorageService()
    store = Store()
    
    # Create and show main application
    main_app = MineGuardApp()
    main_app.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())