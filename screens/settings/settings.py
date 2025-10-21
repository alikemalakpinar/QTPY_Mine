"""Ayarlar ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from theme.theme import MineTrackerTheme

class SettingsScreen(QWidget):
    """Uygulama ayarları"""
    
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
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Ayar bölümleri
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(20)
        
        # Sol: Genel ayarlar
        general_section = self.create_general_settings()
        settings_layout.addWidget(general_section)
        
        # Sağ: Sistem durumu
        system_section = self.create_system_status()
        settings_layout.addWidget(system_section)
        
        layout.addLayout(settings_layout)
        layout.addStretch()
    
    def create_header(self):
        """Header"""
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('general_settings'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        
        subtitle = QLabel('Uygulama tercihleri ve sistem yapılandırması')
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
            }}
        """)
        
        layout.addWidget(self.title)
        layout.addWidget(subtitle)
        
        return header
    
    def create_general_settings(self):
        """Genel ayarlar"""
        section = QWidget()
        section.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Dil seçimi
        self.create_language_setting(layout)
        
        # Bildirimler
        self.create_notifications_setting(layout)
        
        # Tema (gelecek için placeholder)
        self.create_theme_setting(layout)
        
        layout.addStretch()
        
        # Kaydet butonu
        save_btn = QPushButton('💾 ' + self.i18n.t('save'))
        save_btn.setFixedHeight(45)
        save_btn.setStyleSheet(MineTrackerTheme.get_button_style('success'))
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        return section
    
    def create_language_setting(self, parent_layout):
        """Dil ayarı"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        
        self.language_label = QLabel('🌍 ' + self.i18n.t('language'))
        self.language_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        
        # Dil combo box
        self.language_combo = QComboBox()
        languages = self.i18n.get_available_languages()
        for lang in languages:
            self.language_combo.addItem(f"{lang['flag']} {lang['name']}", lang['code'])
        
        # Mevcut dili seç
        current_lang = self.i18n.get_current_language()
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
        
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        
        parent_layout.addWidget(container)
    
    def create_notifications_setting(self, parent_layout):
        """Bildirim ayarları"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        
        self.notifications_label = QLabel('🔔 ' + self.i18n.t('notifications'))
        self.notifications_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        
        # Sesli uyarılar
        self.sound_checkbox = QCheckBox(self.i18n.t('sound_alerts'))
        self.sound_checkbox.setChecked(True)
        self.sound_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 14px;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {MineTrackerTheme.BORDER};
                border-radius: 4px;
                background: {MineTrackerTheme.SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background: {MineTrackerTheme.PRIMARY};
                border-color: {MineTrackerTheme.PRIMARY};
            }}
        """)
        
        # Görsel uyarılar
        self.visual_checkbox = QCheckBox(self.i18n.t('visual_alerts'))
        self.visual_checkbox.setChecked(True)
        self.visual_checkbox.setStyleSheet(self.sound_checkbox.styleSheet())
        
        layout.addWidget(self.notifications_label)
        layout.addWidget(self.sound_checkbox)
        layout.addWidget(self.visual_checkbox)
        
        parent_layout.addWidget(container)
    
    def create_theme_setting(self, parent_layout):
        """Tema ayarı"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        
        self.theme_label = QLabel('🎨 ' + self.i18n.t('theme'))
        self.theme_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        
        # Tema combo box
        self.theme_combo = QComboBox()
        self.theme_combo.addItem('🌙 ' + self.i18n.t('dark_theme'), 'dark')
        self.theme_combo.addItem('☀️ ' + self.i18n.t('light_theme'), 'light')
        self.theme_combo.setEnabled(False)  # Şimdilik sadece koyu tema
        
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)
        
        parent_layout.addWidget(container)
    
    def create_system_status(self):
        """Sistem durumu"""
        section = QWidget()
        section.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        title = QLabel('📊 ' + self.i18n.t('system_status'))
        title.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 600;
            }}
        """)
        layout.addWidget(title)
        
        # Durum bilgileri
        status_items = [
            ('✅ Takip Servisi', self.i18n.t('connected')),
            ('✅ Veritabanı', self.i18n.t('connected')),
            ('✅ 3D Görselleştirme', 'Aktif'),
            ('📈 Personel Takibi', f"{len(self.tracking.get_personnel())} Aktif"),
            ('🚜 Ekipman Takibi', f"{len(self.tracking.get_equipment())} Aktif"),
        ]
        
        for label, value in status_items:
            item = self.create_status_item(label, value)
            layout.addWidget(item)
        
        layout.addStretch()
        
        # Versi on bilgisi
        version_label = QLabel(f"{self.i18n.t('version')}: 1.0.0")
        version_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 11px;
                text-align: center;
            }}
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        return section
    
    def create_status_item(self, label, value):
        """Durum itemı"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 10, 12, 10)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 13px;
            }}
        """)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.SUCCESS};
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        
        layout.addWidget(label_widget)
        layout.addStretch()
        layout.addWidget(value_widget)
        
        return widget
    
    def on_language_changed(self, index):
        """Dil değiştiğinde"""
        lang_code = self.language_combo.itemData(index)
        if lang_code:
            self.i18n.set_language(lang_code)
    
    def save_settings(self):
        """Ayarları kaydet"""
        QMessageBox.information(
            self,
            self.i18n.t('success'),
            'Ayarlar kaydedildi!' if self.i18n.current_language == 'tr' 
            else 'Settings saved successfully!'
        )
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('general_settings'))
        self.language_label.setText('🌍 ' + self.i18n.t('language'))
        self.notifications_label.setText('🔔 ' + self.i18n.t('notifications'))
        self.sound_checkbox.setText(self.i18n.t('sound_alerts'))
        self.visual_checkbox.setText(self.i18n.t('visual_alerts'))
        self.theme_label.setText('🎨 ' + self.i18n.t('theme'))
