from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime, timedelta
import random

class AlertsScreen(QWidget):
    """Safety alerts and emergency management screen"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_alerts()
        
    def init_ui(self):
        """Initialize alerts screen UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header = self.create_header()
        layout.addWidget(header)
        
        # Quick actions row
        actions_row = self.create_quick_actions()
        layout.addWidget(actions_row)
        
        # Main content
        content = self.create_main_content()
        layout.addWidget(content, 1)
        
    def create_header(self):
        """Create alerts screen header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 20)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("🚨 Safety Alert Center")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel("Monitor and manage all safety alerts and emergency responses")
        subtitle.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Alert summary
        summary = self.create_alert_summary()
        
        layout.addWidget(title_widget)
        layout.addStretch()
        layout.addWidget(summary)
        
        return header
        
    def create_alert_summary(self):
        """Create alert summary widget"""
        summary = QWidget()
        summary.setFixedSize(200, 80)
        summary.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QGridLayout(summary)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)
        
        # Critical alerts
        critical_label = QLabel("Critical")
        critical_label.setStyleSheet("QLabel { color: #6c757d; font-size: 11px; }")
        critical_count = QLabel("2")
        critical_count.setStyleSheet("QLabel { color: #dc3545; font-size: 18px; font-weight: bold; }")
        
        # Active alerts
        active_label = QLabel("Active")
        active_label.setStyleSheet("QLabel { color: #6c757d; font-size: 11px; }")
        active_count = QLabel("7")
        active_count.setStyleSheet("QLabel { color: #ffc107; font-size: 18px; font-weight: bold; }")
        
        layout.addWidget(critical_label, 0, 0)
        layout.addWidget(critical_count, 1, 0)
        layout.addWidget(active_label, 0, 1)
        layout.addWidget(active_count, 1, 1)
        
        return summary
        
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_widget = QWidget()
        layout = QHBoxLayout(actions_widget)
        layout.setSpacing(15)
        
        # Emergency protocols button
        emergency_btn = self.create_action_button(
            "🚨 EMERGENCY PROTOCOLS", 
            "#dc3545", 
            "Activate emergency response procedures"
        )
        
        # Evacuation drill button
        drill_btn = self.create_action_button(
            "📢 EVACUATION DRILL", 
            "#fd7e14", 
            "Start evacuation drill simulation"
        )
        
        # Zone lockdown button
        lockdown_btn = self.create_action_button(
            "🔒 ZONE LOCKDOWN", 
            "#6f42c1", 
            "Lock down specific mine sectors"
        )
        
        # Communication test button
        comms_btn = self.create_action_button(
            "📡 COMMS TEST", 
            "#20c997", 
            "Test all communication systems"
        )
        
        layout.addWidget(emergency_btn)
        layout.addWidget(drill_btn)
        layout.addWidget(lockdown_btn)
        layout.addWidget(comms_btn)
        layout.addStretch()
        
        return actions_widget
        
    def create_action_button(self, text, color, tooltip):
        """Create quick action button"""
        btn = QPushButton(text)
        btn.setFixedHeight(50)
        btn.setToolTip(tooltip)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.2)};
            }}
        """)
        
        return btn
        
    def darken_color(self, hex_color, factor=0.1):
        """Darken a hex color by a factor"""
        # Simple color darkening - in production use proper color manipulation
        return hex_color.replace('#', '#').lower()
        
    def create_main_content(self):
        """Create main content area"""
        content = QWidget()
        layout = QHBoxLayout(content)
        layout.setSpacing(20)
        
        # Left panel - Active alerts
        left_panel = self.create_alerts_panel()
        
        # Right panel - Alert details and map
        right_panel = self.create_details_panel()
        
        layout.addWidget(left_panel, 2)
        layout.addWidget(right_panel, 3)
        
        return content
        
    def create_alerts_panel(self):
        """Create active alerts panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Active Alerts")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        filter_combo = QComboBox()
        filter_combo.addItems(["All Alerts", "Critical Only", "Equipment", "Personnel", "Environmental"])
        filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Filter:"))
        header_layout.addWidget(filter_combo)
        
        layout.addLayout(header_layout)
        
        # Alerts list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        alerts_widget = QWidget()
        self.alerts_layout = QVBoxLayout(alerts_widget)
        self.alerts_layout.setSpacing(10)
        self.alerts_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(alerts_widget)
        layout.addWidget(scroll_area, 1)
        
        return panel
        
    def create_details_panel(self):
        """Create alert details and response panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Alert location map
        map_section = self.create_alert_map()
        layout.addWidget(map_section, 2)
        
        # Response actions
        response_section = self.create_response_actions()
        layout.addWidget(response_section, 1)
        
        return panel
        
    def create_alert_map(self):
        """Create alert location map"""
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
        title = QLabel("🗺️ Alert Locations")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        view_3d_btn = QPushButton("View in 3D")
        view_3d_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(view_3d_btn)
        
        layout.addLayout(header_layout)
        
        # Map visualization
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
        
        map_content = QLabel("""
🗺️ Mine Safety Map

🚨 Critical Alert - Sector B
⚠️  Equipment Alert - Sector A  
⚠️  Environmental - Sector C
⚠️  Personnel - Sector D

📍 Live tracking of all alerts
🚛 Equipment positions shown
👥 Personnel locations updated
        """)
        map_content.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        map_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        map_layout.addWidget(map_content)
        layout.addWidget(map_widget, 1)
        
        return section
        
    def create_response_actions(self):
        """Create emergency response actions panel"""
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
        
        title = QLabel("⚡ Emergency Response")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Response actions grid
        actions_grid = QGridLayout()
        actions_grid.setSpacing(10)
        
        response_actions = [
            ("🚑 Medical Team", "Dispatch emergency medical", "#dc3545"),
            ("🚒 Fire Rescue", "Alert fire department", "#fd7e14"),
            ("👮 Security", "Contact mine security", "#6f42c1"),
            ("📞 Emergency", "Call emergency services", "#e83e8c"),
            ("📢 Announce", "Site-wide announcement", "#20c997"),
            ("🔒 Lockdown", "Sector isolation", "#6c757d"),
        ]
        
        for i, (name, desc, color) in enumerate(response_actions):
            action_btn = self.create_response_button(name, desc, color)
            row = i // 2
            col = i % 2
            actions_grid.addWidget(action_btn, row, col)
            
        layout.addLayout(actions_grid)
        
        return section
        
    def create_response_button(self, name, description, color):
        """Create emergency response button"""
        btn = QPushButton()
        btn.setFixedHeight(60)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 10px 15px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """)
        
        btn_layout = QVBoxLayout(btn)
        btn_layout.setSpacing(2)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 10px;
            }
        """)
        
        btn_layout.addWidget(name_label)
        btn_layout.addWidget(desc_label)
        
        return btn
        
    def load_alerts(self):
        """Load and display alerts"""
        # Sample alert data
        alerts_data = [
            {
                'id': 'ALERT_001',
                'type': 'critical',
                'category': 'Equipment',
                'title': 'Equipment Malfunction - Excavator #7',
                'description': 'Hydraulic system failure detected. Immediate maintenance required.',
                'location': 'Sector B - Level 2',
                'timestamp': datetime.now() - timedelta(minutes=5),
                'status': 'active',
                'assigned_to': 'Maintenance Team Alpha'
            },
            {
                'id': 'ALERT_002',
                'type': 'high',
                'category': 'Environmental',
                'title': 'Gas Level Warning',
                'description': 'Methane concentration above normal threshold in ventilation shaft.',
                'location': 'Sector C - Ventilation Shaft 3',
                'timestamp': datetime.now() - timedelta(minutes=12),
                'status': 'investigating',
                'assigned_to': 'Safety Inspector'
            },
            {
                'id': 'ALERT_003',
                'type': 'medium',
                'category': 'Personnel',
                'title': 'Worker Check-in Overdue',
                'description': 'Worker ID: W-1247 has not checked in at scheduled checkpoint.',
                'location': 'Sector A - Tunnel 5',
                'timestamp': datetime.now() - timedelta(minutes=18),
                'status': 'active',
                'assigned_to': 'Shift Supervisor'
            },
            {
                'id': 'ALERT_004',
                'type': 'low',
                'category': 'Equipment',
                'title': 'Routine Maintenance Due',
                'description': 'Conveyor belt #12 scheduled for routine maintenance check.',
                'location': 'Processing Plant',
                'timestamp': datetime.now() - timedelta(hours=2),
                'status': 'scheduled',
                'assigned_to': 'Maintenance Team Beta'
            },
        ]
        
        for alert_data in alerts_data:
            alert_widget = self.create_alert_item(alert_data)
            self.alerts_layout.addWidget(alert_widget)
            
        # Add stretch to push alerts to top
        self.alerts_layout.addStretch()
        
    def create_alert_item(self, alert_data):
        """Create individual alert item widget"""
        item = QWidget()
        item.setFixedHeight(100)
        
        # Set background color based on alert type
        type_colors = {
            'critical': '#fff5f5',
            'high': '#fff8e1',
            'medium': '#f3e5f5',
            'low': '#e8f5e8'
        }
        
        border_colors = {
            'critical': '#f56565',
            'high': '#ed8936',
            'medium': '#9f7aea',
            'low': '#48bb78'
        }
        
        item.setStyleSheet(f"""
            QWidget {{
                background-color: {type_colors.get(alert_data['type'], '#f8f9fa')};
                border-left: 4px solid {border_colors.get(alert_data['type'], '#dee2e6')};
                border-radius: 8px;
                margin-bottom: 5px;
            }}
            QWidget:hover {{
                background-color: {self.lighten_color(type_colors.get(alert_data['type'], '#f8f9fa'))};
            }}
        """)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Alert icon and type
        icon_widget = QWidget()
        icon_widget.setFixedWidth(40)
        icon_layout = QVBoxLayout(icon_widget)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        type_icons = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '⚡',
            'low': 'ℹ️'
        }
        
        icon_label = QLabel(type_icons.get(alert_data['type'], '📋'))
        icon_label.setFont(QFont("Arial", 20))
        icon_layout.addWidget(icon_label)
        
        # Alert content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(4)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title and category
        title_layout = QHBoxLayout()
        
        title_label = QLabel(alert_data['title'])
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        
        category_label = QLabel(f"[{alert_data['category']}]")
        category_label.setStyleSheet(f"""
            QLabel {{
                color: {border_colors.get(alert_data['type'], '#6c757d')};
                font-size: 11px;
                font-weight: 500;
            }}
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(category_label)
        
        # Description
        desc_label = QLabel(alert_data['description'])
        desc_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
            }
        """)
        desc_label.setWordWrap(True)
        
        # Location and time
        info_layout = QHBoxLayout()
        
        location_label = QLabel(f"📍 {alert_data['location']}")
        location_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 11px;
            }
        """)
        
        time_label = QLabel(f"🕒 {self.format_time_ago(alert_data['timestamp'])}")
        time_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
            }
        """)
        
        info_layout.addWidget(location_label)
        info_layout.addStretch()
        info_layout.addWidget(time_label)
        
        content_layout.addLayout(title_layout)
        content_layout.addWidget(desc_label)
        content_layout.addLayout(info_layout)
        
        # Action buttons
        actions_widget = QWidget()
        actions_widget.setFixedWidth(120)
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setSpacing(5)
        
        acknowledge_btn = QPushButton("Acknowledge")
        acknowledge_btn.setFixedHeight(25)
        acknowledge_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        respond_btn = QPushButton("Respond")
        respond_btn.setFixedHeight(25)
        respond_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {border_colors.get(alert_data['type'], '#28a745')};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)
        
        actions_layout.addWidget(acknowledge_btn)
        actions_layout.addWidget(respond_btn)
        
        layout.addWidget(icon_widget)
        layout.addWidget(content_widget, 1)
        layout.addWidget(actions_widget)
        
        return item
        
    def format_time_ago(self, timestamp):
        """Format timestamp as time ago"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.seconds < 60:
            return f"{diff.seconds}s ago"
        elif diff.seconds < 3600:
            return f"{diff.seconds // 60}m ago"
        elif diff.days == 0:
            return f"{diff.seconds // 3600}h ago"
        else:
            return f"{diff.days}d ago"
            
    def lighten_color(self, hex_color):
        """Lighten a hex color"""
        # Simple color lightening - in production use proper color manipulation
        return hex_color
