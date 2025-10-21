"""Ana dashboard ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime

class DashboardScreen(QWidget):
    """Ana dashboard"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.init_ui()
        
        # Güncellemeleri dinle
        self.tracking.location_updated.connect(self.refresh_stats)
        self.i18n.language_changed.connect(self.update_texts)
        
        # Periyodik güncelleme
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_stats)
        self.update_timer.start(5000)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # İstatistik kartları
        stats_layout = self.create_stats_cards()
        layout.addLayout(stats_layout)
        
        # Ana içerik
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Sol: Son aktiviteler
        left_col = self.create_activity_section()
        content_layout.addWidget(left_col, 2)
        
        # Sağ: Bölge durumu
        right_col = self.create_zones_section()
        content_layout.addWidget(right_col, 1)
        
        layout.addLayout(content_layout, 1)
    
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
            ('active_personnel', '👥', str(stats['personnel']['active']), 
             self.i18n.t('underground'), MineTrackerTheme.PRIMARY),
            ('equipment_online', '🚜', f"{stats['equipment']['online']}/{stats['equipment']['total']}",
             self.i18n.t('operational'), MineTrackerTheme.SUCCESS),
            ('safety_incidents', '🛡️', '0', 
             '24 ' + self.i18n.t('incident_free'), MineTrackerTheme.SUCCESS),
            ('zone_temperature', '🌡️', '22°C',
             self.i18n.t('within_limits'), MineTrackerTheme.WARNING)
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
                    elif title_key == 'equipment_online':
                        child.setText(f"{stats['equipment']['online']}/{stats['equipment']['total']}")
        
        # Aktiviteleri güncelle
        self.populate_activities()
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('safety_dashboard'))
        self.subtitle.setText(f"{self.i18n.t('realtime_monitoring')} • {datetime.now().strftime('%d %B %Y')}")
        self.activity_title.setText(self.i18n.t('recent_activity'))
        self.refresh_stats()
