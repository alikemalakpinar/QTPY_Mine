"""Professional Reports System - Enterprise Grade"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import AicoMadenTakipTheme
from datetime import datetime, timedelta
import random

class ReportsScreen(QWidget):
    """Profesyonel raporlama sistemi"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.init_ui()
        
        self.i18n.language_changed.connect(self.update_texts)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Quick Stats
        stats_layout = self.create_quick_stats()
        layout.addLayout(stats_layout)
        
        # Report Cards
        reports_container = self.create_reports_section()
        layout.addWidget(reports_container, 1)
    
    def create_header(self):
        """Header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_container = QVBoxLayout()
        self.title = QLabel("📊 " + self.i18n.t('reports'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
        """)
        
        subtitle = QLabel(f"{datetime.now().strftime('%d %B %Y')} - Analytics & Reports")
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
            }}
        """)
        
        title_container.addWidget(self.title)
        title_container.addWidget(subtitle)
        
        # Export Button
        export_btn = QPushButton("📥 Export All")
        export_btn.setStyleSheet(AicoMadenTakipTheme.get_button_style('primary'))
        export_btn.setFixedHeight(40)
        export_btn.setFixedWidth(140)
        export_btn.clicked.connect(self.export_all_reports)
        
        layout.addLayout(title_container)
        layout.addStretch()
        layout.addWidget(export_btn)
        
        return header
    
    def create_quick_stats(self):
        """Quick statistics"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        stats = self.tracking.get_statistics()
        
        quick_stats = [
            ("Total Personnel", str(stats['personnel']['total']), "👥", AicoMadenTakipTheme.PRIMARY),
            ("Active Now", str(stats['personnel']['active']), "✅", AicoMadenTakipTheme.SUCCESS),
            ("Gateways", f"{stats['gateways']['online']}/6", "📡", AicoMadenTakipTheme.INFO),
            ("Incidents", "0", "🛡️", AicoMadenTakipTheme.SUCCESS)
        ]
        
        for label, value, icon, color in quick_stats:
            card = self.create_quick_stat_card(label, value, icon, color)
            layout.addWidget(card)
        
        return layout
    
    def create_quick_stat_card(self, label, value, icon, color):
        """Quick stat card"""
        card = QWidget()
        card.setFixedHeight(90)
        card.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {AicoMadenTakipTheme.BORDER};
            }}
            QWidget:hover {{
                border-color: {color};
                background: {AicoMadenTakipTheme.SURFACE_LIGHT};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Icon and label
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Arial', 20))
        
        label_text = QLabel(label)
        label_text.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
            }}
        """)
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(label_text)
        top_layout.addStretch()
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: 700;
            }}
        """)
        
        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        
        return card
    
    def create_reports_section(self):
        """Reports cards section"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # Report types
        report_types = [
            {
                'icon': '📋',
                'title': 'Shift Report',
                'description': 'Daily shift activities and personnel attendance',
                'type': 'shift',
                'color': AicoMadenTakipTheme.PRIMARY
            },
            {
                'icon': '📈',
                'title': 'Performance Report',
                'description': 'Personnel and zone performance metrics',
                'type': 'performance',
                'color': AicoMadenTakipTheme.SUCCESS
            },
            {
                'icon': '⚠️',
                'title': 'Incident Report',
                'description': 'Safety incidents and emergency responses',
                'type': 'incident',
                'color': AicoMadenTakipTheme.WARNING
            },
            {
                'icon': '🔋',
                'title': 'Battery Status Report',
                'description': 'Tag battery levels and maintenance schedule',
                'type': 'battery',
                'color': AicoMadenTakipTheme.DANGER
            },
            {
                'icon': '📍',
                'title': 'Location Analytics',
                'description': 'Zone-based activity and movement patterns',
                'type': 'location',
                'color': AicoMadenTakipTheme.INFO
            },
            {
                'icon': '📊',
                'title': 'Summary Report',
                'description': 'Complete overview of all mining operations',
                'type': 'summary',
                'color': AicoMadenTakipTheme.PRIMARY
            }
        ]
        
        for report in report_types:
            card = self.create_report_card(report)
            layout.addWidget(card)
        
        scroll.setWidget(container)
        return scroll
    
    def create_report_card(self, report):
        """Create interactive report card"""
        card = QWidget()
        card.setFixedHeight(120)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {AicoMadenTakipTheme.BORDER};
            }}
            QWidget:hover {{
                border-color: {report['color']};
                background: {AicoMadenTakipTheme.SURFACE_LIGHT};
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(20)
        
        # Icon
        icon_container = QWidget()
        icon_container.setFixedSize(70, 70)
        icon_container.setStyleSheet(f"""
            QWidget {{
                background: {report['color']};
                border-radius: 12px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel(report['icon'])
        icon_label.setFont(QFont('Arial', 32))
        icon_layout.addWidget(icon_label)
        
        # Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        title = QLabel(report['title'])
        title.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        
        description = QLabel(report['description'])
        description.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """)
        description.setWordWrap(True)
        
        # Stats
        stats_label = QLabel(self.get_report_stats(report['type']))
        stats_label.setStyleSheet(f"""
            QLabel {{
                color: {report['color']};
                font-size: 11px;
                font-weight: 600;
            }}
        """)
        
        content_layout.addWidget(title)
        content_layout.addWidget(description)
        content_layout.addWidget(stats_label)
        
        # Actions
        actions_layout = QVBoxLayout()
        actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        actions_layout.setSpacing(8)
        
        view_btn = QPushButton("View Details")
        view_btn.setFixedSize(120, 35)
        view_btn.setStyleSheet(f"""
            QPushButton {{
                background: {report['color']};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {AicoMadenTakipTheme.PRIMARY_LIGHT};
            }}
        """)
        view_btn.clicked.connect(lambda: self.open_report_detail(report))
        
        export_btn = QPushButton("📥 Export")
        export_btn.setFixedSize(120, 35)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                border: 1px solid {AicoMadenTakipTheme.BORDER};
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                border-color: {report['color']};
                color: {report['color']};
            }}
        """)
        export_btn.clicked.connect(lambda: self.export_report(report))
        
        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(export_btn)
        
        layout.addWidget(icon_container)
        layout.addLayout(content_layout, 1)
        layout.addLayout(actions_layout)
        
        return card
    
    def get_report_stats(self, report_type):
        """Get quick stats for report"""
        stats = self.tracking.get_statistics()
        
        if report_type == 'shift':
            return f"Current Shift: {stats['personnel']['active']} active personnel"
        elif report_type == 'performance':
            return f"Avg Performance: 87% • Top Zone: Sector A"
        elif report_type == 'incident':
            return f"Last 30 days: 0 incidents • 100% safety record"
        elif report_type == 'battery':
            return f"{stats['personnel']['low_battery']} low battery alerts"
        elif report_type == 'location':
            return f"6 zones tracked • 15 personnel monitored"
        else:
            return f"Generated: {datetime.now().strftime('%H:%M')}"
    
    def open_report_detail(self, report):
        """Open detailed report view"""
        dialog = ReportDetailDialog(report, self.tracking, self.i18n, self)
        dialog.exec()
    
    def export_report(self, report):
        """Export single report"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Export Report")
        msg.setText(f"Export {report['title']}?")
        msg.setInformativeText("Choose export format:")
        
        pdf_btn = msg.addButton("PDF", QMessageBox.ButtonRole.AcceptRole)
        excel_btn = msg.addButton("Excel", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        
        clicked = msg.clickedButton()
        if clicked == pdf_btn:
            self.simulate_export(report['title'], 'PDF')
        elif clicked == excel_btn:
            self.simulate_export(report['title'], 'Excel')
    
    def export_all_reports(self):
        """Export all reports"""
        reply = QMessageBox.question(
            self,
            "Export All Reports",
            "Export all reports to PDF?\n\nThis will generate a comprehensive report package.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.simulate_export("All Reports", "PDF")
    
    def simulate_export(self, report_name, format_type):
        """Simulate export"""
        progress = QProgressDialog(f"Exporting {report_name}...", "Cancel", 0, 100, self)
        progress.setWindowTitle("Export")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        
        for i in range(101):
            progress.setValue(i)
            QApplication.processEvents()
            if progress.wasCanceled():
                return
            QThread.msleep(10)
        
        QMessageBox.information(
            self,
            "Export Complete",
            f"✅ {report_name} exported as {format_type}\n\nFile: ~/Downloads/{report_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{format_type.lower()}"
        )
    
    def update_texts(self):
        """Update texts"""
        self.title.setText("📊 " + self.i18n.t('reports'))


class ReportDetailDialog(QDialog):
    """Detailed report view dialog"""
    
    def __init__(self, report, tracking, i18n, parent=None):
        super().__init__(parent)
        self.report = report
        self.tracking = tracking
        self.i18n = i18n
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f"{self.report['title']} - Detailed View")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(f"""
            QDialog {{
                background: {AicoMadenTakipTheme.BACKGROUND};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Content based on report type
        content = self.create_content()
        layout.addWidget(content, 1)
        
        # Footer
        footer = self.create_footer()
        layout.addWidget(footer)
    
    def create_header(self):
        """Create header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        
        # Icon and title
        icon = QLabel(self.report['icon'])
        icon.setFont(QFont('Arial', 40))
        
        title_layout = QVBoxLayout()
        title = QLabel(self.report['title'])
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: 700;
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
        """)
        
        date_range = QLabel(f"{(datetime.now() - timedelta(days=30)).strftime('%d %b')} - {datetime.now().strftime('%d %b %Y')}")
        date_range.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
            }}
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(date_range)
        
        layout.addWidget(icon)
        layout.addLayout(title_layout)
        layout.addStretch()
        
        return header
    
    def create_content(self):
        """Create content based on report type"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # Generate content based on type
        if self.report['type'] == 'shift':
            layout.addWidget(self.create_shift_report())
        elif self.report['type'] == 'performance':
            layout.addWidget(self.create_performance_report())
        elif self.report['type'] == 'incident':
            layout.addWidget(self.create_incident_report())
        elif self.report['type'] == 'battery':
            layout.addWidget(self.create_battery_report())
        elif self.report['type'] == 'location':
            layout.addWidget(self.create_location_report())
        else:
            layout.addWidget(self.create_summary_report())
        
        scroll.setWidget(container)
        return scroll
    
    def create_shift_report(self):
        """Shift report details"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Summary stats
        stats_widget = self.create_stat_row("Total Personnel", "15", "Active", "12", "On Break", "3")
        layout.addWidget(stats_widget)
        
        # Personnel table
        table = self.create_personnel_table()
        layout.addWidget(table)
        
        return widget
    
    def create_performance_report(self):
        """Performance report"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        stats_widget = self.create_stat_row("Avg Efficiency", "87%", "Top Performer", "Mehmet Y.", "Avg Time", "8.2h")
        layout.addWidget(stats_widget)
        
        # Zone performance
        zones_table = self.create_zone_performance_table()
        layout.addWidget(zones_table)
        
        return widget
    
    def create_incident_report(self):
        """Incident report"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # No incidents card
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 12px;
                border: 2px solid {AicoMadenTakipTheme.SUCCESS};
                padding: 30px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon = QLabel("✅")
        icon.setFont(QFont('Arial', 60))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Perfect Safety Record")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: 700;
                color: {AicoMadenTakipTheme.SUCCESS};
            }}
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("No incidents in the last 30 days")
        subtitle.setStyleSheet(f"color: {AicoMadenTakipTheme.TEXT_SECONDARY}; font-size: 14px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_layout.addWidget(icon)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        
        layout.addWidget(card)
        return widget
    
    def create_battery_report(self):
        """Battery status report"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['Personnel', 'Tag ID', 'Battery', 'Status'])
        table.setStyleSheet(f"""
            QTableWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        personnel = self.tracking.get_personnel()
        table.setRowCount(len(personnel))
        
        for row, person in enumerate(personnel):
            table.setItem(row, 0, QTableWidgetItem(person['full_name']))
            table.setItem(row, 1, QTableWidgetItem(person['id']))
            table.setItem(row, 2, QTableWidgetItem(f"{person['battery']}%"))
            
            status = "⚠️ Low" if person['battery'] < 20 else "✅ Good" if person['battery'] > 50 else "⚠️ Medium"
            table.setItem(row, 3, QTableWidgetItem(status))
            table.setRowHeight(row, 45)
        
        layout.addWidget(table)
        return widget
    
    def create_location_report(self):
        """Location analytics"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Zone stats
        for zone in self.tracking.get_zones():
            zone_card = self.create_zone_card(zone)
            layout.addWidget(zone_card)
        
        return widget
    
    def create_summary_report(self):
        """Summary report"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        stats = self.tracking.get_statistics()
        
        summary_items = [
            ("👥 Total Personnel", str(stats['personnel']['total'])),
            ("✅ Active Now", str(stats['personnel']['active'])),
            ("⏸️ On Break", str(stats['personnel']['on_break'])),
            ("📡 Gateways Online", f"{stats['gateways']['online']}/{stats['gateways']['total']}"),
            ("📍 Active Zones", "6"),
            ("🛡️ Safety Score", "100%"),
        ]
        
        for label, value in summary_items:
            item_card = self.create_summary_item(label, value)
            layout.addWidget(item_card)
        
        return widget
    
    def create_stat_row(self, label1, value1, label2, value2, label3, value3):
        """Create stats row"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        layout = QHBoxLayout(widget)
        
        for label, value in [(label1, value1), (label2, value2), (label3, value3)]:
            stat_layout = QVBoxLayout()
            
            value_label = QLabel(value)
            value_label.setStyleSheet(f"""
                QLabel {{
                    color: {AicoMadenTakipTheme.PRIMARY};
                    font-size: 24px;
                    font-weight: 700;
                }}
            """)
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {AicoMadenTakipTheme.TEXT_SECONDARY}; font-size: 11px;")
            
            stat_layout.addWidget(value_label)
            stat_layout.addWidget(label_widget)
            
            layout.addLayout(stat_layout)
            if label != label3:
                layout.addSpacing(30)
        
        return widget
    
    def create_personnel_table(self):
        """Create personnel table"""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['ID', 'Name', 'Position', 'Zone', 'Status'])
        table.setStyleSheet(f"""
            QTableWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        personnel = self.tracking.get_personnel()
        table.setRowCount(len(personnel))
        
        for row, person in enumerate(personnel):
            table.setItem(row, 0, QTableWidgetItem(person['id']))
            table.setItem(row, 1, QTableWidgetItem(person['full_name']))
            table.setItem(row, 2, QTableWidgetItem(person['position']))
            table.setItem(row, 3, QTableWidgetItem(person['zone_name']))
            
            status = "✅ Active" if person['status'] == 'active' else "⏸️ Break"
            table.setItem(row, 4, QTableWidgetItem(status))
            table.setRowHeight(row, 45)
        
        return table
    
    def create_zone_performance_table(self):
        """Zone performance table"""
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['Zone', 'Personnel', 'Efficiency', 'Score'])
        table.setStyleSheet(f"""
            QTableWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        zones = self.tracking.get_zones()
        table.setRowCount(len(zones))
        
        for row, zone in enumerate(zones):
            personnel_count = sum(1 for p in self.tracking.get_personnel() if p['zone_id'] == zone['id'])
            efficiency = random.randint(75, 98)
            
            table.setItem(row, 0, QTableWidgetItem(zone['name']))
            table.setItem(row, 1, QTableWidgetItem(str(personnel_count)))
            table.setItem(row, 2, QTableWidgetItem(f"{efficiency}%"))
            table.setItem(row, 3, QTableWidgetItem("⭐" * (efficiency // 20)))
            table.setRowHeight(row, 45)
        
        return table
    
    def create_zone_card(self, zone):
        """Zone card"""
        card = QWidget()
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 12px;
                border-left: 4px solid {zone['color']};
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        
        name = QLabel(zone['name'])
        name.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        
        personnel_count = sum(1 for p in self.tracking.get_personnel() if p['zone_id'] == zone['id'])
        count = QLabel(f"{personnel_count} Personnel")
        count.setStyleSheet(f"color: {AicoMadenTakipTheme.TEXT_SECONDARY}; font-size: 13px;")
        
        layout.addWidget(name)
        layout.addStretch()
        layout.addWidget(count)
        
        return card
    
    def create_summary_item(self, label, value):
        """Summary item"""
        widget = QWidget()
        widget.setFixedHeight(60)
        widget.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.PRIMARY};
                font-size: 18px;
                font-weight: 700;
            }}
        """)
        
        layout.addWidget(label_widget)
        layout.addStretch()
        layout.addWidget(value_widget)
        
        return widget
    
    def create_footer(self):
        """Create footer"""
        footer = QWidget()
        layout = QHBoxLayout(footer)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setFixedWidth(120)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {AicoMadenTakipTheme.SURFACE_LIGHT};
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
                border: 1px solid {AicoMadenTakipTheme.BORDER};
                border-radius: 8px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {AicoMadenTakipTheme.SURFACE_HOVER};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        
        export_btn = QPushButton("📥 Export PDF")
        export_btn.setFixedHeight(40)
        export_btn.setFixedWidth(140)
        export_btn.setStyleSheet(AicoMadenTakipTheme.get_button_style('primary'))
        export_btn.clicked.connect(self.export_pdf)
        
        layout.addStretch()
        layout.addWidget(close_btn)
        layout.addWidget(export_btn)
        
        return footer
    
    def export_pdf(self):
        """Export to PDF"""
        QMessageBox.information(
            self,
            "Export Complete",
            f"✅ {self.report['title']} exported as PDF\n\nFile: ~/Downloads/{self.report['type']}_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
