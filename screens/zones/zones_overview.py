"""Bölgeler ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import AicoTheme

class ZonesScreen(QWidget):
    """Maden bölgeleri yönetimi"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.init_ui()
        
        self.i18n.language_changed.connect(self.update_texts)
        
        # Periyodik güncelleme
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_zones)
        self.update_timer.start(5000)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Bölge kartları
        zones_grid = QGridLayout()
        zones_grid.setSpacing(20)
        
        zones = self.tracking.get_zones()
        for i, zone in enumerate(zones):
            card = self.create_zone_card(zone)
            zones_grid.addWidget(card, i // 3, i % 3)
        
        layout.addLayout(zones_grid)
        
        # Bölge istatistikleri
        stats_section = self.create_stats_section()
        layout.addWidget(stats_section)
    
    def create_header(self):
        """Header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('zones'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {AicoTheme.TEXT_PRIMARY};
            }}
        """)
        
        layout.addWidget(self.title)
        layout.addStretch()
        
        return header
    
    def create_zone_card(self, zone):
        """Bölge kartı"""
        card = QWidget()
        card.setFixedHeight(180)
        card.setStyleSheet(AicoTheme.get_card_style(hover=True))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Başlık ve renk
        header_layout = QHBoxLayout()
        
        color_indicator = QLabel('●')
        color_indicator.setStyleSheet(f"color: {zone['color']}; font-size: 32px;")
        
        zone_name = QLabel(zone['name'])
        zone_name.setStyleSheet(f"""
            QLabel {{
                color: {AicoTheme.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 600;
            }}
        """)
        
        header_layout.addWidget(color_indicator)
        header_layout.addWidget(zone_name)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # İstatistikler
        personnel_count = sum(1 for p in self.tracking.get_personnel() if p['zone_id'] == zone['id'])
        
        # Personel
        personnel_layout = QHBoxLayout()
        personnel_icon = QLabel('👥')
        personnel_icon.setFont(QFont('Arial', 16))
        personnel_label = QLabel(f"{personnel_count} Personel")
        personnel_label.setStyleSheet(f"color: {AicoTheme.TEXT_SECONDARY}; font-size: 13px;")
        personnel_layout.addWidget(personnel_icon)
        personnel_layout.addWidget(personnel_label)
        personnel_layout.addStretch()
        
        # Gateway
        gateway_layout = QHBoxLayout()
        gateway_icon = QLabel('📡')
        gateway_icon.setFont(QFont('Arial', 16))
        gateway_label = QLabel(f"Gateway Active")
        gateway_label.setStyleSheet(f"color: {AicoTheme.TEXT_SECONDARY}; font-size: 13px;")
        gateway_layout.addWidget(gateway_icon)
        gateway_layout.addWidget(gateway_label)
        gateway_layout.addStretch()
        
        layout.addLayout(personnel_layout)
        layout.addLayout(gateway_layout)
        
        # Koordinatlar
        coords_label = QLabel(f"X: {zone['x']}, Y: {zone['y']}")
        coords_label.setStyleSheet(f"""
            QLabel {{
                color: {AicoTheme.TEXT_MUTED};
                font-size: 11px;
                font-family: 'Courier New', monospace;
            }}
        """)
        layout.addWidget(coords_label)
        
        layout.addStretch()
        
        # Detay butonu
        details_btn = QPushButton('📊 Detaylar')
        details_btn.setFixedHeight(35)
        details_btn.setStyleSheet(f"""
            QPushButton {{
                background: {AicoTheme.PRIMARY};
                color: #000000;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {AicoTheme.PRIMARY_LIGHT};
            }}
        """)
        layout.addWidget(details_btn)
        
        return card
    
    def create_stats_section(self):
        """İstatistikler bölümü"""
        section = QWidget()
        section.setStyleSheet(AicoTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel('📊 Bölge Bazlı İstatistikler')
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {AicoTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)
        
        # Bölge detay tablosu
        self.zones_table = QTableWidget()
        self.zones_table.setColumnCount(3)
        self.zones_table.setHorizontalHeaderLabels(['Bölge', 'Personel', 'Durum'])
        
        self.zones_table.setStyleSheet(f"""
            QTableWidget {{
                background: {AicoTheme.BACKGROUND};
                border: none;
                border-radius: 8px;
            }}
        """)
        
        self.zones_table.horizontalHeader().setStretchLastSection(True)
        self.zones_table.verticalHeader().setVisible(False)
        self.zones_table.setMaximumHeight(300)
        
        self.populate_zones_table()
        
        layout.addWidget(self.zones_table)
        
        return section
    
    def populate_zones_table(self):
        """Bölge tablosunu doldur"""
        zones = self.tracking.get_zones()
        self.zones_table.setRowCount(len(zones))
        
        for row, zone in enumerate(zones):
            # Bölge adı
            zone_item = QTableWidgetItem(f"● {zone['name']}")
            zone_item.setForeground(QBrush(QColor(zone['color'])))
            self.zones_table.setItem(row, 0, zone_item)
            
            # Personel sayısı
            personnel_count = sum(1 for p in self.tracking.get_personnel() if p['zone_id'] == zone['id'])
            self.zones_table.setItem(row, 1, QTableWidgetItem(str(personnel_count)))
            
            # Durum
            status = '✅ Aktif' if personnel_count > 0 else '⚫ İnaktif'
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QBrush(QColor(
                AicoTheme.SUCCESS if personnel_count > 0 
                else AicoTheme.TEXT_MUTED
            )))
            self.zones_table.setItem(row, 2, status_item)
            
            self.zones_table.setRowHeight(row, 45)
    
    def refresh_zones(self):
        """Bölgeleri yenile"""
        self.populate_zones_table()
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('zones'))
