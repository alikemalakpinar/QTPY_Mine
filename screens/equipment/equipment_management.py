"""Equipment Management - Anchor & Tag Management Screen"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime
from theme.theme import AicoMadenTakipTheme

class EquipmentScreen(QWidget):
    """Equipment management screen - Anchors & Tags"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        
        self.init_ui()
        
        # Auto refresh
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(3000)
        
        # Connect signals
        self.tracking.anchor_status_changed.connect(self.on_anchor_status_changed)
        self.tracking.tag_status_changed.connect(self.on_tag_status_changed)
        self.tracking.battery_alert.connect(self.on_battery_alert)
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Statistics Cards
        stats_layout = self.create_stats_cards()
        layout.addLayout(stats_layout)
        
        # Tab Widget for Anchors and Tags
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {AicoMadenTakipTheme.BORDER};
                border-radius: 12px;
                background: {AicoMadenTakipTheme.SURFACE};
            }}
            QTabBar::tab {{
                background: {AicoMadenTakipTheme.SURFACE};
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                border: 1px solid {AicoMadenTakipTheme.BORDER};
                padding: 12px 24px;
                margin-right: 4px;
                border-radius: 8px 8px 0 0;
                font-size: 14px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: {AicoMadenTakipTheme.PRIMARY};
                color: white;
                font-weight: 600;
            }}
            QTabBar::tab:hover {{
                background: {AicoMadenTakipTheme.SURFACE_HOVER};
            }}
        """)
        
        # Anchors Tab
        anchors_widget = self.create_anchors_tab()
        self.tab_widget.addTab(anchors_widget, "⚓ Anchors (Sabit Cihazlar)")
        
        # Tags Tab
        tags_widget = self.create_tags_tab()
        self.tab_widget.addTab(tags_widget, "🏷️ Tags (Personel Takip Cihazları)")
        
        layout.addWidget(self.tab_widget)
    
    def create_header(self):
        """Create header"""
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_layout = QVBoxLayout()
        title = QLabel("🔧 Ekipman Yönetimi")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {AicoMadenTakipTheme.TEXT_PRIMARY};
        """)
        
        subtitle = QLabel("Anchor ve Tag Cihazlarının Yönetimi ve İzlenmesi")
        subtitle.setStyleSheet(f"""
            font-size: 14px;
            color: {AicoMadenTakipTheme.TEXT_SECONDARY};
            margin-top: 5px;
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # Refresh Button
        refresh_btn = QPushButton("🔄 Yenile")
        refresh_btn.setStyleSheet(AicoMadenTakipTheme.get_button_style('primary'))
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        return header
    
    def create_stats_cards(self):
        """Create statistics cards"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        stats = self.tracking.get_statistics()
        
        # Anchor stats
        anchor_card = self.create_stat_card(
            "⚓ Anchors",
            str(stats['anchors']['total']),
            f"{stats['anchors']['online']} Online • {stats['anchors']['offline']} Offline",
            AicoMadenTakipTheme.PRIMARY
        )
        layout.addWidget(anchor_card)
        
        # Tag stats
        tag_card = self.create_stat_card(
            "🏷️ Tags",
            str(stats['tags']['total']),
            f"{stats['tags']['active']} Active • {stats['tags']['inactive']} Inactive",
            AicoMadenTakipTheme.SUCCESS
        )
        layout.addWidget(tag_card)
        
        # Battery warning
        total_low = stats['anchors']['low_battery'] + stats['tags']['low_battery']
        battery_card = self.create_stat_card(
            "🔋 Düşük Batarya",
            str(total_low),
            f"Anchors: {stats['anchors']['low_battery']} • Tags: {stats['tags']['low_battery']}",
            AicoMadenTakipTheme.WARNING if total_low > 0 else AicoMadenTakipTheme.SUCCESS
        )
        layout.addWidget(battery_card)
        
        # Average battery
        avg_battery = (stats['anchors']['avg_battery'] + stats['tags']['avg_battery']) / 2
        avg_card = self.create_stat_card(
            "📊 Ortalama Batarya",
            f"{avg_battery:.1f}%",
            f"Anchors: {stats['anchors']['avg_battery']:.1f}% • Tags: {stats['tags']['avg_battery']:.1f}%",
            AicoMadenTakipTheme.INFO
        )
        layout.addWidget(avg_card)
        
        return layout
    
    def create_stat_card(self, title, value, subtitle, color):
        """Create a stat card"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {AicoMadenTakipTheme.BORDER};
                padding: 20px;
            }}
            QWidget:hover {{
                border-color: {color};
                background: {AicoMadenTakipTheme.SURFACE_HOVER};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 13px;
            color: {AicoMadenTakipTheme.TEXT_SECONDARY};
            font-weight: 500;
        """)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {color};
        """)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"""
            font-size: 12px;
            color: {AicoMadenTakipTheme.TEXT_MUTED};
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        
        return card
    
    def create_anchors_tab(self):
        """Create anchors tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.anchor_search = QLineEdit()
        self.anchor_search.setPlaceholderText("🔍 Anchor ara...")
        self.anchor_search.textChanged.connect(self.filter_anchors)
        self.anchor_search.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px;
                font-size: 14px;
                border-radius: 8px;
            }}
        """)
        search_layout.addWidget(self.anchor_search)
        layout.addLayout(search_layout)
        
        # Anchors table
        self.anchors_table = QTableWidget()
        self.anchors_table.setColumnCount(9)
        self.anchors_table.setHorizontalHeaderLabels([
            'ID', 'İsim', 'Bölge', 'Durum', 'Batarya', 'Sinyal', 'Firmware', 'Son Bakım', 'İşlemler'
        ])
        
        self.anchors_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.anchors_table.setStyleSheet(f"""
            QTableWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border: none;
                border-radius: 12px;
                gridline-color: {AicoMadenTakipTheme.BORDER};
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {AicoMadenTakipTheme.BORDER};
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
            QTableWidget::item:selected {{
                background: {AicoMadenTakipTheme.PRIMARY_DARK};
            }}
            QHeaderView::section {{
                background: {AicoMadenTakipTheme.SURFACE_LIGHT};
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                border: none;
                padding: 12px;
                font-weight: 600;
                font-size: 12px;
            }}
        """)
        
        self.load_anchors_data()
        layout.addWidget(self.anchors_table)
        
        return widget
    
    def create_tags_tab(self):
        """Create tags tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.tag_search = QLineEdit()
        self.tag_search.setPlaceholderText("🔍 Tag ara...")
        self.tag_search.textChanged.connect(self.filter_tags)
        self.tag_search.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px;
                font-size: 14px;
                border-radius: 8px;
            }}
        """)
        search_layout.addWidget(self.tag_search)
        layout.addLayout(search_layout)
        
        # Tags table
        self.tags_table = QTableWidget()
        self.tags_table.setColumnCount(7)
        self.tags_table.setHorizontalHeaderLabels([
            'Tag ID', 'Personel', 'Durum', 'Batarya', 'Sinyal', 'Firmware', 'Son Görülme'
        ])
        
        self.tags_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tags_table.setStyleSheet(f"""
            QTableWidget {{
                background: {AicoMadenTakipTheme.SURFACE};
                border: none;
                border-radius: 12px;
                gridline-color: {AicoMadenTakipTheme.BORDER};
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {AicoMadenTakipTheme.BORDER};
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
            QTableWidget::item:selected {{
                background: {AicoMadenTakipTheme.PRIMARY_DARK};
            }}
            QHeaderView::section {{
                background: {AicoMadenTakipTheme.SURFACE_LIGHT};
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                border: none;
                padding: 12px;
                font-weight: 600;
                font-size: 12px;
            }}
        """)
        
        self.load_tags_data()
        layout.addWidget(self.tags_table)
        
        return widget
    
    def load_anchors_data(self):
        """Load anchors data into table"""
        anchors = self.tracking.get_anchors()
        self.anchors_table.setRowCount(len(anchors))
        
        for row, anchor in enumerate(anchors):
            # ID
            self.anchors_table.setItem(row, 0, QTableWidgetItem(anchor['id']))
            
            # Name
            self.anchors_table.setItem(row, 1, QTableWidgetItem(anchor['name']))
            
            # Zone
            self.anchors_table.setItem(row, 2, QTableWidgetItem(anchor['zone']))
            
            # Status
            status = anchor['status']
            status_text = '🟢 Online' if status == 'online' else '🔴 Offline'
            status_item = QTableWidgetItem(status_text)
            self.anchors_table.setItem(row, 3, status_item)
            
            # Battery
            battery = anchor['battery']
            battery_item = QTableWidgetItem(f"{battery}%")
            if battery < 70:
                battery_item.setForeground(QColor(AicoMadenTakipTheme.DANGER))
            elif battery < 85:
                battery_item.setForeground(QColor(AicoMadenTakipTheme.WARNING))
            else:
                battery_item.setForeground(QColor(AicoMadenTakipTheme.SUCCESS))
            self.anchors_table.setItem(row, 4, battery_item)
            
            # Signal
            signal = anchor['signal_strength']
            signal_item = QTableWidgetItem(f"{signal}%")
            self.anchors_table.setItem(row, 5, signal_item)
            
            # Firmware
            self.anchors_table.setItem(row, 6, QTableWidgetItem(anchor.get('firmware_version', 'N/A')))
            
            # Last maintenance
            self.anchors_table.setItem(row, 7, QTableWidgetItem(anchor.get('last_maintenance', 'N/A')))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 5, 5, 5)
            actions_layout.setSpacing(5)
            
            view_btn = QPushButton("👁️")
            view_btn.setFixedSize(30, 30)
            view_btn.setToolTip("Detayları Gör")
            view_btn.clicked.connect(lambda checked, a=anchor: self.view_anchor_details(a))
            
            actions_layout.addWidget(view_btn)
            actions_layout.addStretch()
            
            self.anchors_table.setCellWidget(row, 8, actions_widget)
    
    def load_tags_data(self):
        """Load tags data into table"""
        tags = self.tracking.get_tags()
        self.tags_table.setRowCount(len(tags))
        
        for row, tag in enumerate(tags):
            # Tag ID
            self.tags_table.setItem(row, 0, QTableWidgetItem(tag['id']))
            
            # Person name
            self.tags_table.setItem(row, 1, QTableWidgetItem(tag.get('person_name', 'N/A')))
            
            # Status
            status = tag['status']
            status_text = '🟢 Active' if status == 'active' else '⚫ Inactive'
            status_item = QTableWidgetItem(status_text)
            self.tags_table.setItem(row, 2, status_item)
            
            # Battery
            battery = tag['battery']
            battery_item = QTableWidgetItem(f"{battery}%")
            if battery < 20:
                battery_item.setForeground(QColor(AicoMadenTakipTheme.DANGER))
            elif battery < 40:
                battery_item.setForeground(QColor(AicoMadenTakipTheme.WARNING))
            else:
                battery_item.setForeground(QColor(AicoMadenTakipTheme.SUCCESS))
            self.tags_table.setItem(row, 3, battery_item)
            
            # Signal
            signal = tag['signal_strength']
            signal_item = QTableWidgetItem(f"{signal}%")
            self.tags_table.setItem(row, 4, signal_item)
            
            # Firmware
            self.tags_table.setItem(row, 5, QTableWidgetItem(tag.get('firmware_version', 'N/A')))
            
            # Last seen
            last_seen = tag.get('last_seen', 'N/A')
            if isinstance(last_seen, datetime):
                last_seen = last_seen.strftime('%H:%M:%S')
            self.tags_table.setItem(row, 6, QTableWidgetItem(str(last_seen)))
    
    def filter_anchors(self, text):
        """Filter anchors table"""
        for row in range(self.anchors_table.rowCount()):
            should_show = False
            for col in range(self.anchors_table.columnCount() - 1):
                item = self.anchors_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    should_show = True
                    break
            self.anchors_table.setRowHidden(row, not should_show)
    
    def filter_tags(self, text):
        """Filter tags table"""
        for row in range(self.tags_table.rowCount()):
            should_show = False
            for col in range(self.tags_table.columnCount()):
                item = self.tags_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    should_show = True
                    break
            self.tags_table.setRowHidden(row, not should_show)
    
    def view_anchor_details(self, anchor):
        """View anchor details"""
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Anchor Detayları - {anchor['id']}")
        msg.setText(f"""
<b>Anchor Bilgileri</b><br><br>
<b>ID:</b> {anchor['id']}<br>
<b>İsim:</b> {anchor['name']}<br>
<b>Bölge:</b> {anchor['zone']}<br>
<b>Durum:</b> {anchor['status']}<br>
<b>Batarya:</b> {anchor['battery']}%<br>
<b>Sinyal Gücü:</b> {anchor['signal_strength']}%<br>
<b>Firmware:</b> {anchor.get('firmware_version', 'N/A')}<br>
<b>Kapsama Alanı:</b> {anchor.get('coverage_radius', 100)}m<br>
<b>Koordinatlar:</b> X:{anchor['x']}, Y:{anchor['y']}, Z:{anchor.get('z', 0)}<br>
<b>Son Bakım:</b> {anchor.get('last_maintenance', 'N/A')}
        """)
        msg.setStyleSheet(AicoMadenTakipTheme.get_app_style())
        msg.exec()
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_anchors_data()
        self.load_tags_data()
    
    def on_anchor_status_changed(self, data):
        """Handle anchor status change"""
        self.refresh_data()
    
    def on_tag_status_changed(self, data):
        """Handle tag status change"""
        self.refresh_data()
    
    def on_battery_alert(self, data):
        """Handle battery alert"""
        # Could show notification or update UI
        pass
