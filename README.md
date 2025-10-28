# ⛏️ Aico Maden Takip - Yeraltı Madenci Takip Sistemi

## 📋 Genel Bakış

Aico Maden Takip, yeraltı madencilerinin gerçek zamanlı konumlarını takip eden, 3D görselleştirme sunan ve acil durum yönetimi sağlayan profesyonel bir masaüstü uygulamasıdır.

### ✨ Özellikler

#### 🎯 Temel Özellikler
- **Gerçek Zamanlı Takip**: Tüm personel ve ekipmanın anlık konum takibi
- **3D Görselleştirme**: Three.js tabanlı interaktif 3D maden haritası
- **Acil Durum Sistemi**: SOS sinyalleri, acil durum protokolleri
- **Çok Dilli Destek**: Türkçe ve İngilizce arayüz
- **Modern UI/UX**: Koyu tema, kullanıcı dostu tasarım

#### 📱 Ekranlar
1. **🏠 Dashboard**: Genel durum özeti, istatistikler
2. **🗺️ Canlı 3D Harita**: Tüm varlıkların 3D konumları
3. **👥 Personel Yönetimi**: Detaylı personel takibi
4. **🚜 Ekipman Takibi**: Ekipman durumu ve konumları
5. **🚨 Acil Durum Merkezi**: SOS yönetimi ve protokoller
6. **📊 Raporlar**: Vardiya, performans, olay raporları
7. **📍 Bölgeler**: Maden bölgelerinin yönetimi
8. **⚙️ Ayarlar**: Dil, bildirim, sistem ayarları

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- PyQt6 6.6.0+
- Display server (X11, Wayland veya Windows)

### Adımlar

1. **Bağımlılıkları yükleyin**:
```bash
pip install PyQt6>=6.6.0 PyQt6-WebEngine>=6.6.0
```

2. **Uygulamayı çalıştırın**:
```bash
python3 main.py
```

---

## 📁 Proje Yapısı

```
/app/
├── main.py                      # Ana başlangıç noktası
├── requirements.txt             # Python bağımlılıkları
│
├── app/                         # Ana uygulama modülü
│   ├── app.py                  # Ana uygulama sınıfı
│   └── navigation.py           # Navigasyon sidebar
│
├── screens/                     # Tüm uygulama ekranları
├── components/                  # Yeniden kullanılabilir bileşenler
├── services/                    # Backend servisleri
├── store/                       # State management
└── theme/                       # Tema ve stiller
```

---

## 🎮 Kullanım

### Temel Kullanım

```bash
python3 main.py
```

### Dil Değiştirme
- Ayarlar ekranından Türkçe/English seçebilirsiniz
- Tüm arayüz otomatik güncellenir

### 3D Harita Kontrolleri
- **Fare**: 3D haritayı döndür
- **Scroll**: Yakınlaştır/Uzaklaştır  
- **Ok Tuşları**: Kamerayı hareket ettir

---

## 📸 Özellikler

### ✅ Tamamlanan Özellikler

- ✅ Modüler mimari yapısı
- ✅ Türkçe/İngilizce dil desteği
- ✅ 3D maden görselleştirmesi
- ✅ Gerçek zamanlı personel takibi (15 personel)
- ✅ Ekipman takibi (10 ekipman)
- ✅ Acil durum yönetim sistemi
- ✅ Dashboard ve istatistikler
- ✅ Bölge yönetimi (6 bölge)
- ✅ Raporlama sistemi
- ✅ Modern koyu tema
- ✅ Batarya uyarı sistemi
- ✅ Kalp atışı takibi
- ✅ State management

### 🎨 Tasarım Özellikleri

- Modern, koyu tema (gözleri yormaz)
- Büyük, okunabilir fontlar
- Renkli durum göstergeleri
- İnteraktif tablolar
- Animasyonlu geçişler
- Responsive kartlar

---

## 🔧 Yapılandırma

### Servisleri Kullanma

```python
from services.i18n import I18nService
from services.tracking_service import TrackingService

# Dil servisi
i18n = I18nService()
i18n.set_language('tr')  # Türkçe

# Takip servisi  
tracking = TrackingService()
personnel = tracking.get_personnel()
stats = tracking.get_statistics()
```

---

## 🐛 Sorun Giderme

### PyQt6 Kurulum Hatası
```bash
# Linux
sudo apt-get install python3-pyqt6 python3-pyqt6.qtwebengine

# macOS
brew install pyqt6

# Windows
pip install PyQt6 PyQt6-WebEngine
```

### Display Server Hatası
- GUI uygulaması için display server gereklidir
- Headless/container ortamlarında çalışmaz
- Yerel makinenizde çalıştırın

---

## 📝 Notlar

- **Demo Modu**: Uygulama şu anda simülasyon verileri kullanıyor
- **Gerçek Ortam**: Gerçek sensör/GPS verileri entegre edilebilir
- **Konteyner**: Bu bir desktop uygulamasıdır, web tarayıcısında çalışmaz

---

## 👨‍💻 Geliştirici

**Aico Maden Takip Development Team**

---

## 📄 Lisans

Bu proje özel bir projedir. Tüm hakları saklıdır.

---

**⛏️ Aico Maden Takip - Madencilerin Güvenliği İçin Teknoloji**
