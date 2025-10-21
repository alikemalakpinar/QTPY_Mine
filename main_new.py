#!/usr/bin/env python3
"""
MineTracker - Professional Underground Mining Personnel & Device Tracking System
Real-time location tracking with 3D visualization
Modular Architecture with Turkish/English Support
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.app import MineTrackerApp


def main():
    """Ana başlangıç noktası"""
    # High DPI support
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Uygulama bilgileri
    app.setApplicationName("MineTracker")
    app.setOrganizationName("MineTracker Technologies")
    app.setApplicationDisplayName("MineTracker - Yeraltı Güvenlik Sistemi")
    
    # Ana pencereyi oluştur ve göster
    window = MineTrackerApp()
    window.show()
    
    print("✅ MineTracker başlatıldı!")
    print("🗺️  3D Harita aktif")
    print("📡 Real-time tracking aktif")
    print("🌍 Türkçe/English dil desteği hazır")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
