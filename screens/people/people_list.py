from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime
from screens.people.person_detail import PersonDetailScreen

class PeopleListScreen(QWidget):
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.detail_screen = None
        self.init_ui()
        
        self.tracking.location_updated.connect(self.refresh_table)
        self.i18n.language_changed.connect(self.update_texts)
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_table)
        self.update_timer.start(3000)
    
    def init_ui(self):
        self.main_layout = QStackedLayout(self)
        
        self.list_widget = QWidget()
        list_layout = QVBoxLayout(self.list_widget)
        list_layout.setSpacing(20)
        list_layout.setContentsMargins(30, 30, 30, 30)
        
        header = self.create_header()
        list_layout.addWidget(header)
        
        stats_layout = self.create_stats()
        list_layout.addLayout(stats_layout)
        
        self.create_table()
        list_layout.addWidget(self.table)
        
        self.main_layout.addWidget(self.list_widget)
    
    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('personnel_tracking'))
        self.title.setStyleSheet(f"font-size: 28px; font-weight: 800; color: {MineTrackerTheme.TEXT_PRIMARY}; letter-spacing: -1px;")
        
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
        card = QWidget()
        card.setFixedHeight(110)
        card.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
                border-left: 3px solid {color};
            }}
            QWidget:hover {{
                border-color: {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(4)

        title = QLabel(f"{icon}  {self.i18n.t(title_key).upper()}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
        """)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 36px;
                font-weight: 300;
                letter-spacing: -1px;
            }}
        """)
        value_label.setProperty('value_label', True)
        value_label.setProperty('title_key', title_key)

        layout.addWidget(title)
        layout.addWidget(value_label)
        layout.addStretch()

        return card
    
    def create_table(self):
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
        
        self.table.setStyleSheet(f"QTableWidget {{ background: {MineTrackerTheme.SURFACE}; border: none; border-radius: 16px; }}")
        
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        
        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
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
        
        detail_btn = QPushButton('👁️')
        detail_btn.setFixedSize(35, 35)
        detail_btn.setToolTip('Detayları Gör')
        detail_btn.setStyleSheet(f"""
            QPushButton {{
                background: {MineTrackerTheme.SUCCESS};
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: #33FF99;
            }}
        """)
        detail_btn.clicked.connect(lambda: self.show_person_detail(person['id']))
        
        layout.addWidget(locate_btn)
        layout.addWidget(detail_btn)
        layout.addWidget(sos_btn)
        layout.addStretch()
        
        return widget
    
    def on_row_double_clicked(self, row, column):
        person_id_item = self.table.item(row, 0)
        if person_id_item:
            person_id = person_id_item.text()
            self.show_person_detail(person_id)
    
    def show_person_detail(self, person_id):
        self.detail_screen = PersonDetailScreen(self.i18n, self.tracking, self.store, person_id)
        self.detail_screen.back_requested.connect(self.show_list)
        self.main_layout.addWidget(self.detail_screen)
        self.main_layout.setCurrentWidget(self.detail_screen)
    
    def show_list(self):
        self.main_layout.setCurrentWidget(self.list_widget)
        if self.detail_screen:
            self.main_layout.removeWidget(self.detail_screen)
            self.detail_screen.deleteLater()
            self.detail_screen = None
    
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
