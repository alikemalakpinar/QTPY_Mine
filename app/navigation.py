"""Modern navigasyon sidebar"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme

class NavigationBar(QWidget):
    """Sol navigasyon sidebar"""
    
    page_changed = pyqtSignal(int)
    emergency_triggered = pyqtSignal()
    
    def __init__(self, i18n):
        super().__init__()
        self.i18n = i18n
        self.current_page = 0
        self.nav_buttons = []
        self.init_ui()
        
        # Dil değiştiğinde güncelle
        self.i18n.language_changed.connect(self.update_texts)
    
    def init_ui(self):
        """UI'yi başlat"""
        self.setFixedWidth(260)
        self.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-right: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo/Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Navigation items
        self.nav_items = [
            ('🎯', 'dashboard', 0),
            ('🗺️', 'live_map', 1),
            ('👥', 'personnel', 2),
            ('🚨', 'emergency', 3),
            ('📋', 'reports', 4),
            ('📍', 'zones', 5),
            ('⚙️', 'settings', 6)
        ]
        
        for icon, key, index in self.nav_items:
            btn = self.create_nav_button(icon, key, index)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Emergency button
        emergency_btn = self.create_emergency_button()
        layout.addWidget(emergency_btn)
        
        # Select first page
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
    
    def create_header(self):
        """Header oluştur"""
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE_LIGHT};
                border-bottom: 1px solid {MineTrackerTheme.BORDER};
                border-right: none;
            }}
        """)
        
        layout = QVBoxLayout(header)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        
        # Logo
        logo = QLabel("⛏️ MineTracker")
        logo.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: 700;
                color: {MineTrackerTheme.PRIMARY};
            }}
        """)
        
        # Subtitle
        self.subtitle = QLabel(self.i18n.t('app_subtitle'))
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
            }}
        """)
        self.subtitle.setWordWrap(True)
        
        layout.addWidget(logo)
        layout.addWidget(self.subtitle)
        
        return header
    
    def create_nav_button(self, icon, text_key, index):
        """Navigasyon butonu oluştur"""
        btn = QPushButton(f"{icon}  {self.i18n.t(text_key)}")
        btn.setCheckable(True)
        btn.setFixedHeight(55)
        btn.setProperty('text_key', text_key)
        btn.setProperty('icon', icon)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-left: 3px solid transparent;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 15px;
                font-weight: 500;
                text-align: left;
                padding-left: 25px;
            }}
            QPushButton:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
            QPushButton:checked {{
                background: {MineTrackerTheme.SURFACE_HOVER};
                border-left-color: {MineTrackerTheme.PRIMARY};
                color: {MineTrackerTheme.PRIMARY};
                font-weight: 600;
            }}
        """)
        
        btn.clicked.connect(lambda: self.select_page(index))
        return btn
    
    def create_emergency_button(self):
        """Acil durum butonu oluştur"""
        self.emergency_btn = QPushButton(self.i18n.t('emergency_button'))
        self.emergency_btn.setFixedHeight(60)
        self.emergency_btn.setStyleSheet(f"""
            QPushButton {{
                background: {MineTrackerTheme.DANGER};
                border: none;
                color: white;
                font-size: 16px;
                font-weight: 700;
                margin: 20px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background: #FF5577;
            }}
            QPushButton:pressed {{
                background: #DD2244;
            }}
        """)
        self.emergency_btn.clicked.connect(self.emergency_triggered.emit)
        return self.emergency_btn
    
    def select_page(self, index):
        """Sayfa seç"""
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        self.current_page = index
        self.page_changed.emit(index)
    
    def update_texts(self):
        """Metinleri güncelle (dil değişince)"""
        self.subtitle.setText(self.i18n.t('app_subtitle'))
        self.emergency_btn.setText(self.i18n.t('emergency_button'))
        
        for btn in self.nav_buttons:
            text_key = btn.property('text_key')
            icon = btn.property('icon')
            if text_key and icon:
                btn.setText(f"{icon}  {self.i18n.t(text_key)}")
