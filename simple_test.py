#!/usr/bin/env python3
"""Simple MineTracker Test"""
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MineTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MineTracker - Underground Safety System")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("background: #0F0F0F;")
        
        # Simple test widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        # Title
        label = QLabel("⛏️ MineTracker System")
        label.setStyleSheet("font-size: 48px; color: #00E5FF; padding: 50px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status label
        self.status_label = QLabel("Sistem Hazır")
        self.status_label.setStyleSheet("font-size: 18px; color: #00FF88;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Start button
        btn = QPushButton("🚀 Start Tracking")
        btn.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                padding: 20px 40px;
                background: #00E5FF;
                color: black;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #33EEFF;
            }
            QPushButton:pressed {
                background: #00CCDD;
            }
        """)
        btn.clicked.connect(self.start_tracking)  # ✅ BURADA EKSİKTİ!
        btn.setFixedWidth(300)
        
        # Load full system button
        load_btn = QPushButton("📱 Tam Sistemi Aç")
        load_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 15px 30px;
                background: #9966FF;
                color: white;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #AA77FF;
            }
        """)
        load_btn.clicked.connect(self.load_full_system)
        load_btn.setFixedWidth(300)
        
        layout.addWidget(label)
        layout.addWidget(self.status_label)
        layout.addWidget(btn)
        layout.addWidget(load_btn)
        
        # Timer for demo
        self.is_tracking = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_tracking)
        self.count = 0
    
    def start_tracking(self):
        """Start tracking butonu"""
        if not self.is_tracking:
            self.is_tracking = True
            self.status_label.setText("✅ Tracking Başladı!")
            self.status_label.setStyleSheet("font-size: 18px; color: #00FF88;")
            self.timer.start(1000)  # Her saniye güncelle
            print("✅ Tracking başlatıldı!")
        else:
            self.is_tracking = False
            self.status_label.setText("⏸️ Tracking Durduruldu")
            self.status_label.setStyleSheet("font-size: 18px; color: #FFB800;")
            self.timer.stop()
            print("⏸️ Tracking durduruldu!")
    
    def update_tracking(self):
        """Tracking güncelleme"""
        self.count += 1
        self.status_label.setText(f"📡 Tracking Aktif... ({self.count} saniye)")
    
    def load_full_system(self):
        """Tam sistemi yükle"""
        reply = QMessageBox.question(
            self,
            "Tam Sistem",
            "Tam MineTracker sistemini başlatmak ister misiniz?\n\n"
            "Bu sistem şunları içerir:\n"
            "• 3D Harita\n"
            "• 15 Personel Takibi\n"
            "• 10 Ekipman Takibi\n"
            "• Acil Durum Sistemi\n"
            "• Türkçe/İngilizce Dil Desteği",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.status_label.setText("🔄 Tam sistem yükleniyor...")
            QTimer.singleShot(1000, self.actually_load_full_system)
    
    def actually_load_full_system(self):
        """Tam sistemi gerçekten yükle"""
        try:
            from app.app import MineTrackerApp as FullApp
            self.full_window = FullApp()
            self.full_window.show()
            self.hide()  # Bu pencereyi gizle
            print("✅ Tam sistem başlatıldı!")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Tam sistem yüklenemedi:\n\n{str(e)}\n\n"
                f"Lütfen konsol çıktısını kontrol edin."
            )
            print(f"❌ Hata: {e}")
            import traceback
            traceback.print_exc()


def main():
    print("\n" + "="*60)
    print("⛏️  MineTracker - Basit Test")
    print("="*60)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MineTrackerApp()
    window.show()
    
    print("\n✅ Pencere açıldı!")
    print("👉 'Start Tracking' butonuna tıklayın")
    print("👉 'Tam Sistemi Aç' ile full sistemi başlatın\n")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
