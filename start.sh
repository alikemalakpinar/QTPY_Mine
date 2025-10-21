#!/bin/bash
# MineTracker Hızlı Başlatma

echo "⛏️  MineTracker Hızlı Başlatma"
echo "================================================"
echo ""

# PyQt6-WebEngine kontrolü
echo "🔍 QtWebEngine kontrolü..."
python3 -c "from PyQt6.QtWebEngineWidgets import QWebEngineView; print('✅ QtWebEngine mevcut')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ QtWebEngine bulunamadı!"
    echo ""
    echo "📦 Kurulum için:"
    echo "   pip install PyQt6-WebEngine"
    echo ""
    read -p "Şimdi yüklemek ister misiniz? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install PyQt6-WebEngine
    fi
fi

echo ""
echo "================================================"
echo "🚀 Uygulamayı başlatıyorum..."
echo "================================================"
echo ""

# Ana uygulamayı başlat
python3 main.py
