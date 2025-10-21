#!/usr/bin/env python3
"""
MineTracker - Test Script
PyQt6 kurulumu ve test
"""

import sys
import subprocess

def check_dependencies():
    """Bağımlılıkları kontrol et"""
    print("🔍 MineTracker Bağımlılık Kontrolü")
    print("=" * 50)
    
    # Python sürümü
    print(f"✅ Python: {sys.version.split()[0]}")
    
    # PyQt6 kontrolü
    try:
        import PyQt6
        print(f"✅ PyQt6: {PyQt6.__version__}")
    except ImportError:
        print("❌ PyQt6: YÜK DEĞIL")
        print("\n📦 PyQt6 kurulumu için:")
        print("   pip install PyQt6 PyQt6-WebEngine")
        return False
    
    # PyQt6-WebEngine
    try:
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        print("✅ PyQt6-WebEngine: Yüklü")
    except ImportError:
        print("❌ PyQt6-WebEngine: Yüklü Değil")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Tüm bağımlılıklar hazır!")
    return True


def test_services():
    """Servisleri test et"""
    print("\n🧪 Servis Testleri")
    print("=" * 50)
    
    try:
        from services.i18n import I18nService
        i18n = I18nService()
        print(f"✅ I18n Servisi: {i18n.t('app_title')}")
    except Exception as e:
        print(f"❌ I18n Servisi: {e}")
    
    try:
        from services.tracking_service import TrackingService
        tracking = TrackingService()
        stats = tracking.get_statistics()
        print(f"✅ Tracking Servisi: {stats['personnel']['total']} personel, {stats['equipment']['total']} ekipman")
    except Exception as e:
        print(f"❌ Tracking Servisi: {e}")
    
    print("=" * 50)


def run_app():
    """Uygulamayı çalıştır"""
    print("\n🚀 MineTracker Başlatılıyor...")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from app.app import MineTrackerApp
        
        # High DPI support
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        
        # Uygulama bilgileri
        app.setApplicationName("MineTracker")
        app.setOrganizationName("MineTracker Technologies")
        
        # Ana pencereyi oluştur ve göster
        window = MineTrackerApp()
        window.show()
        
        print("✅ MineTracker başlatıldı!")
        print("🗺️  3D Harita aktif")
        print("📡 Real-time tracking aktif")
        print("🌍 Türkçe/English dil desteği hazır")
        print("\n⚠️  Not: Bu test ortamında GUI görüntülenemeyebilir.")
        print("    Gerçek ortamda çalıştırın!")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n")
    print("⛏️  " + "=" * 46 + " ⛏️")
    print("   MineTracker - Yeraltı Madenci Takip Sistemi")
    print("⛏️  " + "=" * 46 + " ⛏️")
    print("\n")
    
    # Bağımlılıkları kontrol et
    deps_ok = check_dependencies()
    
    if deps_ok:
        # Servisleri test et
        test_services()
        
        # Uygulamayı çalıştırmayı dene
        print("\n⚠️  PyQt6 GUI uygulaması konteyner ortamında çalışmayabilir.")
        print("    Lütfen yerel makinenizde çalıştırın!\n")
        
    else:
        print("\n⚠️  Bağımlılıklar eksik. Lütfen PyQt6 yükleyin.")
        print("\nKurulum komutu:")
        print("  pip install PyQt6 PyQt6-WebEngine")
