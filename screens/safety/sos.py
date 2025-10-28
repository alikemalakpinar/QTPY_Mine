"""Acil durum merkezi ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import AicoMadenTakipTheme
from datetime import datetime

class EmergencyScreen(QWidget):
    """Acil durum yönetim merkezi"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.emergencies = []
        self.init_ui()
        
        # Acil durum sinyallerini dinle
        self.tracking.emergency_signal.connect(self.handle_emergency)
        self.i18n.language_changed.connect(self.update_texts)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # İstatistikler
        stats_layout = self.create_stats()
        layout.addLayout(stats_layout)
        
        # İçerik
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Sol: Aktif acil durumlar
        left_section = self.create_emergencies_section()
        content_layout.addWidget(left_section, 2)
        
        # Sağ: Acil durum kontakları ve protokol
        right_section = self.create_contacts_section()
        content_layout.addWidget(right_section, 1)
        
        layout.addLayout(content_layout, 1)
    
    def create_header(self):
        """Header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('emergency_center'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {AicoMadenTakipTheme.DANGER};
            }}
        """)
        
        # Test butonu
        test_btn = QPushButton('🚨 Test SOS')
        test_btn.setStyleSheet(AicoMadenTakipTheme.get_button_style('danger'))
        test_btn.setFixedHeight(45)
        test_btn.clicked.connect(self.test_emergency)
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(test_btn)
        
        return header
    
    def create_stats(self):
        """İstatistikler"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        self.stat_cards = []
        cards_data = [
            ('active_emergencies', '🚨', '0', AicoMadenTakipTheme.DANGER),
            ('response_time', '⏱️', '< 2 ' + self.i18n.t('min_ago'), AicoMadenTakipTheme.SUCCESS),
            ('evacuation_status', '🚻', self.i18n.t('all_clear'), AicoMadenTakipTheme.SUCCESS),
            ('emergency_contacts', '📞', '24/7', AicoMadenTakipTheme.PRIMARY)
        ]
        
        for title_key, icon, value, color in cards_data:
            card = self.create_stat_card(title_key, icon, value, color)
            self.stat_cards.append(card)
            layout.addWidget(card)
        
        return layout
    
    def create_stat_card(self, title_key, icon, value, color):
        """Stat kartı"""
        card = QWidget()
        card.setFixedHeight(110)
        card.setStyleSheet(AicoMadenTakipTheme.get_card_style(hover=True))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(5)
        
        title = QLabel(f"{icon}  {self.i18n.t(title_key)}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                font-size: 12px;
                text-transform: uppercase;
            }}
        """)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: 700;
            }}
        """)
        value_label.setProperty('title_key', title_key)
        
        layout.addWidget(title)
        layout.addWidget(value_label)
        layout.addStretch()
        
        return card
    
    def create_emergencies_section(self):
        """Acil durumlar bölümü"""
        section = QWidget()
        section.setStyleSheet(AicoMadenTakipTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.emergencies_title = QLabel('🚨 ' + self.i18n.t('active_emergencies'))
        self.emergencies_title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(self.emergencies_title)
        
        # Acil durum listesi
        self.emergency_list = QListWidget()
        self.emergency_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background: {AicoMadenTakipTheme.BACKGROUND};
                border-left: 4px solid {AicoMadenTakipTheme.DANGER};
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
            QListWidget::item:hover {{
                background: {AicoMadenTakipTheme.SURFACE_HOVER};
            }}
        """)
        
        if not self.emergencies:
            self.emergency_list.addItem(
                f"✅ {self.i18n.t('all_clear')} - Aktif acil durum yok" if self.i18n.current_language == 'tr' 
                else f"✅ {self.i18n.t('all_clear')} - No active emergencies"
            )
        
        layout.addWidget(self.emergency_list)
        
        return section
    
    def create_contacts_section(self):
        """Kontaklar bölümü"""
        section = QWidget()
        section.setStyleSheet(AicoMadenTakipTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel('📞 ' + self.i18n.t('emergency_contacts'))
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)
        
        # Kontaklar
        contacts = [
            ('🚑', 'Ambulans', '112'),
            ('🚒', 'İtfaiye', '110'),
            ('👮', 'Polis', '155'),
            ('🏭', 'Maden Güvenlik', '+90 555 123 4567'),
            ('👨‍⚕️', 'Saha Doktoru', '+90 555 987 6543')
        ]
        
        for icon, name, phone in contacts:
            contact_widget = self.create_contact_item(icon, name, phone)
            layout.addWidget(contact_widget)
        
        layout.addStretch()
        
        # Protokol bilgisi
        protocol_label = QLabel(
            f"""
            <b>📝 {self.i18n.t('emergency_protocol')}</b><br>
            <span style='font-size: 11px; color: {AicoMadenTakipTheme.TEXT_SECONDARY};'>
            1. Acil durum sinyali gönder<br>
            2. Güvenli bölgeye çekilin<br>
            3. Ekip liderini bilgilendirin<br>
            4. Talimatları bekleyin
            </span>
            """ if self.i18n.current_language == 'tr' else f"""
            <b>📝 {self.i18n.t('emergency_protocol')}</b><br>
            <span style='font-size: 11px; color: {AicoMadenTakipTheme.TEXT_SECONDARY};'>
            1. Send emergency signal<br>
            2. Move to safe zone<br>
            3. Inform team leader<br>
            4. Await instructions
            </span>
            """
        )
        protocol_label.setWordWrap(True)
        protocol_label.setStyleSheet(f"""
            QLabel {{
                background: {AicoMadenTakipTheme.BACKGROUND};
                border-radius: 8px;
                padding: 15px;
                border-left: 4px solid {AicoMadenTakipTheme.WARNING};
            }}
        """)
        layout.addWidget(protocol_label)
        
        return section
    
    def create_contact_item(self, icon, name, phone):
        """Kontak item"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {AicoMadenTakipTheme.BACKGROUND};
                border-radius: 8px;
                padding: 10px;
            }}
            QWidget:hover {{
                background: {AicoMadenTakipTheme.SURFACE_HOVER};
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Arial', 20))
        icon_label.setFixedWidth(30)
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 500;
            }}
        """)
        
        phone_label = QLabel(phone)
        phone_label.setStyleSheet(f"""
            QLabel {{
                color: {AicoMadenTakipTheme.PRIMARY};
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(phone_label)
        
        return widget
    
    def handle_emergency(self, data):
        """Acil durum ekle"""
        self.emergencies.append(data)
        
        # Listeyi güncelle
        self.emergency_list.clear()
        for emergency in self.emergencies:
            time_str = datetime.fromisoformat(emergency['timestamp']).strftime('%H:%M:%S')
            if emergency['type'] == 'personnel':
                text = f"🚨 {emergency['name']} - {emergency['zone']} [{time_str}]"
            else:
                text = f"⚠️ {emergency['name']} - {emergency['zone']} [{time_str}]"
            self.emergency_list.addItem(text)
        
        # Stat kartını güncelle
        for card in self.stat_cards:
            for label in card.findChildren(QLabel):
                if label.property('title_key') == 'active_emergencies':
                    label.setText(str(len(self.emergencies)))
                    label.setStyleSheet(f"""
                        QLabel {{
                            color: {AicoMadenTakipTheme.DANGER};
                            font-size: 28px;
                            font-weight: 700;
                        }}
                    """)
    
    def test_emergency(self):
        """Test acil durumu"""
        personnel = self.tracking.get_personnel()
        if personnel:
            import random
            test_person = random.choice(personnel)
            self.tracking.trigger_emergency(test_person['id'], 'personnel')
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('emergency_center'))
        self.emergencies_title.setText('🚨 ' + self.i18n.t('active_emergencies'))
