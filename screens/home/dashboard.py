from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import random
from datetime import datetime, timedelta

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_timers()
        
    def init_ui(self):
        """Initialize dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Stats cards row
        stats_row = self.create_stats_row()
        layout.addWidget(stats_row)
        
        # Main content row
        content_row = self.create_content_row()
        layout.addWidget(content_row, 1)
        
    def create_header(self):
        """Create dashboard header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 20)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Safety Dashboard")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel(f"Real-time monitoring • {datetime.now().strftime('%B %d, %Y')}")
        subtitle.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Status indicator
        status_widget = self.create_status_indicator()
        
        layout.addWidget(title_widget)
        layout.addStretch()
        layout.addWidget(status_widget)
        
        return header
        
    def create_status_indicator(self):
        """Create system status indicator"""
        status_widget = QWidget()
        status_widget.setFixedSize(120, 60)
        status_widget.setStyleSheet("""
            QWidget {
                background-color: #d4edda;
                border-radius: 8px;
                border: 1px solid #c3e6cb;
            }
        """)
        
        layout = QVBoxLayout(status_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        status_label = QLabel("🟢 OPERATIONAL")
        status_label.setStyleSheet("""
            QLabel {
                color: #155724;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(status_label)
        
        return status_widget
        
    def create_stats_row(self):
        """Create statistics cards row"""
        stats_widget = QWidget()
        layout = QHBoxLayout(stats_widget)
        layout.setSpacing(20)
        
        # Statistics data
        stats = [
            ("Active Personnel", "147", "👥", "#3498db", "+5 from yesterday"),
            ("Equipment Online", "89%", "🚛", "#2ecc71", "All critical systems up"),
            ("Safety Incidents", "0", "🛡️", "#e74c3c", "24 hours incident-free"),
            ("Zone Temperature", "22°C", "🌡️", "#f39c12", "Within safe limits"),
        ]
        
        for title, value, icon, color, subtitle in stats:
            card = self.create_stat_card(title, value, icon, color, subtitle)
            layout.addWidget(card)
            
        return stats_widget
        
    def create_stat_card(self, title, value, icon, color, subtitle):
        """Create individual statistics card"""
        card = QWidget()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }}
            QWidget:hover {{
                border: 1px solid {color};
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 20))
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 13px;
                font-weight: 500;
            }
        """)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: bold;
            }}
        """)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
            }
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        
        return card
        
    def create_content_row(self):
        """Create main content row"""
        content_widget = QWidget()
        layout = QHBoxLayout(content_widget)
        layout.setSpacing(20)
        
        # Left column - Recent alerts and activity
        left_column = self.create_left_column()
        
        # Right column - Live map and equipment status
        right_column = self.create_right_column()
        
        layout.addWidget(left_column, 1)
        layout.addWidget(right_column, 2)
        
        return content_widget
        
    def create_left_column(self):
        """Create left column with alerts and activity"""
        column = QWidget()
        layout = QVBoxLayout(column)
        layout.setSpacing(15)
        
        # Recent alerts section
        alerts_section = self.create_alerts_section()
        layout.addWidget(alerts_section)
        
        # Recent activity section
        activity_section = self.create_activity_section()
        layout.addWidget(activity_section, 1)
        
        return column
        
    def create_alerts_section(self):
        """Create recent alerts section"""
        section = QWidget()
        section.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🚨 Recent Alerts")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        view_all_btn = QPushButton("View All")
        view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #007bff;
                border: none;
                font-size: 12px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #0056b3;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(view_all_btn)
        
        layout.addLayout(header_layout)
        
        # Alert items
        alerts = [
            ("Equipment Maintenance Due", "Loader #7 - Scheduled for tomorrow", "⚠️", "#f39c12"),
            ("Zone Temperature Alert", "Sector B - Slightly elevated", "🌡️", "#e74c3c"),
            ("Personnel Check-in", "All shift workers accounted for", "✅", "#2ecc71"),
        ]
        
        for alert_title, alert_desc, alert_icon, alert_color in alerts:
            alert_item = self.create_alert_item(alert_title, alert_desc, alert_icon, alert_color)
            layout.addWidget(alert_item)
            
        return section
        
    def create_alert_item(self, title, description, icon, color):
        """Create individual alert item"""
        item = QWidget()
        item.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 10px;
            }
            QWidget:hover {
                background-color: #e9ecef;
            }
        """)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 16))
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(2)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
            }
        """)
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        
        layout.addWidget(icon_label)
        layout.addWidget(content_widget)
        
        return item
        
    def create_activity_section(self):
        """Create recent activity section"""
        section = QWidget()
        section.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("📋 Recent Activity")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Activity timeline
        activities = [
            ("Shift Change Completed", "Day shift → Night shift", "2 min ago"),
            ("Equipment Inspection", "Excavator #3 passed safety check", "15 min ago"),
            ("Personnel Training", "Safety drill completed - Sector A", "1 hour ago"),
            ("System Update", "Location tracking calibrated", "2 hours ago"),
        ]
        
        for activity_title, activity_desc, activity_time in activities:
            activity_item = self.create_activity_item(activity_title, activity_desc, activity_time)
            layout.addWidget(activity_item)
            
        return section
        
    def create_activity_item(self, title, description, time):
        """Create individual activity item"""
        item = QWidget()
        layout = QHBoxLayout(item)
        layout.setContentsMargins(0, 5, 0, 5)
        
        # Timeline dot
        dot = QLabel("●")
        dot.setStyleSheet("QLabel { color: #007bff; font-size: 12px; }")
        dot.setFixedWidth(20)
        
        # Content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(2)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
            }
        """)
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        
        # Time
        time_label = QLabel(time)
        time_label.setStyleSheet("""
            QLabel {
                color: #adb5bd;
                font-size: 10px;
            }
        """)
        time_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(dot)
        layout.addWidget(content_widget, 1)
        layout.addWidget(time_label)
        
        return item
        
    def create_right_column(self):
        """Create right column with map and equipment"""
        column = QWidget()
        layout = QVBoxLayout(column)
        layout.setSpacing(15)
        
        # Live map section
        map_section = self.create_map_section()
        layout.addWidget(map_section, 2)
        
        # Equipment status section
        equipment_section = self.create_equipment_section()
        layout.addWidget(equipment_section, 1)
        
        return column
        
    def create_map_section(self):
        """Create live mine map section"""
        section = QWidget()
        section.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🗺️ Live Mine Map")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        fullscreen_btn = QPushButton("Fullscreen")
        fullscreen_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(fullscreen_btn)
        
        layout.addLayout(header_layout)
        
        # Map placeholder
        map_widget = QWidget()
        map_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 2px dashed #dee2e6;
            }
        """)
        
        map_layout = QVBoxLayout(map_widget)
        map_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        map_label = QLabel("🗺️ Interactive 3D Mine Map\n\n📍 147 Personnel Tracked\n🚛 89% Equipment Online\n⚠️ 3 Active Zones")
        map_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                text-align: center;
            }
        """)
        map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        map_layout.addWidget(map_label)
        
        layout.addWidget(map_widget, 1)
        
        return section
        
    def create_equipment_section(self):
        """Create equipment status section"""
        section = QWidget()
        section.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("🚛 Equipment Status")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Equipment grid
        equipment_grid = QGridLayout()
        equipment_grid.setSpacing(10)
        
        equipment_data = [
            ("Excavator #1", "Online", "#2ecc71"),
            ("Loader #7", "Maintenance", "#f39c12"),
            ("Truck #15", "Online", "#2ecc71"),
            ("Drill #3", "Offline", "#e74c3c"),
            ("Crusher #1", "Online", "#2ecc71"),
            ("Conveyor #2", "Online", "#2ecc71"),
        ]
        
        for i, (name, status, color) in enumerate(equipment_data):
            equipment_item = self.create_equipment_item(name, status, color)
            row = i // 2
            col = i % 2
            equipment_grid.addWidget(equipment_item, row, col)
            
        layout.addLayout(equipment_grid)
        
        return section
        
    def create_equipment_item(self, name, status, color):
        """Create individual equipment status item"""
        item = QWidget()
        item.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(8, 8, 8, 8)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        
        status_label = QLabel(f"● {status}")
        status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 11px;
                font-weight: 600;
            }}
        """)
        
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(status_label)
        
        return item
        
    def init_timers(self):
        """Initialize update timers"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(30000)  # Update every 30 seconds
        
    def update_data(self):
        """Update dashboard data"""
        # In a real application, this would fetch fresh data from APIs
        pass
