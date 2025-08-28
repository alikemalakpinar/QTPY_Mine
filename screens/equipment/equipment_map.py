from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime, timedelta

class EquipmentMapScreen(QWidget):
    """Equipment tracking and management screen with live map"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_equipment_data()
        
    def init_ui(self):
        """Initialize equipment screen UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Equipment status overview
        status_overview = self.create_status_overview()
        layout.addWidget(status_overview)
        
        # Main content
        content = self.create_main_content()
        layout.addWidget(content, 1)
        
    def create_header(self):
        """Create equipment screen header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 20)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("🚛 Equipment Management")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel("Real-time monitoring and maintenance tracking for all mining equipment")
        subtitle.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Quick actions
        actions = self.create_header_actions()
        
        layout.addWidget(title_widget)
        layout.addStretch()
        layout.addWidget(actions)
        
        return header
        
    def create_header_actions(self):
        """Create header action buttons"""
        actions = QWidget()
        layout = QHBoxLayout(actions)
        layout.setSpacing(10)
        
        # Equipment health report
        health_btn = QPushButton("📊 Health Report")
        health_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        # Schedule maintenance
        maintenance_btn = QPushButton("🔧 Schedule Maintenance")
        maintenance_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        
        # Add equipment
        add_btn = QPushButton("+ Add Equipment")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        layout.addWidget(health_btn)
        layout.addWidget(maintenance_btn)
        layout.addWidget(add_btn)
        
        return actions
        
    def create_status_overview(self):
        """Create equipment status overview cards"""
        overview = QWidget()
        layout = QHBoxLayout(overview)
        layout.setSpacing(20)
        
        # Status cards data
        status_data = [
            ("Operational", "42", "🟢", "#28a745", "Equipment running normally"),
            ("Maintenance", "8", "🟡", "#ffc107", "Scheduled/ongoing maintenance"),
            ("Critical Issues", "3", "🔴", "#dc3545", "Requires immediate attention"),
            ("Offline", "5", "⚫", "#6c757d", "Not currently in use"),
            ("Total Fleet", "58", "🚛", "#007bff", "All registered equipment"),
        ]
        
        for title, count, icon, color, description in status_data:
            card = self.create_status_card(title, count, icon, color, description)
            layout.addWidget(card)
            
        return overview
        
    def create_status_card(self, title, count, icon, color, description):
        """Create individual status card"""
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
        
        # Count
        count_label = QLabel(count)
        count_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: bold;
            }}
        """)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
            }
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(count_label)
        layout.addWidget(desc_label)
        
        return card
        
    def create_main_content(self):
        """Create main content area"""
        content = QWidget()
        layout = QHBoxLayout(content)
        layout.setSpacing(20)
        
        # Left panel - Equipment list and filters
        left_panel = self.create_left_panel()
        
        # Right panel - Equipment map and details
        right_panel = self.create_right_panel()
        
        layout.addWidget(left_panel, 2)
        layout.addWidget(right_panel, 3)
        
        return content
        
    def create_left_panel(self):
        """Create left panel with equipment list"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Equipment filters
        filters = self.create_equipment_filters()
        layout.addWidget(filters)
        
        # Equipment list
        equipment_list = self.create_equipment_list()
        layout.addWidget(equipment_list, 1)
        
        return panel
        
    def create_equipment_filters(self):
        """Create equipment filter controls"""
        filters = QWidget()
        filters.setFixedHeight(60)
        filters.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QHBoxLayout(filters)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Status filter
        status_label = QLabel("Status:")
        status_label.setStyleSheet("QLabel { color: #495057; font-weight: 500; }")
        
        status_combo = QComboBox()
        status_combo.addItems(["All Status", "Operational", "Maintenance", "Critical", "Offline"])
        status_combo.setStyleSheet("""
            QComboBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 100px;
            }
        """)
        
        # Type filter
        type_label = QLabel("Type:")
        type_label.setStyleSheet("QLabel { color: #495057; font-weight: 500; }")
        
        type_combo = QComboBox()
        type_combo.addItems(["All Types", "Excavators", "Loaders", "Trucks", "Drills", "Conveyors", "Crushers"])
        type_combo.setStyleSheet("""
            QComboBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 100px;
            }
        """)
        
        # Search
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search equipment...")
        search_box.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        
        layout.addWidget(status_label)
        layout.addWidget(status_combo)
        layout.addWidget(type_label)
        layout.addWidget(type_combo)
        layout.addWidget(search_box, 1)
        
        return filters
        
    def create_equipment_list(self):
        """Create equipment list panel"""
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
        title = QLabel("Equipment List")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Equipment items scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        equipment_widget = QWidget()
        self.equipment_layout = QVBoxLayout(equipment_widget)
        self.equipment_layout.setSpacing(10)
        self.equipment_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(equipment_widget)
        layout.addWidget(scroll_area, 1)
        
        return panel
        
    def create_right_panel(self):
        """Create right panel with map and details"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Equipment location map
        map_section = self.create_equipment_map()
        layout.addWidget(map_section, 2)
        
        # Selected equipment details
        details_section = self.create_equipment_details()
        layout.addWidget(details_section, 1)
        
        return panel
        
    def create_equipment_map(self):
        """Create equipment location map"""
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
        
        title = QLabel("🗺️ Equipment Location Map")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        # Map controls
        controls_layout = QHBoxLayout()
        
        view_3d_btn = QPushButton("3D View")
        view_3d_btn.setFixedHeight(30)
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
        
        fullscreen_btn = QPushButton("Fullscreen")
        fullscreen_btn.setFixedHeight(30)
        fullscreen_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        
        controls_layout.addWidget(view_3d_btn)
        controls_layout.addWidget(fullscreen_btn)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(controls_layout)
        
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
🗺️ Live Equipment Tracking

