from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime, timedelta
import random

class PeopleListScreen(QWidget):
    """Personnel tracking and management screen"""
    
    def __init__(self):
        super().__init__()
        self.personnel_data = []
        self.init_ui()
        self.load_personnel_data()
        
    def init_ui(self):
        """Initialize personnel screen UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header = self.create_header()
        layout.addWidget(header)
        
        # Statistics row
        stats_row = self.create_stats_row()
        layout.addWidget(stats_row)
        
        # Main content
        content = self.create_main_content()
        layout.addWidget(content, 1)
        
    def create_header(self):
        """Create personnel screen header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 20)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("👥 Personnel Management")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel("Real-time tracking and safety monitoring of all mine personnel")
        subtitle.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Search and filter controls
        controls = self.create_header_controls()
        
        layout.addWidget(title_widget)
        layout.addStretch()
        layout.addWidget(controls)
        
        return header
        
    def create_header_controls(self):
        """Create header control buttons"""
        controls = QWidget()
        controls.setFixedWidth(400)
        layout = QHBoxLayout(controls)
        layout.setSpacing(10)
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search personnel...")
        search_box.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
        """)
        
        # Add person button
        add_btn = QPushButton("+ Add Person")
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
        
        # Export button
        export_btn = QPushButton("📊 Export")
        export_btn.setStyleSheet("""
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
        
        layout.addWidget(search_box, 1)
        layout.addWidget(add_btn)
        layout.addWidget(export_btn)
        
        return controls
        
    def create_stats_row(self):
        """Create personnel statistics row"""
        stats_widget = QWidget()
        layout = QHBoxLayout(stats_widget)
        layout.setSpacing(20)
        
        # Statistics data
        stats = [
            ("On Shift", "147", "👷", "#28a745", "Day shift active"),
            ("Off Duty", "89", "🏠", "#6c757d", "Night shift & weekend"),
            ("In Training", "23", "📚", "#ffc107", "Safety certification"),
            ("Medical Leave", "5", "🏥", "#dc3545", "Temporary absence"),
            ("Emergency Contacts", "264", "📞", "#17a2b8", "Updated profiles"),
        ]
        
        for title, value, icon, color, subtitle in stats:
            card = self.create_stat_card(title, value, icon, color, subtitle)
            layout.addWidget(card)
            
        return stats_widget
        
    def create_stat_card(self, title, value, icon, color, subtitle):
        """Create personnel statistics card"""
        card = QWidget()
        card.setFixedHeight(100)
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
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(6)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 16))
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
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
                font-size: 24px;
                font-weight: bold;
            }}
        """)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 10px;
            }
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        
        return card
        
    def create_main_content(self):
        """Create main content area"""
        content = QWidget()
        layout = QHBoxLayout(content)
        layout.setSpacing(20)
        
        # Personnel list (left side)
        personnel_list = self.create_personnel_list()
        
        # Personnel details and location (right side)
        details_panel = self.create_details_panel()
        
        layout.addWidget(personnel_list, 2)
        layout.addWidget(details_panel, 3)
        
        return content
        
    def create_personnel_list(self):
        """Create personnel list panel"""
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
        
        # Header with filters
        header_layout = QHBoxLayout()
        
        title = QLabel("Personnel List")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        # Status filter
        status_filter = QComboBox()
        status_filter.addItems(["All Personnel", "On Shift", "Off Duty", "In Training", "Medical Leave"])
        status_filter.setStyleSheet("""
            QComboBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 120px;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Status:"))
        header_layout.addWidget(status_filter)
        
        layout.addLayout(header_layout)
        
        # Personnel table
        self.personnel_table = QTableWidget()
        self.setup_personnel_table()
        layout.addWidget(self.personnel_table, 1)
        
        return panel
        
    def setup_personnel_table(self):
        """Setup personnel data table"""
        headers = ["ID", "Name", "Role", "Shift", "Location", "Status", "Last Check-in", "Actions"]
        self.personnel_table.setColumnCount(len(headers))
        self.personnel_table.setHorizontalHeaderLabels(headers)
        
        # Style the table
        self.personnel_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #e9ecef;
                border: none;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #495057;
                border: none;
                border-bottom: 1px solid #dee2e6;
                font-weight: 600;
                font-size: 12px;
                padding: 10px 8px;
            }
        """)
        
        # Configure table properties
        self.personnel_table.setAlternatingRowColors(True)
        self.personnel_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.personnel_table.verticalHeader().setVisible(False)
        self.personnel_table.setShowGrid(True)
        
        # Set column widths
        header = self.personnel_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i, width in enumerate([80, 150, 120, 80, 150, 100, 120, 100]):
            self.personnel_table.setColumnWidth(i, width)
            
    def create_details_panel(self):
        """Create personnel details panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Personnel profile section
        profile_section = self.create_profile_section()
        layout.addWidget(profile_section, 1)
        
        # Location tracking section
        location_section = self.create_location_section()
        layout.addWidget(location_section, 1)
        
        # Safety metrics section
        safety_section = self.create_safety_section()
        layout.addWidget(safety_section, 1)
        
        return panel
        
    def create_profile_section(self):
        """Create personnel profile section"""
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
        title = QLabel("👤 Personnel Profile")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Profile info (placeholder)
        profile_info = QLabel("""
<b>John Smith</b> (ID: W-1247)<br>
<b>Role:</b> Mining Engineer<br>
<b>Department:</b> Operations<br>
<b>Shift:</b> Day Shift (06:00-14:00)<br>
<b>Experience:</b> 8 years<br>
<b>Certifications:</b> Safety Level 3, Equipment Operator<br>
<b>Emergency Contact:</b> Jane Smith (555-0123)<br>
<b>Medical Info:</b> No restrictions
        """)
        profile_info.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 13px;
                line-height: 1.5;
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        layout.addWidget(profile_info)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        edit_btn = QPushButton("✏️ Edit Profile")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        contact_btn = QPushButton("📞 Contact")
        contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(contact_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        return section
        
    def create_location_section(self):
        """Create location tracking section"""
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
        title = QLabel("📍 Real-time Location")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        status_indicator = QLabel("🟢 TRACKED")
        status_indicator.setStyleSheet("""
            QLabel {
                color: #28a745;
                font-size: 12px;
                font-weight: bold;
                background-color: #d4edda;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(status_indicator)
        
        layout.addLayout(header_layout)
        
        # Location details
        location_info = QLabel("""
<b>Current Location:</b> Sector B - Level 2<br>
<b>Zone:</b> Excavation Area Alpha<br>
<b>Coordinates:</b> X: -245.7, Y: 156.3<br>
<b>Last Update:</b> 2 seconds ago<br>
<b>Movement Status:</b> Active<br>
<b>Heart Rate:</b> 78 BPM (Normal)<br>
<b>Environmental:</b> Temp: 22°C, Safe levels
        """)
        location_info.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 12px;
                line-height: 1.5;
                background-color: #f8f9fa;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        layout.addWidget(location_info)
        
        # Mini location map placeholder
        mini_map = QWidget()
        mini_map.setFixedHeight(80)
        mini_map.setStyleSheet("""
            QWidget {
                background-color: #e9ecef;
                border-radius: 6px;
                border: 1px dashed #adb5bd;
            }
        """)
        
        map_layout = QVBoxLayout(mini_map)
        map_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        map_label = QLabel("📍 Live Position Map")
        map_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        map_layout.addWidget(map_label)
        layout.addWidget(mini_map)
        
        return section
        
    def create_safety_section(self):
        """Create safety metrics section"""
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
        title = QLabel("🛡️ Safety Metrics")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Safety metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(10)
        
        safety_metrics = [
            ("Days Since Incident", "234", "#28a745"),
            ("Safety Score", "98%", "#17a2b8"),
            ("Training Hours", "156", "#ffc107"),
            ("Incidents Reported", "0", "#dc3545"),
        ]
        
        for i, (metric, value, color) in enumerate(safety_metrics):
            metric_widget = self.create_safety_metric(metric, value, color)
            row = i // 2
            col = i % 2
            metrics_grid.addWidget(metric_widget, row, col)
            
        layout.addLayout(metrics_grid)
        
        # Recent safety activities
        activities_label = QLabel("Recent Safety Activities:")
        activities_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 13px;
                font-weight: 600;
                margin-top: 10px;
            }
        """)
        layout.addWidget(activities_label)
        
        activities_list = QLabel("""
• Completed monthly safety training (Dec 15)
• Participated in evacuation drill (Dec 10)
• Reported near-miss incident (Dec 8)
• Updated emergency contact info (Dec 5)
        """)
        activities_list.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                line-height: 1.6;
                background-color: #f8f9fa;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        layout.addWidget(activities_list)
        
        return section
        
    def create_safety_metric(self, metric, value, color):
        """Create individual safety metric widget"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color}15;
                border-radius: 6px;
                border: 1px solid {color}30;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: bold;
            }}
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        metric_label = QLabel(metric)
        metric_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 10px;
                font-weight: 500;
            }
        """)
        metric_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(metric_label)
        
        return widget
        
    def load_personnel_data(self):
        """Load personnel data into the table"""
        # Sample personnel data
        personnel_data = [
            ["W-001", "John Smith", "Mining Engineer", "Day", "Sector B-L2", "🟢 Active", "2 min ago"],
            ["W-002", "Sarah Johnson", "Safety Inspector", "Day", "Sector A-L1", "🟢 Active", "1 min ago"],
            ["W-003", "Mike Wilson", "Equipment Operator", "Day", "Processing", "🟢 Active", "3 min ago"],
            ["W-004", "Lisa Brown", "Supervisor", "Day", "Control Room", "🟢 Active", "30 sec ago"],
            ["W-005", "David Chen", "Maintenance Tech", "Day", "Workshop", "🟡 Break", "15 min ago"],
            ["W-006", "Anna Martinez", "Geologist", "Day", "Sector C-L3", "🟢 Active", "5 min ago"],
            ["W-007", "Robert Taylor", "Drill Operator", "Night", "Sector D-L1", "🔴 Off Duty", "8 hours ago"],
            ["W-008", "Emily Davis", "Environmental Tech", "Day", "Lab", "🟢 Active", "1 min ago"],
        ]
        
        self.personnel_table.setRowCount(len(personnel_data))
        
        for row, person in enumerate(personnel_data):
            for col, data in enumerate(person):
                if col < len(person):  # Regular data columns
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Color coding for status
                    if col == 5:  # Status column
                        if "🟢" in data:
                            item.setForeground(QColor("#28a745"))
                        elif "🟡" in data:
                            item.setForeground(QColor("#ffc107"))
                        elif "🔴" in data:
                            item.setForeground(QColor("#dc3545"))
                            
                    self.personnel_table.setItem(row, col, item)
            
            # Add action buttons in the last column
            self.add_action_buttons(row)
            
    def add_action_buttons(self, row):
        """Add action buttons to a table row"""
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 2, 5, 2)
        actions_layout.setSpacing(3)
        
        # View details button
        view_btn = QPushButton("👁️")
        view_btn.setFixedSize(25, 25)
        view_btn.setToolTip("View Details")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        # Contact button
        contact_btn = QPushButton("📞")
        contact_btn.setFixedSize(25, 25)
        contact_btn.setToolTip("Contact")
        contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        # Track button
        track_btn = QPushButton("📍")
        track_btn.setFixedSize(25, 25)
        track_btn.setToolTip("Track Location")
        track_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #117a8b;
            }
        """)
        
        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(contact_btn)
        actions_layout.addWidget(track_btn)
        actions_layout.addStretch()
        
        self.personnel_table.setCellWidget(row, 7, actions_widget)
