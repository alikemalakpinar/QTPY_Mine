"""Raporlar ekranı"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QFont
from theme.theme import MineTrackerTheme
from datetime import datetime

class ReportsScreen(QWidget):
    """Raporlar ve analizler ekranı"""
    
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
        
        # Rapor tipleri
        reports_grid = QGridLayout()
        reports_grid.setSpacing(20)
        
        report_types = [
            ('📋', 'Vardiya Raporu', 'Günlük vardiya detayları', 'primary'),
            ('📈', 'Performans Raporu', 'Ekipman ve personel performansı', 'success'),
            ('⚠️', 'Olay Raporu', 'Güvenlik olayları analizi', 'warning'),
            ('🔋', 'Batarya Raporu', 'Cihaz batarya durumları', 'danger'),
            ('📍', 'Konum Raporu', 'Bölge bazlı aktivite', 'info'),
            ('📄', 'Özet Rapor', 'Genel durum özeti', 'primary')
        ]
        
        for i, (icon, title, desc, variant) in enumerate(report_types):
            card = self.create_report_card(icon, title, desc, variant)
            reports_grid.addWidget(card, i // 3, i % 3)
        
        layout.addLayout(reports_grid)
        
        # Hızlı istatistikler
        stats_section = self.create_stats_section()
        layout.addWidget(stats_section)
        
        layout.addStretch()
    
    def create_header(self):
        """Header"""
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.title = QLabel(self.i18n.t('reports'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        
        subtitle = QLabel(f"{datetime.now().strftime('%d %B %Y')} - Raporlar ve İstatistikler")
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
            }}
        """)
        
        layout.addWidget(self.title)
        layout.addWidget(subtitle)
        
        return header
    
    def create_report_card(self, icon, title, description, variant):
        """Rapor kartı"""
        card = QWidget()
        card.setFixedHeight(150)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=True))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Arial', 32))
        
        # Başlık
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        
        # Açıklama
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """)
        desc_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        return card
    
    def create_stats_section(self):
        """Hızlı istatistikler"""
        section = QWidget()
        section.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel('📊 Günlük Özet İstatistikler')
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)
        
        # İstatistik grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        stats = self.tracking.get_statistics()
        
        stats_data = [
            ('Toplam Personel', str(stats['personnel']['total']), MineTrackerTheme.PRIMARY),
            ('Aktif Personel', str(stats['personnel']['active']), MineTrackerTheme.SUCCESS),
            ('Molada', str(stats['personnel']['on_break']), MineTrackerTheme.WARNING),
            ('Gateway Online', str(stats['gateways']['online']), MineTrackerTheme.SUCCESS),
            ('Gateway Offline', str(stats['gateways']['offline']), MineTrackerTheme.DANGER),
            ('Düşük Batarya', str(stats['personnel']['low_battery']), MineTrackerTheme.DANGER)
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            stat_widget = self.create_stat_item(label, value, color)
            stats_grid.addWidget(stat_widget, i // 3, i % 3)
        
        layout.addLayout(stats_grid)
        
        return section
    
    def create_stat_item(self, label, value, color):
        """İstatistik item"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 24px;
                font-weight: 700;
            }}
        """)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 11px;
            }}
        """)
        
        layout.addWidget(value_label)
        layout.addWidget(label_widget)
        
        return widget
    
    def update_texts(self):
        """Metinleri güncelle"""
        self.title.setText(self.i18n.t('reports'))
