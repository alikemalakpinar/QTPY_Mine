#!/usr/bin/env python3
"""
MineTracker - Professional Underground Mining Personnel & Device Tracking System
Real-time location tracking with 3D visualization
Modular Architecture with Turkish/English Support
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# ⚠️ IMPORTANT: QtWebEngineWidgets MUST be imported BEFORE QApplication is created
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except ImportError:
    print("⚠️ Warning: QtWebEngineWidgets not available. 3D map may not work.")
    QWebEngineView = None

from app.app import MineTrackerApp


def main():
    """Ana başlangıç noktası"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Uygulama bilgileri
    app.setApplicationName("AICO - MineTracker")
    app.setOrganizationName("AICO Technologies")
    app.setApplicationDisplayName("AICO Maden Takip Sistemi - Yeraltı Güvenlik Sistemi")
    
    # Ana pencereyi oluştur ve göster
    window = MineTrackerApp()
    window.show()
    
    print("✅ AICO Maden Takip Sistemi başlatıldı!")
    print("🗺️  3D Harita aktif")
    print("📡 Real-time tracking aktif")
    print("🌍 Türkçe/English dil desteği hazır")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
