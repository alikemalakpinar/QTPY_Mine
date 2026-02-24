"""MineTracker Ultra - Tesla-Grade Main Application with Animated Transitions"""
import sys

# CRITICAL: Import QtWebEngine components FIRST!
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    QWebEngineView = None

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from app.navigation import NavigationBar
from theme.theme import MineTrackerTheme
from services.i18n import I18nService
from services.advanced_tracking_service import AdvancedTrackingService
from services.tcp_server_service import TCPServerService
from store.store import Store
from components.animations import AnimatedStackedWidget
from components.notification_island import DynamicIsland

# Screens
from screens.home.dashboard import DashboardScreen
from screens.home.live_map import LiveMapScreen
from screens.people.people_list import PeopleListScreen
from screens.equipment.equipment_management import EquipmentScreen
from screens.safety.sos import EmergencyScreen
from screens.reports.reports_home import ReportsScreen
from screens.zones.zones_overview import ZonesScreen
from screens.settings.settings import SettingsScreen
from screens.analytics.analytics_screen import AnalyticsScreen


class MineTrackerApp(QMainWindow):
    """Tesla-Grade MineTracker with animated transitions and Dynamic Island alerts"""

    def __init__(self):
        super().__init__()

        # Services
        self.i18n = I18nService()
        self.tracking = AdvancedTrackingService(mode='hybrid')
        self.store = Store()

        # TCP Server
        self.tcp_server = TCPServerService(host='0.0.0.0', port=8888)
        self.tcp_server.data_received.connect(self.on_tcp_data_received)
        self.tcp_server.connection_status.connect(self.on_tcp_connection_status)
        self.tcp_server.error_occurred.connect(self.on_tcp_error)
        self.tcp_server.start()

        # Init UI
        self.init_ui()
        self.init_connections()

        print("MineTracker Ultra started!")
        print(f"TCP Server: 0.0.0.0:8888")
        print(f"Tracking Mode: {self.tracking.mode}")
        print(f"3D Map: {'Active' if WEBENGINE_AVAILABLE else 'Disabled'}")

    def init_ui(self):
        """Initialize Tesla-grade UI"""
        self.setWindowTitle("MineTracker Ultra - Underground Safety System")
        self.setGeometry(100, 100, 1700, 950)

        # Apply theme
        self.setStyleSheet(MineTrackerTheme.get_app_style())

        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background: {MineTrackerTheme.BACKGROUND};")
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Navigation sidebar
        self.nav_bar = NavigationBar(self.i18n)
        self.nav_bar.page_changed.connect(self.change_page)
        self.nav_bar.emergency_triggered.connect(self.handle_emergency_button)
        main_layout.addWidget(self.nav_bar)

        # Content area with Dynamic Island overlay
        content_container = QWidget()
        content_container.setStyleSheet(f"background: {MineTrackerTheme.BACKGROUND};")
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Dynamic Island notification
        self.dynamic_island = DynamicIsland(content_container)
        self.dynamic_island.set_status("System Online", MineTrackerTheme.SUCCESS)
        self.dynamic_island.raise_()

        # Animated stacked widget for smooth page transitions
        self.stacked_widget = AnimatedStackedWidget()
        self.stacked_widget.set_transition_duration(300)
        self.stacked_widget.setStyleSheet(f"""
            AnimatedStackedWidget {{
                background: {MineTrackerTheme.BACKGROUND};
            }}
        """)

        # Create screens
        self.init_screens()

        content_layout.addWidget(self.stacked_widget, 1)

        main_layout.addWidget(content_container, 1)

        # Status bar
        self.create_status_bar()

        # Show first page
        self.stacked_widget.setCurrentIndex(0)

    def init_screens(self):
        """Create all screens"""
        self.dashboard = DashboardScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.dashboard)

        self.live_map = LiveMapScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.live_map)

        self.personnel = PeopleListScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.personnel)

        self.equipment = EquipmentScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.equipment)

        self.emergency = EmergencyScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.emergency)

        self.reports = ReportsScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.reports)

        self.zones = ZonesScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.zones)

        self.settings = SettingsScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.settings)

    def init_connections(self):
        """Setup signal connections"""
        self.tracking.emergency_signal.connect(self.handle_emergency)
        self.tracking.battery_alert.connect(self.handle_battery_alert)
        self.i18n.language_changed.connect(self.update_window_title)
        self.tracking.position_calculated.connect(self.on_position_calculated)

    def on_tcp_data_received(self, data):
        self.tracking.process_tcp_data(data)
        stats = self.tcp_server.get_statistics()
        self.tcp_status_label.setText(
            f"TCP: {stats['connected_clients']} clients  |  {stats['total_messages']} msgs  |  {stats['messages_per_second']:.1f} msg/s"
        )

    def on_tcp_connection_status(self, client_address, connected):
        if connected:
            print(f"TCP Client connected: {client_address}")
        else:
            print(f"TCP Client disconnected: {client_address}")

    def on_tcp_error(self, error_message):
        print(f"TCP Error: {error_message}")

    def on_position_calculated(self, data):
        tag_id = data.get('tag_id')
        accuracy = data.get('accuracy', 0)
        anchors_used = data.get('anchors_used', [])
        print(f"Position calculated: {tag_id} Accuracy: {accuracy:.3f}m [Anchors: {', '.join(anchors_used)}]")

    def create_status_bar(self):
        """Premium minimal status bar"""
        status = self.statusBar()
        status.setStyleSheet(f"""
            QStatusBar {{
                background: {MineTrackerTheme.BACKGROUND};
                color: {MineTrackerTheme.TEXT_MUTED};
                border-top: 1px solid {MineTrackerTheme.BORDER};
                font-size: 11px;
                padding: 4px 12px;
            }}
        """)

        self.status_label = QLabel("System Online")
        self.status_label.setStyleSheet(f"color: {MineTrackerTheme.SUCCESS}; font-weight: 600; font-size: 11px;")
        status.addWidget(self.status_label)

        self.tcp_status_label = QLabel("TCP: Waiting for connections...")
        self.tcp_status_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_MUTED}; font-size: 11px;")
        status.addWidget(self.tcp_status_label)

        separator = QLabel("  |  ")
        separator.setStyleSheet(f"color: {MineTrackerTheme.BORDER}; font-size: 11px;")
        status.addWidget(separator)

        self.mode_label = QLabel(f"Mode: {self.tracking.mode.upper()}")
        self.mode_label.setStyleSheet(f"color: {MineTrackerTheme.PRIMARY}; font-weight: 600; font-size: 11px;")
        status.addWidget(self.mode_label)

        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_MUTED}; font-size: 11px;")
        status.addPermanentWidget(self.time_label)

        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()

    def update_time(self):
        from datetime import datetime
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.time_label.setText(current_time)

    def change_page(self, index):
        """Smooth page transition"""
        self.stacked_widget.slide_to(index)

    def handle_emergency(self, data):
        """Handle emergency with Dynamic Island alert and dialog"""
        self.dynamic_island.show_alert(
            'danger',
            'EMERGENCY ALERT',
            f"{data['name']} - {data['zone']}",
            f"Coordinates: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}",
            auto_dismiss_ms=15000
        )

        msg = QMessageBox(self)
        msg.setWindowTitle("EMERGENCY ALERT")

        if data['type'] == 'personnel':
            text = f"""EMERGENCY SIGNAL!

Personnel: {data['name']}
Position: {data.get('position', 'Unknown')}
Zone: {data['zone']}
Coordinates: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}
Time: {data['timestamp']}"""
        else:
            text = f"""EQUIPMENT EMERGENCY!

Equipment: {data['name']}
Zone: {data['zone']}
Coordinates: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}
Time: {data['timestamp']}"""

        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStyleSheet(MineTrackerTheme.get_app_style())
        msg.exec()

    def handle_battery_alert(self, data):
        self.dynamic_island.show_alert(
            'warning',
            'Low Battery Alert',
            f"{data['name']} - Battery: {data['battery']}%",
            f"Tag ID: {data['id']}",
            auto_dismiss_ms=6000
        )
        print(f"Low Battery: {data['id']} - {data['name']} - {data['battery']}%")

    def handle_emergency_button(self):
        reply = QMessageBox.critical(
            self,
            "Emergency Protocol",
            """Activate emergency protocol?

This will:
- Alert all personnel
- Notify emergency services
- Activate evacuation procedures""",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.nav_bar.select_page(4)
            self.dynamic_island.show_alert(
                'danger',
                'EMERGENCY PROTOCOL ACTIVE',
                'All personnel have been notified',
                'Evacuation routes are now displayed',
                auto_dismiss_ms=20000
            )

    def update_window_title(self):
        if self.i18n.current_language == 'tr':
            self.setWindowTitle("AICO Maden Takip Sistemi Ultra")
        else:
            self.setWindowTitle("AICO MineTracker Ultra - Underground Safety System")

    def closeEvent(self, event):
        print("MineTracker shutting down...")
        if hasattr(self, 'tcp_server') and self.tcp_server.running:
            self.tcp_server.stop()
            self.tcp_server.wait(2000)
        print("Clean shutdown complete!")
        event.accept()
