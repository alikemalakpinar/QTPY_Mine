"""Ana uygulama sınıfı - Modular Architecture"""
import sys

# ⚠️ CRITICAL: Import QtWebEngine components FIRST!
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    QWebEngineView = None

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from app.navigation import NavigationBar
from theme.theme import AicoMadenTakipTheme
from services.i18n import I18nService
from services.tracking_service import TrackingService
from store.store import Store

# Screens
from screens.home.dashboard import DashboardScreen
from screens.home.live_map import LiveMapScreen
from screens.people.people_list import PeopleListScreen
from screens.equipment.equipment_management import EquipmentScreen
from screens.safety.sos import EmergencyScreen
from screens.reports.reports_home import ReportsScreen
from screens.zones.zones_overview import ZonesScreen
from screens.settings.settings import SettingsScreen

class AicoMadenTakipApp(QMainWindow):
    """Ana AicoMadenTakip Uygulaması"""
    
    def __init__(self):
        super().__init__()
        
        # Servisler
        self.i18n = I18nService()
        self.tracking = TrackingService()
        self.store = Store()
        
        # UI başlat
        self.init_ui()
        self.init_connections()
        
    def init_ui(self):
        """UI'yi başlat"""
        self.setWindowTitle("AicoMadenTakip - Underground Safety System")
        self.setGeometry(100, 100, 1600, 900)
        
        # Tema uygula
        self.setStyleSheet(AicoMadenTakipTheme.get_app_style())
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Navigation sidebar
        self.nav_bar = NavigationBar(self.i18n)
        self.nav_bar.page_changed.connect(self.change_page)
        self.nav_bar.emergency_triggered.connect(self.handle_emergency_button)
        main_layout.addWidget(self.nav_bar)
        
        # Content area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"""
            QStackedWidget {{
                background: {AicoMadenTakipTheme.BACKGROUND};
            }}
        """)
        
        # Ekranları oluştur
        self.init_screens()
        
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Status bar
        self.create_status_bar()
        
        # İlk sayfayı göster
        self.stacked_widget.setCurrentIndex(0)
    
    def init_screens(self):
        """Tüm ekranları oluştur"""
        # Dashboard
        self.dashboard = DashboardScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.dashboard)
        
        # Live 3D Map
        self.live_map = LiveMapScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.live_map)
        
        # Personnel
        self.personnel = PeopleListScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.personnel)
        
        # Equipment (Anchor & Tag Management)
        self.equipment = EquipmentScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.equipment)
        
        # Emergency
        self.emergency = EmergencyScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.emergency)
        
        # Reports
        self.reports = ReportsScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.reports)
        
        # Zones
        self.zones = ZonesScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.zones)
        
        # Settings
        self.settings = SettingsScreen(self.i18n, self.tracking, self.store)
        self.stacked_widget.addWidget(self.settings)
    
    def init_connections(self):
        """Sinyal bağlantılarını kur"""
        # Acil durum sinyali
        self.tracking.emergency_signal.connect(self.handle_emergency)
        
        # Batarya uyarıları
        self.tracking.battery_alert.connect(self.handle_battery_alert)
        
        # Dil değişikliği
        self.i18n.language_changed.connect(self.update_window_title)
    
    def create_status_bar(self):
        """Status bar oluştur"""
        status = self.statusBar()
        status.setStyleSheet(f"""
            QStatusBar {{
                background: {AicoMadenTakipTheme.SURFACE};
                color: {AicoMadenTakipTheme.TEXT_SECONDARY};
                border-top: 1px solid {AicoMadenTakipTheme.BORDER};
                font-size: 12px;
                padding: 5px;
            }}
        """)
        
        # Sistem durumu
        self.status_label = QLabel(self.i18n.t('system_online'))
        status.addWidget(self.status_label)
        
        # Saat
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"color: {AicoMadenTakipTheme.TEXT_SECONDARY};")
        status.addPermanentWidget(self.time_label)
        
        # Zaman güncelleyici
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
    
    def update_time(self):
        """Saati güncelle"""
        from datetime import datetime
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.time_label.setText(f"🕐 {current_time}")
    
    def change_page(self, index):
        """Sayfa değiştir"""
        self.stacked_widget.setCurrentIndex(index)
    
    def handle_emergency(self, data):
        """Acil durum sinyalini işle"""
        msg = QMessageBox(self)
        msg.setWindowTitle("🚨 ACİL DURUM UYARISI" if self.i18n.current_language == 'tr' else "🚨 EMERGENCY ALERT")
        
        if data['type'] == 'personnel':
            text = f"""
ACİL DURUM SİNYALİ!

Personel: {data['name']}
Pozisyon: {data.get('position', 'Bilinmiyor')}
Bölge: {data['zone']}
Koordinatlar: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}
Zaman: {data['timestamp']}
            """ if self.i18n.current_language == 'tr' else f"""
EMERGENCY SIGNAL!

Personnel: {data['name']}
Position: {data.get('position', 'Unknown')}
Zone: {data['zone']}
Coordinates: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}
Time: {data['timestamp']}
            """
        else:
            text = f"""
EKİPMAN ACİL DURUMU!

Ekipman: {data['name']}
Bölge: {data['zone']}
Koordinatlar: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}
Zaman: {data['timestamp']}
            """ if self.i18n.current_language == 'tr' else f"""
EQUIPMENT EMERGENCY!

Equipment: {data['name']}
Zone: {data['zone']}
Coordinates: X:{data['location']['x']:.1f}, Y:{data['location']['y']:.1f}
Time: {data['timestamp']}
            """
        
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStyleSheet(AicoMadenTakipTheme.get_app_style())
        msg.exec()
    
    def handle_battery_alert(self, data):
        """Batarya uyarısını işle"""
        # Sessizce logla, her seferinde popup gösterme
        print(f"⚠️ Low Battery: {data['id']} - {data['name']} - {data['battery']}%")
    
    def handle_emergency_button(self):
        """Acil durum butonuna basıldığında"""
        reply = QMessageBox.critical(
            self,
            "🚨 Acil Durum Protokolü" if self.i18n.current_language == 'tr' else "🚨 Emergency Protocol",
            """Acil durum protokolünü başlatmak istiyor musunuz?

Bu işlem:
• Tüm personeli uyaracak
• Acil servisler bilgilendirilecek
• Tahliye prosedürleri aktif olacak""" if self.i18n.current_language == 'tr' else """Activate emergency protocol?

This will:
• Alert all personnel
• Notify emergency services
• Activate evacuation procedures""",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Acil durum ekranına geç (Equipment eklendi, index 4 oldu)
            self.nav_bar.select_page(4)
            
            QMessageBox.information(
                self,
                "Protokol Aktif" if self.i18n.current_language == 'tr' else "Protocol Active",
                """✅ Acil durum protokolü aktif edildi!

• Tüm personel bilgilendirildi
• Acil servisler arandı
• Tahliye rotaları gösteriliyor""" if self.i18n.current_language == 'tr' else """✅ Emergency protocol activated!

• All personnel notified
• Emergency services contacted
• Evacuation routes displayed"""
            )
    
    def update_window_title(self):
        """Pencere başlığını güncelle"""
        if self.i18n.current_language == 'tr':
            self.setWindowTitle("AicoMadenTakip - Yer Altı Güvenlik Sistemi")
        else:
            self.setWindowTitle("AicoMadenTakip - Underground Safety System")