🚛 Excavator #7 - Sector B (Active)
🚛 Loader #12 - Processing Plant (Active)  
🚛 Truck #25 - Transport Route (Moving)
🚛 Drill #3 - Sector A (Maintenance)
🚛 Crusher #1 - Plant (Offline)

📍 Real-time GPS tracking
⚡ Equipment status monitoring
🔧 Maintenance alerts integrated
        """)
        map_content.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 13px;
                line-height: 1.8;
            }
        """)
        map_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        map_layout.addWidget(map_content)
        layout.addWidget(map_widget, 1)
        
        return section
        
    def create_equipment_details(self):
        """Create equipment details panel"""
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
        
        title = QLabel("🚛 Equipment Details")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        status_badge = QLabel("🟢 OPERATIONAL")
        status_badge.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(status_badge)
        
        layout.addLayout(header_layout)
        
        # Equipment information
        equipment_info = QLabel("""
<b>Excavator #7 - CAT 374F</b><br>
<b>Serial Number:</b> CAT374F-2024-007<br>
<b>Location:</b> Sector B - Level 2<br>
<b>Operator:</b> Mike Wilson (W-003)<br>
<b>Operating Hours:</b> 2,847 hours<br>
<b>Fuel Level:</b> 78% (245L remaining)<br>
<b>Engine Temp:</b> 87°C (Normal)<br>
<b>Hydraulic Pressure:</b> 340 bar (Normal)<br>
<b>Last Maintenance:</b> November 15, 2024<br>
<b>Next Service Due:</b> January 15, 2025
        """)
        equipment_info.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 12px;
                line-height: 1.6;
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        layout.addWidget(equipment_info)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        
        maintenance_btn = QPushButton("🔧 Schedule Maintenance")
        maintenance_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        
        contact_btn = QPushButton("📞 Contact Operator")
        contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        report_btn = QPushButton("📋 Generate Report")
        report_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        actions_layout.addWidget(maintenance_btn)
        actions_layout.addWidget(contact_btn)
        actions_layout.addWidget(report_btn)
        
        layout.addLayout(actions_layout)
        
        return section
        
    def load_equipment_data(self):
        """Load equipment data"""
        # Sample equipment data
        equipment_data = [
            {
                'id': 'EXC-007',
                'name': 'Excavator #7',
                'type': 'CAT 374F',
                'status': 'operational',
                'location': 'Sector B - Level 2',
                'operator': 'Mike Wilson',
                'fuel_level': 78,
                'operating_hours': 2847,
                'last_maintenance': '2024-11-15',
                'next_service': '2025-01-15'
            },
            {
                'id': 'LDR-012',
                'name': 'Loader #12',
                'type': 'CAT 980M',
                'status': 'operational',
                'location': 'Processing Plant',
                'operator': 'Sarah Chen',
                'fuel_level': 92,
                'operating_hours': 1856,
                'last_maintenance': '2024-12-01',
                'next_service': '2025-02-01'
            },
            {
                'id': 'TRK-025',
                'name': 'Truck #25',
                'type': 'CAT 777G',
                'status': 'operational',
                'location': 'Transport Route A',
                'operator': 'David Rodriguez',
                'fuel_level': 45,
                'operating_hours': 3421,
                'last_maintenance': '2024-10-20',
                'next_service': '2024-12-20'
            },
            {
                'id': 'DRL-003',
                'name': 'Drill #3',
                'type': 'Atlas Copco ROC D65',
                'status': 'maintenance',
                'location': 'Sector A - Workshop',
                'operator': 'Maintenance Team',
                'fuel_level': 0,
                'operating_hours': 4567,
                'last_maintenance': '2024-12-18',
                'next_service': '2024-12-22'
            },
            {
                'id': 'CSH-001',
                'name': 'Crusher #1',
                'type': 'Sandvik CJ815',
                'status': 'offline',
                'location': 'Processing Plant',
                'operator': 'Unassigned',
                'fuel_level': 0,
                'operating_hours': 8934,
                'last_maintenance': '2024-11-30',
                'next_service': '2024-12-30'
            }
        ]
        
        for equipment in equipment_data:
            equipment_item = self.create_equipment_item(equipment)
            self.equipment_layout.addWidget(equipment_item)
            
        # Add stretch to push items to top
        self.equipment_layout.addStretch()
        
    def create_equipment_item(self, equipment_data):
        """Create individual equipment item"""
        item = QWidget()
        item.setFixedHeight(120)
        
        # Status color mapping
        status_colors = {
            'operational': ('#d4edda', '#28a745'),
            'maintenance': ('#fff3cd', '#ffc107'),
            'critical': ('#f8d7da', '#dc3545'),
            'offline': ('#e2e3e5', '#6c757d')
        }
        
        bg_color, border_color = status_colors.get(equipment_data['status'], ('#f8f9fa', '#dee2e6'))
        
        item.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: 8px;
                margin-bottom: 8px;
            }}
            QWidget:hover {{
                background-color: {self.adjust_color_brightness(bg_color, -0.05)};
                cursor: pointer;
            }}
        """)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Equipment icon and type
        icon_widget = QWidget()
        icon_widget.setFixedWidth(50)
        icon_layout = QVBoxLayout(icon_widget)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon based on equipment type
        type_icons = {
            'excavator': '🚚',
            'loader': '🚛',
            'truck': '🚜',
            'drill': '⚡',
            'crusher': '🏭'
        }
        
        equipment_type = equipment_data['type'].lower()
        for key in type_icons:
            if key in equipment_type:
                icon = type_icons[key]
                break
        else:
            icon = '🚛'
            
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        icon_layout.addWidget(icon_label)
        
        # Equipment details
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setSpacing(4)
        details_layout.setContentsMargins(0, 0, 0, 0)
        
        # Name and ID
        name_layout = QHBoxLayout()
        
        name_label = QLabel(f"{equipment_data['name']} ({equipment_data['id']})")
        name_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        
        status_label = QLabel(equipment_data['status'].upper())
        status_label.setStyleSheet(f"""
            QLabel {{
                color: {border_color};
                font-size: 10px;
                font-weight: bold;
            }}
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        name_layout.addWidget(status_label)
        
        # Type and location
        type_label = QLabel(f"Model: {equipment_data['type']}")
        type_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
            }
        """)
        
        location_label = QLabel(f"📍 {equipment_data['location']}")
        location_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 11px;
            }
        """)
        
        # Operator and metrics
        operator_layout = QHBoxLayout()
        
        operator_label = QLabel(f"👤 {equipment_data['operator']}")
        operator_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 11px;
            }
        """)
        
        fuel_label = QLabel(f"⛽ {equipment_data['fuel_level']}%")
        fuel_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 11px;
            }
        """)
        
        hours_label = QLabel(f"🕒 {equipment_data['operating_hours']}h")
        hours_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 11px;
            }
        """)
        
        operator_layout.addWidget(operator_label)
        operator_layout.addStretch()
        operator_layout.addWidget(fuel_label)
        operator_layout.addWidget(hours_label)
        
        details_layout.addLayout(name_layout)
        details_layout.addWidget(type_label)
        details_layout.addWidget(location_label)
        details_layout.addLayout(operator_layout)
        
        # Action buttons
        actions_widget = QWidget()
        actions_widget.setFixedWidth(100)
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setSpacing(4)
        
        track_btn = QPushButton("📍 Track")
        track_btn.setFixedHeight(25)
        track_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        details_btn = QPushButton("ℹ️ Details")
        details_btn.setFixedHeight(25)
        details_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        service_btn = QPushButton("🔧 Service")
        service_btn.setFixedHeight(25)
        service_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 3px;
                font-size: 10px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        
        actions_layout.addWidget(track_btn)
        actions_layout.addWidget(details_btn)
        actions_layout.addWidget(service_btn)
        
        layout.addWidget(icon_widget)
        layout.addWidget(details_widget, 1)
        layout.addWidget(actions_widget)
        
        return item
        
    def adjust_color_brightness(self, hex_color, factor):
        """Adjust the brightness of a hex color"""
        # Simple brightness adjustment - in production use proper color manipulation
        return hex_color
