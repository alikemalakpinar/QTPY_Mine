import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from screens.home.dashboard import DashboardScreen
from screens.safety.alerts import AlertsScreen
from screens.people.people_list import PeopleListScreen
from screens.equipment.equipment_map import EquipmentMapScreen
from app.navigation import NavigationBar
from services.mqtt_client import MQTTClient
from services.ws_client import WebSocketClient
from theme.theme import MineGuardTheme

class MineGuardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = MineGuardTheme()
        self.init_ui()
        self.init_services()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("MineGuard Safety Management System")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(self.theme.get_main_style())
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create navigation bar
        self.nav_bar = NavigationBar()
        self.nav_bar.page_changed.connect(self.change_page)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Initialize screens
        self.init_screens()
        
        # Add to layout
        main_layout.addWidget(self.nav_bar)
        main_layout.addWidget(self.stacked_widget, 1)
        
    def init_screens(self):
        """Initialize all application screens"""
        self.dashboard = DashboardScreen()
        self.alerts = AlertsScreen()
        self.people = PeopleListScreen()
        self.equipment = EquipmentMapScreen()
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.alerts)
        self.stacked_widget.addWidget(self.people)
        self.stacked_widget.addWidget(self.equipment)
        
    def init_services(self):
        """Initialize background services"""
        self.mqtt_client = MQTTClient()
        self.ws_client = WebSocketClient()
        
        # Connect to services
        self.mqtt_client.connect_to_broker()
        self.ws_client.connect_to_server()
        
    def change_page(self, page_index):
        """Change the current page"""
        self.stacked_widget.setCurrentIndex(page_index)
