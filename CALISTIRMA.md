# 🚀 MineTracker - ÇALIŞTIRMA TALİMATLARI

## ⚠️ ÖNEMLİ NOTLAR

### Bu bir Desktop Uygulamasıdır!
- PyQt6 GUI uygulaması
- Yerel makinenizde çalıştırılmalı
- Display server gereklidir (pencere sistemi)
- **Konteyner/headless ortamlarda GUI gösterilemez!**

---

## 📥 KURULUM

### Ön Gereksinimler
```bash
Python 3.8+
Display Server (X11, Wayland veya Windows)
```

### Adım 1: Dosyaları İndirin
```bash
# Tüm /app klasörünü yerel makinenize kopyalayın
```

### Adım 2: PyQt6 Kurun

**Windows:**
```bash
pip install PyQt6 PyQt6-WebEngine
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-pyqt6 python3-pyqt6.qtwebengine
# VEYA
pip install PyQt6 PyQt6-WebEngine
```

**macOS:**
```bash
brew install pyqt6
# VEYA  
pip install PyQt6 PyQt6-WebEngine
```

**Otomatik Kurulum (Linux/macOS):**
```bash
chmod +x install.sh
./install.sh
```

---

## 🎮 ÇALIŞTIRMA

### Seçenek 1: Basit Test (Önerilen İlk Adım)
```bash
python3 simple_test.py
```

**Ne yapacak:**
- Basit bir pencere açar
- "Start Tracking" butonu ile tracking testi
- "Tam Sistemi Aç" butonu ile full sisteme geçiş
- Sorun giderme için idealdir

### Seçenek 2: Tam Sistem
```bash
python3 main.py
```

**Tam sistem özellikleri:**
- 8 farklı ekran
- 3D harita
- 15 personel + 10 ekipman takibi
- Türkçe/İngilizce dil desteği
- Acil durum sistemi

---

## 🐛 SORUN GİDERME

### Hata 1: "No module named 'PyQt6'"
```bash
# Çözüm:
pip install PyQt6 PyQt6-WebEngine
```

### Hata 2: "cannot connect to X server"
```bash
# Çözüm: Display server gereklidir
# Linux: DISPLAY=:0 python3 main.py
# Veya yerel makinenizde çalıştırın
```

### Hata 3: "Import hatası"
```bash
# Çözüm: types klasörü sorunu
cd /app
mv types app_types  # Eğer hala types varsa
python3 main.py
```

### Hata 4: Butona basınca çalışmıyor
```bash
# Çözüm: simple_test.py kullanın, düzeltilmiş versiyondur
python3 simple_test.py
```

---

## 📋 DOSYA YAPISI

```
/app/
├── simple_test.py         # ✅ BU DOSYAYI ÖNCE ÇALIŞTIRIN
├── main.py                # Tam sistem
├── install.sh             # Otomatik kurulum
├── README.md              # Detaylı dokümantasyon
│
├── app/                   # Ana uygulama
│   ├── app.py            # Ana pencere
│   └── navigation.py     # Menü
│
├── screens/               # Tüm ekranlar
│   ├── home/             # Dashboard, 3D harita
│   ├── people/           # Personel
│   ├── equipment/        # Ekipman
│   ├── safety/           # Acil durum
│   ├── reports/          # Raporlar
│   ├── zones/            # Bölgeler
│   └── settings/         # Ayarlar
│
├── services/              # Backend
│   ├── i18n.py           # Dil desteği
│   └── tracking_service.py  # Takip
│
├── components/            # Bileşenler
│   └── model3d/          # 3D harita
│       └── mine_3d_view.py
│
└── theme/                 # Tasarım
    └── theme.py
```

---

## ✅ TEST ETTİKTEN SONRA

### 1. Basit Test Çalıştı mı?
```bash
python3 simple_test.py
# "Start Tracking" butonuna tıklayın
# Timer çalışıyor mu kontrol edin
```

### 2. Tam Sistemi Deneyin
```bash
python3 simple_test.py
# "Tam Sistemi Aç" butonuna tıklayın
# Veya doğrudan:
python3 main.py
```

### 3. Özellikleri Test Edin
- Dashboard: İstatistikleri görün
- 3D Harita: Fareyle döndürün
- Personel: Listeyi inceleyin
- Ayarlar: Dili değiştirin (TR/EN)
- Acil Durum: Test SOS butonunu deneyin

---

## 🎯 DEMO VERİLERİ

Uygulama simülasyon verileri içerir:
- **15 Personel** - Türk isimleriyle
- **10 Ekipman** - Türkçe isimlerle
- **6 Bölge** - Maden sektörleri
- **Her 2 saniye** güncelleme
- **Kalp atışı, batarya** simülasyonu

---

## 📞 DESTEK

Sorun yaşarsanız:

1. **Konsol çıktısını kontrol edin**
   ```bash
   python3 simple_test.py 2>&1 | tee log.txt
   ```

2. **PyQt6 versiyonunu kontrol edin**
   ```bash
   python3 -c "from PyQt6.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)"
   ```

3. **Display server test**
   ```bash
   echo $DISPLAY  # Linux/macOS
   ```

---

## 🎨 EKSİKSİZ ÖZELLİKLER

✅ Modüler mimari
✅ Türkçe/İngilizce
✅ 3D görselleştirme
✅ Gerçek zamanlı takip
✅ 8 tam ekran
✅ Acil durum sistemi
✅ Modern koyu tema
✅ Batarya/kalp atışı takibi
✅ State management
✅ Bölge yönetimi

---

**⛏️ İyi Kullanımlar! - MineTracker Team**
