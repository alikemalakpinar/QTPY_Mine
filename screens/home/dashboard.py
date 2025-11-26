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
        """Header oluştur"""
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('safety_dashboard'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        
        self.subtitle = QLabel(f"{self.i18n.t('realtime_monitoring')} • {datetime.now().strftime('%d %B %Y')}")
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
            }}
        """)
        
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        
        return header
    
    def create_stats_cards(self):
        """İstatistik kartları oluştur"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        stats = self.tracking.get_statistics()
        
        self.cards_data = [
            ('active_personnel', '👷', str(stats['personnel']['active']), 
             self.i18n.t('underground'), MineTrackerTheme.PRIMARY),
            ('total_personnel', '👥', f"{stats['personnel']['total']}", 
             'Total Personnel', MineTrackerTheme.SUCCESS),
            ('gateways_online', '📡', f"{stats['gateways']['online']}/{stats['gateways']['total']}",
             'Gateway Status', MineTrackerTheme.SUCCESS),
            ('safety_incidents', '🛡️', '0', 
             '24 ' + self.i18n.t('incident_free'), MineTrackerTheme.SUCCESS)
        ]
        
        self.cards = []
        for title_key, icon, value, subtitle, color in self.cards_data:
            card = self.create_stat_card(title_key, icon, value, subtitle, color)
            self.cards.append((card, title_key, icon, subtitle, color))
            layout.addWidget(card)
        
        return layout
    
    def create_stat_card(self, title_key, icon, value, subtitle, color):
        """Tek bir istatistik kartı"""
        card = QWidget()
        card.setFixedHeight(130)
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=True))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Üst kısım
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Arial', 24))
        
        title_label = QLabel(self.i18n.t(title_key))
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 12px;
                font-weight: 500;
                text-transform: uppercase;
            }}
        """)
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        
        # Değer
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 36px;
                font-weight: 700;
            }}
        """)
        value_label.setProperty('value_label', True)
        
        # Alt yazı
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 11px;
            }}
        """)
        
        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        
        return card
    
    def create_activity_section(self):
        """Son aktiviteler bölümü"""
        section = QWidget()
        section.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Başlık
        self.activity_title = QLabel(self.i18n.t('recent_activity'))
        self.activity_title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(self.activity_title)
        
        # Aktivite listesi
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet(f"""
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
                font-size: 13px;
            }}
            QListWidget::item:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
            }}
        """)
        
        self.populate_activities()
        layout.addWidget(self.activity_list)
        
        return section
    
    def populate_activities(self):
        """Aktiviteleri doldur"""
        self.activity_list.clear()
        
        personnel = self.tracking.get_personnel()[:5]
        for person in personnel:
            time_diff = datetime.now() - person['last_update']
            seconds = time_diff.total_seconds()
            
            if seconds < 60:
                time_str = self.i18n.t('just_now')
            elif seconds < 3600:
                time_str = f"{int(seconds/60)} {self.i18n.t('min_ago')}"
            else:
                time_str = f"{int(seconds/3600)} {self.i18n.t('hour_ago')}"
            
            status_icon = '✅' if person['status'] == 'active' else '🚨' if person['status'] == 'emergency' else '⌛'
            item_text = f"{status_icon} {person['full_name']} - {person['zone_name']} • {time_str}"
            self.activity_list.addItem(item_text)
    
    def create_zones_section(self):
        """Bölgeler bölümü"""
        section = QWidget()
        section.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel('📍 ' + self.i18n.t('zones'))
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)
        
        # Bölge listesi
        zones = self.tracking.get_zones()
        for zone in zones:
            zone_widget = self.create_zone_item(zone)
            layout.addWidget(zone_widget)
        
        layout.addStretch()
        
        return section
    
    def create_zone_item(self, zone):
        """Bölge item'ı"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Renk göstergesi
        color_indicator = QLabel('●')
        color_indicator.setStyleSheet(f"color: {zone['color']}; font-size: 20px;")
        
        # İsim
        name_label = QLabel(zone['name'])
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 500;
            }}
        """)
        
        # Personel sayısı
        count = sum(1 for p in self.tracking.get_personnel() if p['zone_id'] == zone['id'])
        count_label = QLabel(f"{count} 👤")
        count_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """)
        
        layout.addWidget(color_indicator)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(count_label)
        
        return widget
    
    def refresh_stats(self):
        """İstatistikleri yenile"""
        stats = self.tracking.get_statistics()
        
        # Kartları güncelle
        for card, title_key, icon, subtitle, color in self.cards:
            value_label = card.findChild(QLabel, '', Qt.FindChildOption.FindDirectChildrenOnly)
            for child in card.findChildren(QLabel):
                if child.property('value_label'):
                    if title_key == 'active_personnel':
                        child.setText(str(stats['personnel']['active']))
                    elif title_key == 'total_personnel':
                        child.setText(str(stats['personnel']['total']))
                    elif title_key == 'gateways_online':
                        child.setText(f"{stats['gateways']['online']}/{stats['gateways']['total']}")
        
        # Aktiviteleri güncelle
        self.populate_activities()
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('safety_dashboard'))
        self.subtitle.setText(f"{self.i18n.t('realtime_monitoring')} • {datetime.now().strftime('%d %B %Y')}")
        self.activity_title.setText(self.i18n.t('recent_activity'))
        self.refresh_stats()
