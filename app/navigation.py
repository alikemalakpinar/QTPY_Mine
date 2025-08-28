from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class NavigationBar(QWidget):
    page_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.init_ui()
        
    def init_ui(self):
        """Initialize navigation UI"""
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e2329;
                border-right: 1px solid #3d4047;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Navigation items
        self.nav_items = [
            ("Dashboard", "📊", 0),
            ("Safety Alerts", "🚨", 1),
            ("Personnel", "👥", 2),
            ("Equipment", "🚛", 3),
            ("Reports", "📋", 4),
            ("Settings", "⚙️", 5),
        ]
        
        self.buttons = []
        for name, icon, index in self.nav_items:
            btn = self.create_nav_button(name, icon, index)
            self.buttons.append(btn)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Emergency button
        emergency_btn = self.create_emergency_button()
        layout.addWidget(emergency_btn)
        
    def create_header(self):
        """Create navigation header"""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background-color: #0f1419;
                border-bottom: 1px solid #3d4047;
            }
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        icon_label = QLabel("⛏️")
        icon_label.setFont(QFont("Arial", 24))
        
        text_label = QLabel("MineGuard")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        
        return header
        
    def create_nav_button(self, name, icon, index):
        """Create a navigation button"""
        btn = QPushButton(f"{icon}  {name}")
        btn.setFixedHeight(50)
        btn.clicked.connect(lambda: self.select_page(index))
        
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #a0a6b8;
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2a2f36;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #3d4047;
            }
        """)
        
        return btn
        
    def create_emergency_button(self):
        """Create emergency SOS button"""
        btn = QPushButton("🚨 EMERGENCY SOS")
        btn.setFixedHeight(60)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
        return btn
        
    def select_page(self, index):
        """Select a navigation page"""
        # Update button styles
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 15px 20px;
                        text-align: left;
                        font-size: 14px;
                        font-weight: 500;
                        border-right: 3px solid #0056b3;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #a0a6b8;
                        border: none;
                        padding: 15px 20px;
                        text-align: left;
                        font-size: 14px;
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #2a2f36;
                        color: #ffffff;
                    }
                """)
        
        self.current_page = index
        self.page_changed.emit(index)