#!/usr/bin/env python3
"""
Aico Maden Takip - Profesyonel Yeraltı Madenci ve Cihaz Takip Sistemi
Gerçek zamanlı konum takibi ve 3D görselleştirme
Modüler mimari ile Türkçe/İngilizce destek
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

from app.app import AicoMadenTakipApp


def main():
    """Ana başlangıç noktası"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Uygulama bilgileri
    app.setApplicationName("AicoMadenTakip")
    app.setOrganizationName("Aico Teknoloji")
    app.setApplicationDisplayName("Aico Maden Takip - Yeraltı Güvenlik Sistemi")
    
    # Ana pencereyi oluştur ve göster
    window = AicoMadenTakipApp()
    window.show()
    
    print("✅ Aico Maden Takip başlatıldı!")
    print("🗺️  3D Harita aktif")
    print("📡 Gerçek zamanlı takip aktif")
    print("🌍 Türkçe/English dil desteği hazır")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
