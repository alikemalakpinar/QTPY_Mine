"""Ultra Modern Dashboard - Real-time Analytics & Trilateration Visualization"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime
from components.charts import RealtimeChart, ModernStatCard
import random

class DashboardScreen(QWidget):
    """Ultra modern dashboard - Gelişmiş tracking metrikleri"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        
        # Chart data storage
        self.avg_accuracy_history = []
        self.active_personnel_history = []
        self.avg_battery_history = []
        
        self.init_ui()
        
        # Güncellemeleri dinle
        self.tracking.location_updated.connect(self.on_location_updated)
        self.tracking.position_calculated.connect(self.on_position_calculated)
        self.i18n.language_changed.connect(self.update_texts)
        
        # Periyodik güncelleme
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_all)
        self.update_timer.start(3000)
    
    def init_ui(self):
        """UI'yi başlat - Ultra Modern"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(35, 35, 35, 35)
        
        # Header with mode selector
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Modern stat cards (gradient)
        stats_layout = self.create_modern_stats_cards()
        main_layout.addLayout(stats_layout)
        
        # Real-time charts row
        charts_layout = self.create_charts_section()
        main_layout.addLayout(charts_layout)
        
        # Bottom row: Activity + Position Metrics
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(25)
        
        # Sol: Recent calculations & activity
        left_section = self.create_recent_calculations_section()
        bottom_layout.addWidget(left_section, 3)
        
        # Sağ: Anchor status & metrics
        right_section = self.create_anchor_metrics_section()
        bottom_layout.addWidget(right_section, 2)
        
        main_layout.addLayout(bottom_layout, 1)
    
    def create_header(self):
        """Header with tracking mode selector"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Title section
        title_section = QVBoxLayout()
        title_section.setSpacing(5)
        
        self.title = QLabel("🎯 " + self.i18n.t('safety_dashboard'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 36px;
                font-weight: 800;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -1px;
            }}
        """)
        
        self.subtitle = QLabel(f"{self.i18n.t('realtime_monitoring')} • {datetime.now().strftime('%d %B %Y, %H:%M')}")
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 15px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
            }}
        """)
        
        title_section.addWidget(self.title)
        title_section.addWidget(self.subtitle)
        
        layout.addLayout(title_section)
        layout.addStretch()
        
        # Mode selector
        mode_group = QWidget()
        mode_group.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 10px;
                border: 1px solid {MineTrackerTheme.BORDER};
                padding: 8px;
            }}
        """)
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setSpacing(5)
        mode_layout.setContentsMargins(5, 5, 5, 5)
        
        mode_label = QLabel("📡 Mode:")
        mode_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-weight: 600;")
        mode_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Hybrid', 'Simulation', 'TCP Only'])
        self.mode_combo.setStyleSheet(f"""
            QComboBox {{
                background: {MineTrackerTheme.SURFACE_LIGHT};
                border: 1px solid {MineTrackerTheme.BORDER};
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: 600;
                min-width: 120px;
            }}
            QComboBox:hover {{
                border-color: {MineTrackerTheme.PRIMARY};
            }}
        """)
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        layout.addWidget(mode_group)
        
        return header
    
    def create_modern_stats_cards(self):
        """Ultra modern gradient stat cards"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        stats = self.tracking.get_statistics()
        
        # Active Personnel Card
        self.card_active = ModernStatCard(
            icon='👷',
            title=self.i18n.t('active_personnel'),
            value=str(stats['personnel']['active']),
            subtitle=f"/{stats['personnel']['total']} " + self.i18n.t('underground'),
            color=MineTrackerTheme.PRIMARY,
            gradient=True
        )
        self.card_active.clicked.connect(lambda: print("Navigate to Personnel"))
        
        # Anchors Online Card
        self.card_anchors = ModernStatCard(
            icon='⚓',
            title='Anchors',
            value=f"{stats['anchors']['online']}/{stats['anchors']['total']}",
            subtitle='Online • Coverage: 100%',
            color=MineTrackerTheme.SUCCESS,
            gradient=True
        )
        
        # Tags Active Card
        self.card_tags = ModernStatCard(
            icon='🏷️',
            title='Tags',
            value=f"{stats['tags']['active']}/{stats['tags']['total']}",
            subtitle=f"Active • Battery Avg: {stats['tags']['avg_battery']:.0f}%",
            color=MineTrackerTheme.INFO,
            gradient=True
        )
        
        # Position Accuracy Card (average)
        avg_accuracy = self.calculate_avg_accuracy()
        self.card_accuracy = ModernStatCard(
            icon='🎯',
            title='Avg Accuracy',
            value=f"{avg_accuracy:.2f}m",
            subtitle='Trilateration + Kalman Filter',
            color=MineTrackerTheme.WARNING if avg_accuracy > 1.0 else MineTrackerTheme.SUCCESS,
            gradient=True
        )
        
        layout.addWidget(self.card_active)
        layout.addWidget(self.card_anchors)
        layout.addWidget(self.card_tags)
        layout.addWidget(self.card_accuracy)
        
        return layout
    
    def create_charts_section(self):
        """Real-time charts - Position accuracy, battery, active personnel"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Accuracy Chart
        accuracy_container = self.create_chart_container("🎯 Position Accuracy (m)", "realtime")
        accuracy_layout = QVBoxLayout()
        accuracy_layout.setContentsMargins(15, 15, 15, 15)
        
        self.accuracy_chart = RealtimeChart("Accuracy (m)", max_points=30, y_range=(0, 2))
        self.accuracy_chart.line_color = QColor(MineTrackerTheme.SUCCESS)
        self.accuracy_chart.fill_color = QColor(MineTrackerTheme.SUCCESS)
        self.accuracy_chart.fill_color.setAlpha(50)
        
        accuracy_layout.addWidget(self.accuracy_chart)
        accuracy_container.setLayout(accuracy_layout)
        
        # Battery Chart
        battery_container = self.create_chart_container("🔋 Avg Battery Level (%)", "realtime")
        battery_layout = QVBoxLayout()
        battery_layout.setContentsMargins(15, 15, 15, 15)
        
        self.battery_chart = RealtimeChart("Battery %", max_points=30, y_range=(0, 100))
        self.battery_chart.line_color = QColor(MineTrackerTheme.WARNING)
        self.battery_chart.fill_color = QColor(MineTrackerTheme.WARNING)
        self.battery_chart.fill_color.setAlpha(50)
        
        battery_layout.addWidget(self.battery_chart)
        battery_container.setLayout(battery_layout)
        
        # Active Personnel Chart
        personnel_container = self.create_chart_container("👷 Active Personnel", "realtime")
        personnel_layout = QVBoxLayout()
        personnel_layout.setContentsMargins(15, 15, 15, 15)
        
        self.personnel_chart = RealtimeChart("Personnel", max_points=30, y_range=(0, 20))
        self.personnel_chart.line_color = QColor(MineTrackerTheme.PRIMARY)
        self.personnel_chart.fill_color = QColor(MineTrackerTheme.PRIMARY)
        self.personnel_chart.fill_color.setAlpha(50)
        
        personnel_layout.addWidget(self.personnel_chart)
        personnel_container.setLayout(personnel_layout)
        
        layout.addWidget(accuracy_container)
        layout.addWidget(battery_container)
        layout.addWidget(personnel_container)
        
        return layout
    
    def create_chart_container(self, title, badge_text=""):
        """Chart container with modern styling"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        return container
    
    def create_recent_calculations_section(self):
        """Son trilateration hesaplamaları"""
        section = QWidget()
        section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📐 Recent Position Calculations")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        
        badge = QLabel("LIVE")
        badge.setStyleSheet(f"""
            QLabel {{
                background: {MineTrackerTheme.SUCCESS};
                color: white;
                font-size: 10px;
                font-weight: 700;
                padding: 4px 8px;
                border-radius: 4px;
            }}
        """)
        badge.setFixedHeight(22)
        
        header_layout.addWidget(title)
        header_layout.addWidget(badge)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Recent calculations list
        self.calculations_list = QListWidget()
        self.calculations_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
            }}
            QListWidget::item:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
            }}
        """)
        
        layout.addWidget(self.calculations_list)
        
        return section
    
    def create_anchor_metrics_section(self):
        """Anchor durum ve metrikleri"""
        section = QWidget()
        section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        title = QLabel("⚓ Anchor Status")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)
        
        # Anchor list
        anchors = self.tracking.get_anchors()
        
        for anchor in anchors:
            anchor_widget = self.create_anchor_status_widget(anchor)
            layout.addWidget(anchor_widget)
        
        layout.addStretch()
        
        return section
    
    def create_anchor_status_widget(self, anchor):
        """Tek bir anchor durum widget'ı"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        
        # Status indicator
        status_dot = QLabel("●")
        status_dot.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.SUCCESS if anchor['status'] == 'online' else MineTrackerTheme.DANGER};
                font-size: 20px;
            }}
        """)
        
        # Name
        name_label = QLabel(anchor['name'])
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        
        # Battery
        battery = anchor['battery']
        battery_label = QLabel(f"🔋 {battery}%")
        if battery < 70:
            color = MineTrackerTheme.DANGER
        elif battery < 85:
            color = MineTrackerTheme.WARNING
        else:
            color = MineTrackerTheme.SUCCESS
        
        battery_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 11px;
                font-weight: 600;
            }}
        """)
        
        # Signal
        signal_label = QLabel(f"📶 {anchor['signal_strength']}%")
        signal_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 11px;
            }}
        """)
        
        layout.addWidget(status_dot)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(battery_label)
        layout.addWidget(signal_label)
        
        return widget
    
    def calculate_avg_accuracy(self):
        """Ortalama pozisyon doğruluğunu hesapla"""
        personnel = self.tracking.get_personnel()
        accuracies = [p.get('position_accuracy', 0) for p in personnel if p.get('position_accuracy', 0) > 0]
        
        if not accuracies:
            return 0.5  # Default
        
        return sum(accuracies) / len(accuracies)
    
    def on_mode_changed(self, mode_text):
        """Tracking mode değiştiğinde"""
        mode_map = {
            'Hybrid': 'hybrid',
            'Simulation': 'simulation',
            'TCP Only': 'tcp'
        }
        
        mode = mode_map.get(mode_text, 'hybrid')
        self.tracking.set_mode(mode)
        print(f"📡 Tracking mode changed: {mode}")
    
    def on_location_updated(self, data):
        """Konum güncellendiğinde"""
        self.refresh_stats_quick()
    
    def on_position_calculated(self, data):
        """Yeni pozisyon hesaplandığında"""
        # Recent calculations listesine ekle
        tag_id = data.get('tag_id')
        accuracy = data.get('accuracy', 0)
        final_pos = data.get('final')
        anchors_used = data.get('anchors_used', [])
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        item_text = f"[{timestamp}] {tag_id} → ({final_pos[0]:.1f}, {final_pos[1]:.1f}) ± {accuracy:.2f}m [Anchors: {', '.join(anchors_used)}]"
        
        self.calculations_list.insertItem(0, item_text)
        
        # Limit list size
        while self.calculations_list.count() > 15:
            self.calculations_list.takeItem(self.calculations_list.count() - 1)
    
    def refresh_all(self):
        """Tüm verileri yenile"""
        stats = self.tracking.get_statistics()
        
        # Update cards
        self.card_active.update_value(str(stats['personnel']['active']))
        self.card_active.update_subtitle(f"/{stats['personnel']['total']} " + self.i18n.t('underground'))
        
        self.card_anchors.update_value(f"{stats['anchors']['online']}/{stats['anchors']['total']}")
        
        self.card_tags.update_value(f"{stats['tags']['active']}/{stats['tags']['total']}")
        self.card_tags.update_subtitle(f"Active • Battery Avg: {stats['tags']['avg_battery']:.0f}%")
        
        avg_accuracy = self.calculate_avg_accuracy()
        self.card_accuracy.update_value(f"{avg_accuracy:.2f}m")
        self.card_accuracy.color = QColor(MineTrackerTheme.WARNING if avg_accuracy > 1.0 else MineTrackerTheme.SUCCESS)
        
        # Update charts
        self.accuracy_chart.add_data_point(avg_accuracy)
        self.battery_chart.add_data_point(stats['tags']['avg_battery'])
        self.personnel_chart.add_data_point(stats['personnel']['active'])
        
        # Update time
        self.subtitle.setText(f"{self.i18n.t('realtime_monitoring')} • {datetime.now().strftime('%d %B %Y, %H:%M:%S')}")
    
    def refresh_stats_quick(self):
        """Hızlı stat güncelleme (ağır işlemler yok)"""
        stats = self.tracking.get_statistics()
        self.card_active.update_value(str(stats['personnel']['active']))
        self.card_anchors.update_value(f"{stats['anchors']['online']}/{stats['anchors']['total']}")
        self.card_tags.update_value(f"{stats['tags']['active']}/{stats['tags']['total']}")
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText("🎯 " + self.i18n.t('safety_dashboard'))
        self.subtitle.setText(f"{self.i18n.t('realtime_monitoring')} • {datetime.now().strftime('%d %B %Y, %H:%M')}")
        self.refresh_all()

