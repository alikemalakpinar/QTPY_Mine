"""Ekipman takip ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime

class EquipmentMapScreen(QWidget):
    """Ekipman harita ve takip ekranı"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.init_ui()
        
        # Güncellemeleri dinle
        self.tracking.location_updated.connect(self.refresh_data)
        self.i18n.language_changed.connect(self.update_texts)
        
        # Periyodik güncelleme
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_data)
        self.update_timer.start(3000)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # İstatistik kartları
        stats_layout = self.create_stats()
        layout.addLayout(stats_layout)
        
        # Ekipman tablosu
        self.create_table()
        layout.addWidget(self.table)
    
    def create_header(self):
        """Header oluştur"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('equipment_tracking'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        
        # Arama
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(self.i18n.t('search_equipment'))
        self.search_box.setMaximumWidth(300)
        self.search_box.textChanged.connect(self.filter_equipment)
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.search_box)
        
        return header
    
    def create_stats(self):
        """İstatistik kartları"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        stats = self.tracking.get_statistics()['equipment']
        
        self.stat_cards = []
        cards_data = [
            ('total_equipment', '🚜', str(stats['total']), MineTrackerTheme.PRIMARY),
            ('online', '✅', str(stats['online']), MineTrackerTheme.SUCCESS),
            ('maintenance', '🔧', str(stats['maintenance']), MineTrackerTheme.WARNING),
            ('critical_alerts', '⚠️', str(stats['low_battery']), MineTrackerTheme.DANGER)
        ]
        
        for title_key, icon, value, color in cards_data:
            card = self.create_stat_card(title_key, icon, value, color)
            self.stat_cards.append(card)
            layout.addWidget(card)
        
        return layout
    
    def create_stat_card(self, title_key, icon, value, color):
        """Tek bir istatistik kartı"""
        card = QWidget()
        card.setFixedHeight(100)
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=True))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(5)
        
        title = QLabel(f"{icon}  {self.i18n.t(title_key)}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 12px;
                text-transform: uppercase;
            }}
        """)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 32px;
                font-weight: 700;
            }}
        """)
        value_label.setProperty('value_label', True)
        value_label.setProperty('title_key', title_key)
        
        layout.addWidget(title)
        layout.addWidget(value_label)
        layout.addStretch()
        
        return card
    
    def create_table(self):
        """Ekipman tablosu"""
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            self.i18n.t('equipment_id'),
            self.i18n.t('name'),
            self.i18n.t('type'),
            self.i18n.t('operator'),
            self.i18n.t('zone'),
            self.i18n.t('status'),
            self.i18n.t('battery'),
            self.i18n.t('health_score'),
            self.i18n.t('actions')
        ])
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: {MineTrackerTheme.SURFACE};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 100)
        self.table.setColumnWidth(7, 120)
        
        self.table.verticalHeader().setVisible(False)
        
        self.populate_table()
    
    def populate_table(self):
        """Tabloyu doldur"""
        equipment = self.tracking.get_equipment()
        self.table.setRowCount(len(equipment))
        
        for row, equip in enumerate(equipment):
            # ID
            id_item = QTableWidgetItem(equip['id'])
            id_item.setForeground(QBrush(QColor(MineTrackerTheme.PRIMARY)))
            self.table.setItem(row, 0, id_item)
            
            # İsim
            self.table.setItem(row, 1, QTableWidgetItem(equip['name']))
            
            # Tip
            self.table.setItem(row, 2, QTableWidgetItem(equip['type']))
            
            # Operatör
            self.table.setItem(row, 3, QTableWidgetItem(equip['operator']))
            
            # Bölge
            zone_item = QTableWidgetItem(equip['zone_name'])
            zone_item.setForeground(QBrush(QColor(MineTrackerTheme.SUCCESS)))
            self.table.setItem(row, 4, zone_item)
            
            # Durum
            status_map = {
                'online': ('✅ ' + self.i18n.t('online'), MineTrackerTheme.SUCCESS),
                'maintenance': ('🔧 ' + self.i18n.t('maintenance'), MineTrackerTheme.WARNING),
                'offline': ('❌ ' + self.i18n.t('offline'), MineTrackerTheme.DANGER)
            }
            status_text, status_color = status_map.get(equip['status'], (equip['status'], MineTrackerTheme.TEXT_PRIMARY))
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(QBrush(QColor(status_color)))
            self.table.setItem(row, 5, status_item)
            
            # Batarya
            battery_item = QTableWidgetItem(f"{equip['battery']}%")
            if equip['battery'] < 20:
                battery_item.setForeground(QBrush(QColor(MineTrackerTheme.DANGER)))
            elif equip['battery'] < 50:
                battery_item.setForeground(QBrush(QColor(MineTrackerTheme.WARNING)))
            else:
                battery_item.setForeground(QBrush(QColor(MineTrackerTheme.SUCCESS)))
            self.table.setItem(row, 6, battery_item)
            
            # Sağlık skoru
            health_item = QTableWidgetItem(f"{equip['health_score']}%")
            if equip['health_score'] < 50:
                health_item.setForeground(QBrush(QColor(MineTrackerTheme.DANGER)))
            elif equip['health_score'] < 75:
                health_item.setForeground(QBrush(QColor(MineTrackerTheme.WARNING)))
            else:
                health_item.setForeground(QBrush(QColor(MineTrackerTheme.SUCCESS)))
            self.table.setItem(row, 7, health_item)
            
            # Aksiyonlar
            actions_widget = self.create_actions_widget(equip)
            self.table.setCellWidget(row, 8, actions_widget)
            
            self.table.setRowHeight(row, 55)
    
    def create_actions_widget(self, equip):
        """Aksiyon butonları"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Yerini bul
        locate_btn = QPushButton('📍')
        locate_btn.setFixedSize(35, 35)
        locate_btn.setToolTip(self.i18n.t('locate'))
        locate_btn.setStyleSheet(f"""
            QPushButton {{
                background: {MineTrackerTheme.PRIMARY};
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {MineTrackerTheme.PRIMARY_LIGHT};
            }}
        """)
        
        # Detaylar
        details_btn = QPushButton('📊')
        details_btn.setFixedSize(35, 35)
        details_btn.setToolTip('Details')
        details_btn.setStyleSheet(f"""
            QPushButton {{
                background: {MineTrackerTheme.INFO};
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: #8B7AE7;
            }}
        """)
        
        layout.addWidget(locate_btn)
        layout.addWidget(details_btn)
        layout.addStretch()
        
        return widget
    
    def filter_equipment(self, text):
        """Ekipman filtrele"""
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount() - 1):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
    
    def refresh_data(self):
        """Verileri yenile"""
        self.populate_table()
        
        # İstatistikleri güncelle
        stats = self.tracking.get_statistics()['equipment']
        for card in self.stat_cards:
            for label in card.findChildren(QLabel):
                if label.property('value_label'):
                    title_key = label.property('title_key')
                    if title_key == 'total_equipment':
                        label.setText(str(stats['total']))
                    elif title_key == 'online':
                        label.setText(str(stats['online']))
                    elif title_key == 'maintenance':
                        label.setText(str(stats['maintenance']))
                    elif title_key == 'critical_alerts':
                        label.setText(str(stats['low_battery']))
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('equipment_tracking'))
        self.search_box.setPlaceholderText(self.i18n.t('search_equipment'))
        self.table.setHorizontalHeaderLabels([
            self.i18n.t('equipment_id'),
            self.i18n.t('name'),
            self.i18n.t('type'),
            self.i18n.t('operator'),
            self.i18n.t('zone'),
            self.i18n.t('status'),
            self.i18n.t('battery'),
            self.i18n.t('health_score'),
            self.i18n.t('actions')
        ])
        self.refresh_data()
