"""Canlı 3D harita ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from theme.theme import AicoMadenTakipTheme
from components.model3d.mine_3d_view import Mine3DView

class LiveMapScreen(QWidget):
    """Canlı 3D maden haritası"""
    
    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.init_ui()
        
        # Dil değişikliğini dinle
        self.i18n.language_changed.connect(self.update_texts)
    
    def init_ui(self):
        """UI'yi başlat"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # 3D Harita
        self.map_3d = Mine3DView(self.tracking)
        layout.addWidget(self.map_3d, 1)
    
    def create_header(self):
        """Header oluştur"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('live_mine_map'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {AicoMadenTakipTheme.TEXT_PRIMARY};
            }}
        """)
        
        # Kontroller
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Tam ekran butonu
        fullscreen_btn = QPushButton('🔲 ' + self.i18n.t('fullscreen'))
        fullscreen_btn.setStyleSheet(AicoMadenTakipTheme.get_button_style('primary'))
        fullscreen_btn.setFixedHeight(40)
        fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        
        controls_layout.addWidget(fullscreen_btn)
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addLayout(controls_layout)
        
        return header
    
    def toggle_fullscreen(self):
        """Tam ekran değiştir"""
        if self.window().isFullScreen():
            self.window().showNormal()
        else:
            self.window().showFullScreen()
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('live_mine_map'))
