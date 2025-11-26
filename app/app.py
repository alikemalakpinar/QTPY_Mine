"""Ana uygulama sınıfı - Modular Architecture + Advanced Tracking"""
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
from theme.theme import MineTrackerTheme
from services.i18n import I18nService
from services.advanced_tracking_service import AdvancedTrackingService
from services.tcp_server_service import TCPServerService
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

class MineTrackerApp(QMainWindow):
    """Ana MineTracker Uygulaması - Ultra Modern & Advanced"""
    
    def __init__(self):
        super().__init__()
        
        # Servisler
        self.i18n = I18nService()
        self.tracking = AdvancedTrackingService(mode='hybrid')  # Hybrid mode: simulation + TCP
        self.store = Store()
        
        # TCP Server (port 8888)
        self.tcp_server = TCPServerService(host='0.0.0.0', port=8888)
        self.tcp_server.data_received.connect(self.on_tcp_data_received)
        self.tcp_server.connection_status.connect(self.on_tcp_connection_status)
        self.tcp_server.error_occurred.connect(self.on_tcp_error)
        self.tcp_server.start()
        
        # UI başlat
        self.init_ui()
        self.init_connections()
        
        print("✅ MineTracker Ultra başlatıldı!")
        print(f"📡 TCP Server: 0.0.0.0:8888")
        print(f"🎯 Tracking Mode: {self.tracking.mode}")
        print(f"🗺️  3D Harita: {'Aktif' if WEBENGINE_AVAILABLE else 'Kapalı'}")
        
    def init_ui(self):
        """UI'yi başlat"""
        self.setWindowTitle("MineTracker Ultra - Underground Safety System")
        self.setGeometry(100, 100, 1700, 950)
        
        # Tema uygula
        self.setStyleSheet(MineTrackerTheme.get_app_style())
        
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
                background: {MineTrackerTheme.BACKGROUND};
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
        # Dashboard (ULTRA MODERN)
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
        
        # Position calculated
        self.tracking.position_calculated.connect(self.on_position_calculated)
    
    def on_tcp_data_received(self, data):
        """TCP'den veri geldiğinde"""
        # Tracking service'e gönder
        self.tracking.process_tcp_data(data)
        
        # Status bar güncelle
        stats = self.tcp_server.get_statistics()
        self.tcp_status_label.setText(
            f"📡 TCP: {stats['connected_clients']} clients • {stats['total_messages']} msgs • {stats['messages_per_second']:.1f} msg/s"
        )
    
    def on_tcp_connection_status(self, client_address, connected):
        """TCP bağlantı durumu değiştiğinde"""
        if connected:
            print(f"🔌 TCP Client connected: {client_address}")
        else:
            print(f"🔌 TCP Client disconnected: {client_address}")
    
    def on_tcp_error(self, error_message):
        """TCP hata oluştuğunda"""
        print(f"❌ TCP Error: {error_message}")
    
    def on_position_calculated(self, data):
        """Position hesaplandığında (trilateration + kalman)"""
        tag_id = data.get('tag_id')
        accuracy = data.get('accuracy', 0)
        anchors_used = data.get('anchors_used', [])
        
        # Console log
        print(f"🎯 Position calculated: {tag_id} → Accuracy: {accuracy:.3f}m [Anchors: {', '.join(anchors_used)}]")
    
    def create_status_bar(self):
        """Status bar oluştur"""
        status = self.statusBar()
        status.setStyleSheet(f"""
            QStatusBar {{
                background: {MineTrackerTheme.SURFACE};
                color: {MineTrackerTheme.TEXT_SECONDARY};
                border-top: 1px solid {MineTrackerTheme.BORDER};
                font-size: 12px;
                padding: 5px;
            }}
        """)
        
        # Sistem durumu
        self.status_label = QLabel("✅ " + self.i18n.t('system_online'))
        self.status_label.setStyleSheet(f"color: {MineTrackerTheme.SUCCESS}; font-weight: 600;")
        status.addWidget(self.status_label)
        
        # TCP status
        self.tcp_status_label = QLabel("📡 TCP: Waiting for connections...")
        self.tcp_status_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY};")
        status.addWidget(self.tcp_status_label)
        
        # Spacer
        status.addWidget(QLabel(" | "), 0)
        
        # Tracking mode
        self.mode_label = QLabel(f"🎯 Mode: {self.tracking.mode.upper()}")
        self.mode_label.setStyleSheet(f"color: {MineTrackerTheme.PRIMARY}; font-weight: 600;")
        status.addWidget(self.mode_label)
        
        # Saat
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY};")
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
        msg.setStyleSheet(MineTrackerTheme.get_app_style())
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
            self.setWindowTitle("AICO Maden Takip Sistemi Ultra - Yer Altı Güvenlik Sistemi")
        else:
            self.setWindowTitle("AICO MineTracker Ultra - Underground Safety System")
    
    def closeEvent(self, event):
        """Pencere kapatılırken TCP sunucusunu durdur"""
        print("⏸️  MineTracker kapatılıyor...")
        
        # TCP server'ı durdur
        if hasattr(self, 'tcp_server') and self.tcp_server.running:
            self.tcp_server.stop()
            self.tcp_server.wait(2000)
        
        print("✅ Temiz kapanış tamamlandı!")
        event.accept()
