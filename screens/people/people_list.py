"""Personel takip ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime

class PeopleListScreen(QWidget):
    """Personel listesi ve takibi"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.init_ui()
        
        # Güncellemeleri dinle
        self.tracking.location_updated.connect(self.refresh_table)
        self.i18n.language_changed.connect(self.update_texts)
        
        # Periyodik güncelleme
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_table)
        self.update_timer.start(3000)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header ve arama
        header = self.create_header()
        layout.addWidget(header)
        
        # İstatistik kartları
        stats_layout = self.create_stats()
        layout.addLayout(stats_layout)
        
        # Personel tablosu
        self.create_table()
        layout.addWidget(self.table)
    
    def create_header(self):
        """Header oluştur"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('personnel_tracking'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        
        # Arama kutusu
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(self.i18n.t('search_personnel'))
        self.search_box.setMaximumWidth(300)
        self.search_box.textChanged.connect(self.filter_personnel)
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.search_box)
        
        return header
    
    def create_stats(self):
        """İstatistik kartları"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        stats = self.tracking.get_statistics()['personnel']
        
        self.stat_cards = []
        cards_data = [
            ('total_underground', '👥', str(stats['total']), MineTrackerTheme.PRIMARY),
            ('active_now', '✅', str(stats['active']), MineTrackerTheme.SUCCESS),
            ('on_break', '⌛', str(stats['on_break']), MineTrackerTheme.WARNING),
            ('critical_alerts', '🚨', str(stats['low_battery']), MineTrackerTheme.DANGER)
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
        
        # Başlık
        title = QLabel(f"{icon}  {self.i18n.t(title_key)}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 12px;
                text-transform: uppercase;
            }}
        """)
        
        # Değer
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
        """Personel tablosu oluştur"""
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            self.i18n.t('person_id'),
            self.i18n.t('name'),
            self.i18n.t('position'),
            self.i18n.t('zone'),
            self.i18n.t('status'),
            self.i18n.t('heart_rate'),
            self.i18n.t('battery'),
            self.i18n.t('last_update'),
            self.i18n.t('actions')
        ])
        
        # Tablo stili
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: {MineTrackerTheme.SURFACE};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        # Kolon genişlikleri
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 100)
        self.table.setColumnWidth(7, 120)
        
        # Satır numaralarını gizle
        self.table.verticalHeader().setVisible(False)
        
        # Tabloyu doldur
        self.populate_table()
    
    def populate_table(self):
        """Tabloyu doldur"""
        personnel = self.tracking.get_personnel()
        self.table.setRowCount(len(personnel))
        
        for row, person in enumerate(personnel):
            # ID
            id_item = QTableWidgetItem(person['id'])
            id_item.setForeground(QBrush(QColor(MineTrackerTheme.PRIMARY)))
            self.table.setItem(row, 0, id_item)
            
            # İsim
            name_item = QTableWidgetItem(person['full_name'])
            self.table.setItem(row, 1, name_item)
            
            # Pozisyon
            self.table.setItem(row, 2, QTableWidgetItem(person['position']))
            
            # Bölge
            zone_item = QTableWidgetItem(person['zone_name'])
            zone_item.setForeground(QBrush(QColor(MineTrackerTheme.SUCCESS)))
            self.table.setItem(row, 3, zone_item)
            
            # Durum
            status_text = {
                'active': '✅ ' + self.i18n.t('active'),
                'break': '⌛ ' + self.i18n.t('break'),
                'emergency': '🚨 ' + self.i18n.t('emergency')
            }.get(person['status'], person['status'])
            
            status_item = QTableWidgetItem(status_text)
            status_color = {
                'active': MineTrackerTheme.SUCCESS,
                'break': MineTrackerTheme.WARNING,
                'emergency': MineTrackerTheme.DANGER
            }.get(person['status'], MineTrackerTheme.TEXT_PRIMARY)
            status_item.setForeground(QBrush(QColor(status_color)))
            self.table.setItem(row, 4, status_item)
            
            # Kalp atışı
            hr_item = QTableWidgetItem(f"{person['heart_rate']} bpm")
            if person['heart_rate'] > 100:
                hr_item.setForeground(QBrush(QColor(MineTrackerTheme.DANGER)))
            elif person['heart_rate'] > 90:
                hr_item.setForeground(QBrush(QColor(MineTrackerTheme.WARNING)))
            self.table.setItem(row, 5, hr_item)
            
            # Batarya
            battery_item = QTableWidgetItem(f"{person['battery']}%")
            if person['battery'] < 20:
                battery_item.setForeground(QBrush(QColor(MineTrackerTheme.DANGER)))
            elif person['battery'] < 50:
                battery_item.setForeground(QBrush(QColor(MineTrackerTheme.WARNING)))
            else:
                battery_item.setForeground(QBrush(QColor(MineTrackerTheme.SUCCESS)))
            self.table.setItem(row, 6, battery_item)
            
            # Son güncelleme
            time_diff = datetime.now() - person['last_update']
            seconds = time_diff.total_seconds()
            if seconds < 60:
                time_text = self.i18n.t('just_now')
            elif seconds < 3600:
                time_text = f"{int(seconds/60)} {self.i18n.t('min_ago')}"
            else:
                time_text = f"{int(seconds/3600)} {self.i18n.t('hour_ago')}"
            self.table.setItem(row, 7, QTableWidgetItem(time_text))
            
            # Aksiyonlar
            actions_widget = self.create_actions_widget(person)
            self.table.setCellWidget(row, 8, actions_widget)
            
            # Satır yüksekliği
            self.table.setRowHeight(row, 55)
    
    def create_actions_widget(self, person):
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
        
        # Acil durum
        sos_btn = QPushButton('🚨')
        sos_btn.setFixedSize(35, 35)
        sos_btn.setToolTip('SOS')
        sos_btn.setStyleSheet(f"""
            QPushButton {{
                background: {MineTrackerTheme.DANGER};
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: #FF5577;
            }}
        """)
        sos_btn.clicked.connect(lambda: self.tracking.trigger_emergency(person['id'], 'personnel'))
        
        layout.addWidget(locate_btn)
        layout.addWidget(sos_btn)
        layout.addStretch()
        
        return widget
    
    def filter_personnel(self, text):
        """Personel filtrele"""
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount() - 1):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
    
    def refresh_table(self):
        """Tabloyu yenile"""
        self.populate_table()
        
        # İstatistikleri güncelle
        stats = self.tracking.get_statistics()['personnel']
        for card in self.stat_cards:
            for label in card.findChildren(QLabel):
                if label.property('value_label'):
                    title_key = label.property('title_key')
                    if title_key == 'total_underground':
                        label.setText(str(stats['total']))
                    elif title_key == 'active_now':
                        label.setText(str(stats['active']))
                    elif title_key == 'on_break':
                        label.setText(str(stats['on_break']))
                    elif title_key == 'critical_alerts':
                        label.setText(str(stats['low_battery']))
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('personnel_tracking'))
        self.search_box.setPlaceholderText(self.i18n.t('search_personnel'))
        # Tablo başlıklarını güncelle
        self.table.setHorizontalHeaderLabels([
            self.i18n.t('person_id'),
            self.i18n.t('name'),
            self.i18n.t('position'),
            self.i18n.t('zone'),
            self.i18n.t('status'),
            self.i18n.t('heart_rate'),
            self.i18n.t('battery'),
            self.i18n.t('last_update'),
            self.i18n.t('actions')
        ])
        self.refresh_table()
