"""Çok dilli destek servisi - Türkçe/İngilizce"""
from PyQt6.QtCore import QObject, pyqtSignal

class I18nService(QObject):
    """Uygulama çok dilli destek servisi"""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_language = 'tr'  # Varsayılan Türkçe
        
        # Tüm çeviriler
        self.translations = {
            'tr': {
                # Navigasyon
                'app_title': 'Aico Maden Takip',
                'app_subtitle': 'Yeraltı Güvenlik ve Takip Sistemi',
                'dashboard': 'Kontrol Paneli',
                'live_map': 'Canlı 3D Harita',
                'personnel': 'Personel',
                'equipment': 'Ekipman',
                'emergency': 'Acil Durum',
                'reports': 'Raporlar',
                'zones': 'Bölgeler',
                'settings': 'Ayarlar',
                'emergency_button': '🚨 ACİL DURUM',
                
                # Dashboard
                'safety_dashboard': 'Güvenlik Kontrol Paneli',
                'realtime_monitoring': 'Gerçek Zamanlı İzleme',
                'active_personnel': 'Aktif Personel',
                'equipment_online': 'Aktif Ekipman',
                'safety_incidents': 'Güvenlik Olayları',
                'zone_temperature': 'Bölge Sıcaklığı',
                'underground': 'Yer Altında',
                'operational': 'Çalışıyor',
                'incident_free': 'saat olay yok',
                'within_limits': 'Güvenli sınırlar içinde',
                'recent_alerts': '🚨 Son Uyarılar',
                'recent_activity': '📋 Son Aktiviteler',
                'live_mine_map': '🗺️ Canlı Maden Haritası',
                'equipment_status': '🚜 Ekipman Durumu',
                'view_all': 'Tümünü Gör',
                'fullscreen': 'Tam Ekran',
                'online': 'Çevrimiçi',
                'offline': 'Çevrimdışı',
                'maintenance': 'Bakımda',
                
                # Personel
                'personnel_tracking': '📍 Personel Takibi',
                'search_personnel': '🔍 Personel ara...',
                'total_underground': 'Toplam Yer Altında',
                'active_now': 'Şu Anda Aktif',
                'on_break': 'Molada',
                'emergency_drills': 'Acil Durum Tatbikatı',
                'person_id': 'Personel ID',
                'name': 'Ad Soyad',
                'position': 'Pozisyon',
                'zone': 'Bölge',
                'status': 'Durum',
                'heart_rate': 'Kalp Atışı',
                'battery': 'Batarya',
                'last_update': 'Son Güncelleme',
                'actions': 'İşlemler',
                'active': 'Aktif',
                'break': 'Mola',
                'emergency': 'ACİL DURUM',
                'locate': 'Yerini Bul',
                'profile': 'Profil',
                'contact': 'İletişim',
                
                # Ekipman
                'equipment_tracking': '🚜 Ekipman Takibi',
                'search_equipment': '🔍 Ekipman ara...',
                'total_equipment': 'Toplam Ekipman',
                'critical_alerts': 'Kritik Uyarılar',
                'avg_battery': 'Ortalama Batarya',
                'equipment_id': 'Ekipman ID',
                'type': 'Tip',
                'operator': 'Operatör',
                'location': 'Konum',
                'fuel': 'Yakıt',
                'signal': 'Sinyal',
                'health_score': 'Sağlık Skoru',
                
                # Acil Durum
                'emergency_center': '🚨 Acil Durum Merkezi',
                'active_emergencies': 'Aktif Acil Durumlar',
                'emergency_contacts': 'Acil Durum Kontakları',
                'evacuation_status': 'Tahliye Durumu',
                'response_time': 'Müdahale Süresi',
                'trigger_emergency': 'Acil Durum Başlat',
                'emergency_protocol': 'Acil Durum Protokolü',
                'all_clear': 'Tehlike Yok',
                'evacuating': 'Tahliye Ediliyor',
                'responding': 'Müdahale Ediliyor',
                
                # Ayarlar
                'general_settings': '⚙️ Genel Ayarlar',
                'language': 'Dil',
                'turkish': 'Türkçe',
                'english': 'İngilizce',
                'theme': 'Tema',
                'dark_theme': 'Koyu Tema',
                'light_theme': 'Açık Tema',
                'notifications': 'Bildirimler',
                'sound_alerts': 'Sesli Uyarılar',
                'visual_alerts': 'Görsel Uyarılar',
                'system_status': 'Sistem Durumu',
                'connected': 'Bağlı',
                'disconnected': 'Bağlantı Kesildi',
                'version': 'Sürüm',
                
                # Genel
                'save': 'Kaydet',
                'cancel': 'İptal',
                'confirm': 'Onayla',
                'close': 'Kapat',
                'loading': 'Yükleniyor...',
                'error': 'Hata',
                'success': 'Başarılı',
                'warning': 'Uyarı',
                'info': 'Bilgi',
                'yes': 'Evet',
                'no': 'Hayır',
                'good': 'İyi',
                'fair': 'Orta',
                'poor': 'Kötü',
                'critical': 'Kritik',
                'just_now': 'Şimdi',
                'min_ago': 'dakika önce',
                'hour_ago': 'saat önce',
                'system_online': '✅ Sistem Çevrimiçi',
            },
            'en': {
                # Navigation
                'app_title': 'Aico Mining Track',
                'app_subtitle': 'Underground Safety & Tracking System',
                'dashboard': 'Dashboard',
                'live_map': 'Live 3D Map',
                'personnel': 'Personnel',
                'equipment': 'Equipment',
                'emergency': 'Emergency',
                'reports': 'Reports',
                'zones': 'Zones',
                'settings': 'Settings',
                'emergency_button': '🚨 EMERGENCY',
                
                # Dashboard
                'safety_dashboard': 'Safety Dashboard',
                'realtime_monitoring': 'Real-time Monitoring',
                'active_personnel': 'Active Personnel',
                'equipment_online': 'Equipment Online',
                'safety_incidents': 'Safety Incidents',
                'zone_temperature': 'Zone Temperature',
                'underground': 'Underground',
                'operational': 'Operational',
                'incident_free': 'hours incident-free',
                'within_limits': 'Within safe limits',
                'recent_alerts': '🚨 Recent Alerts',
                'recent_activity': '📋 Recent Activity',
                'live_mine_map': '🗺️ Live Mine Map',
                'equipment_status': '🚜 Equipment Status',
                'view_all': 'View All',
                'fullscreen': 'Fullscreen',
                'online': 'Online',
                'offline': 'Offline',
                'maintenance': 'Maintenance',
                
                # Personnel
                'personnel_tracking': '📍 Personnel Tracking',
                'search_personnel': '🔍 Search personnel...',
                'total_underground': 'Total Underground',
                'active_now': 'Active Now',
                'on_break': 'On Break',
                'emergency_drills': 'Emergency Drills',
                'person_id': 'Person ID',
                'name': 'Name',
                'position': 'Position',
                'zone': 'Zone',
                'status': 'Status',
                'heart_rate': 'Heart Rate',
                'battery': 'Battery',
                'last_update': 'Last Update',
                'actions': 'Actions',
                'active': 'Active',
                'break': 'Break',
                'emergency': 'EMERGENCY',
                'locate': 'Locate',
                'profile': 'Profile',
                'contact': 'Contact',
                
                # Equipment
                'equipment_tracking': '🚜 Equipment Tracking',
                'search_equipment': '🔍 Search equipment...',
                'total_equipment': 'Total Equipment',
                'critical_alerts': 'Critical Alerts',
                'avg_battery': 'Average Battery',
                'equipment_id': 'Equipment ID',
                'type': 'Type',
                'operator': 'Operator',
                'location': 'Location',
                'fuel': 'Fuel',
                'signal': 'Signal',
                'health_score': 'Health Score',
                
                # Emergency
                'emergency_center': '🚨 Emergency Center',
                'active_emergencies': 'Active Emergencies',
                'emergency_contacts': 'Emergency Contacts',
                'evacuation_status': 'Evacuation Status',
                'response_time': 'Response Time',
                'trigger_emergency': 'Trigger Emergency',
                'emergency_protocol': 'Emergency Protocol',
                'all_clear': 'All Clear',
                'evacuating': 'Evacuating',
                'responding': 'Responding',
                
                # Settings
                'general_settings': '⚙️ General Settings',
                'language': 'Language',
                'turkish': 'Turkish',
                'english': 'English',
                'theme': 'Theme',
                'dark_theme': 'Dark Theme',
                'light_theme': 'Light Theme',
                'notifications': 'Notifications',
                'sound_alerts': 'Sound Alerts',
                'visual_alerts': 'Visual Alerts',
                'system_status': 'System Status',
                'connected': 'Connected',
                'disconnected': 'Disconnected',
                'version': 'Version',
                
                # General
                'save': 'Save',
                'cancel': 'Cancel',
                'confirm': 'Confirm',
                'close': 'Close',
                'loading': 'Loading...',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning',
                'info': 'Info',
                'yes': 'Yes',
                'no': 'No',
                'good': 'Good',
                'fair': 'Fair',
                'poor': 'Poor',
                'critical': 'Critical',
                'just_now': 'Just now',
                'min_ago': 'min ago',
                'hour_ago': 'hour ago',
                'system_online': '✅ System Online',
            }
        }
    
    def t(self, key, default=None):
        """Çeviri al - Get translation"""
        translation = self.translations.get(self.current_language, {}).get(key)
        if translation:
            return translation
        # Fallback to English
        translation = self.translations.get('en', {}).get(key)
        if translation:
            return translation
        return default or key
    
    def set_language(self, language_code):
        """Dil değiştir - Change language"""
        if language_code in ['tr', 'en']:
            self.current_language = language_code
            self.language_changed.emit(language_code)
            return True
        return False
    
    def get_current_language(self):
        """Mevcut dili al - Get current language"""
        return self.current_language
    
    def get_available_languages(self):
        """Mevcut dilleri al - Get available languages"""
        return [
            {'code': 'tr', 'name': 'Türkçe', 'flag': '🇹🇷'},
            {'code': 'en', 'name': 'English', 'flag': '🇬🇧'}
        ]
