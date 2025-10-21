#!/bin/bash
# MineTracker Kurulum ve Çalıştırma Scripti

echo "⛏️  MineTracker - Kurulum Başlatılıyor..."
echo "================================================"

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python 3.8+ yükleyin."
    exit 1
fi

echo "✅ Python bulundu: $(python3 --version)"

# PyQt6 kurulumu
echo ""
echo "📦 PyQt6 kuruluyor..."
pip install PyQt6>=6.6.0 PyQt6-WebEngine>=6.6.0

if [ $? -eq 0 ]; then
    echo "✅ PyQt6 kurulumu başarılı!"
else
    echo "❌ PyQt6 kurulumu başarısız!"
    echo ""
    echo "Manuel kurulum için:"
    echo "  Linux: sudo apt-get install python3-pyqt6 python3-pyqt6.qtwebengine"
    echo "  macOS: brew install pyqt6"
    echo "  Windows: pip install PyQt6 PyQt6-WebEngine"
    exit 1
fi

# Test
echo ""
echo "🧪 Kurulum test ediliyor..."
python3 -c "from PyQt6.QtWidgets import QApplication; print('✅ PyQt6 hazır!')"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ KURULUM TAMAMLANDI!"
    echo "================================================"
    echo ""
    echo "Çalıştırma:"
    echo "  1. Basit Test:  python3 simple_test.py"
    echo "  2. Tam Sistem:  python3 main.py"
    echo ""
    echo "Not: GUI için display server gereklidir (X11/Wayland)"
    echo "================================================"
else
    echo "❌ Test başarısız! PyQt6 doğru kurulmadı."
    exit 1
fi
