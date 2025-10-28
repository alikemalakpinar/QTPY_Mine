"""Gerçek zamanlı personel takip servisi - Anchor & Tag tabanlı (ENTERPRISE)"""
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import random
from datetime import datetime

class TrackingService(QObject):
    """Enterprise-grade tracking service - Anchor (Gateway) & Tag based"""
    
    # Signals
    location_updated = pyqtSignal(dict)  # Konum güncellemesi
    battery_alert = pyqtSignal(dict)  # Batarya uyarısı
    emergency_signal = pyqtSignal(dict)  # Acil durum sinyali
    status_changed = pyqtSignal(dict)  # Durum değişikliği
    anchor_status_changed = pyqtSignal(dict)  # Anchor durum değişikliği
    tag_status_changed = pyqtSignal(dict)  # Tag durum değişikliği
    
    def __init__(self):
        super().__init__()
        self.personnel = []
        self.tags = []  # Personnel tracking tags
        
        # Anchors (Fixed position gateway devices)
        self.anchors = [
            {
                'id': 'ANC001', 'name': 'Ana Şaft Anchor', 'zone': 'Ana Şaft', 
                'color': '#00D4FF', 'x': 0, 'y': 0, 'z': -10,
                'status': 'online', 'battery': 95, 'signal_strength': 98,
                'firmware_version': '2.1.0', 'last_maintenance': '2025-01-15',
                'coverage_radius': 100, 'type': 'anchor'
            },
            {
                'id': 'ANC002', 'name': 'Sektör A Anchor', 'zone': 'Sektör A',
                'color': '#00FF88', 'x': -350, 'y': -200, 'z': -25,
                'status': 'online', 'battery': 88, 'signal_strength': 95,
                'firmware_version': '2.1.0', 'last_maintenance': '2025-01-15',
                'coverage_radius': 100, 'type': 'anchor'
            },
            {
                'id': 'ANC003', 'name': 'Sektör B Anchor', 'zone': 'Sektör B',
                'color': '#FFB800', 'x': 350, 'y': -200, 'z': -30,
                'status': 'online', 'battery': 92, 'signal_strength': 96,
                'firmware_version': '2.1.0', 'last_maintenance': '2025-01-15',
                'coverage_radius': 100, 'type': 'anchor'
            },
            {
                'id': 'ANC004', 'name': 'Sektör C Anchor', 'zone': 'Sektör C',
                'color': '#9966FF', 'x': 0, 'y': 280, 'z': -20,
                'status': 'online', 'battery': 78, 'signal_strength': 92,
                'firmware_version': '2.0.5', 'last_maintenance': '2025-01-10',
                'coverage_radius': 100, 'type': 'anchor'
            },
            {
                'id': 'ANC005', 'name': 'İşleme Anchor', 'zone': 'İşleme',
                'color': '#FF3366', 'x': -250, 'y': 350, 'z': -15,
                'status': 'online', 'battery': 85, 'signal_strength': 94,
                'firmware_version': '2.1.0', 'last_maintenance': '2025-01-15',
                'coverage_radius': 100, 'type': 'anchor'
            },
            {
                'id': 'ANC006', 'name': 'Atölye Anchor', 'zone': 'Atölye',
                'color': '#00CCFF', 'x': 250, 'y': 350, 'z': -12,
                'status': 'online', 'battery': 90, 'signal_strength': 97,
                'firmware_version': '2.1.0', 'last_maintenance': '2025-01-15',
                'coverage_radius': 100, 'type': 'anchor'
            }
        ]
        
        # For backward compatibility
        self.gateways = self.anchors
        
        # Bölgeler (Gateway konumlarıyla aynı)
        self.zones = [
            {'id': 'ZONE_A', 'name': 'Ana Şaft', 'color': '#00D4FF', 'x': 0, 'y': 0},
            {'id': 'ZONE_B', 'name': 'Sektör A', 'color': '#00FF88', 'x': -350, 'y': -200},
            {'id': 'ZONE_C', 'name': 'Sektör B', 'color': '#FFB800', 'x': 350, 'y': -200},
            {'id': 'ZONE_D', 'name': 'Sektör C', 'color': '#9966FF', 'x': 0, 'y': 280},
            {'id': 'ZONE_E', 'name': 'İşleme', 'color': '#FF3366', 'x': -250, 'y': 350},
            {'id': 'ZONE_F', 'name': 'Atölye', 'color': '#00CCFF', 'x': 250, 'y': 350}
        ]
        
        self.init_personnel()
        
        # Gerçek zamanlı güncelleme
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_locations)
        self.update_timer.start(2000)  # Her 2 saniyede bir güncelle
        
    def init_personnel(self):
        """Demo personel verisi oluştur"""
        turkish_names = [
            ('Mehmet', 'Yılmaz', 'Maden Mühendisi'),
            ('Ayşe', 'Demir', 'Güvenlik Uzmanı'),
            ('Ahmet', 'Kaya', 'Operatör'),
            ('Fatma', 'Çelik', 'Ekip Lideri'),
            ('Ali', 'Öztürk', 'Teknisyen'),
            ('Zeynep', 'Aydın', 'Operatör'),
            ('Mustafa', 'Şahin', 'Maden Mühendisi'),
            ('Elif', 'Kurt', 'Güvenlik Görevlisi'),
            ('Can', 'Özdemir', 'Operatör'),
            ('Deniz', 'Arslan', 'Ekip Lideri'),
            ('Burak', 'Koç', 'Teknisyen'),
            ('Selin', 'Polat', 'Operatör'),
            ('Emre', 'Güneş', 'Maden Mühendisi'),
            ('Merve', 'Yıldız', 'Güvenlik Uzmanı'),
            ('Onur', 'Akın', 'Operatör')
        ]
        
        for i, (first_name, last_name, position) in enumerate(turkish_names, 1):
            zone = random.choice(self.zones)
            tag_id = f'TAG{i:03d}'
            person_id = f'P{i:03d}'
            
            # Create person
            person = {
                'id': person_id,
                'first_name': first_name,
                'last_name': last_name,
                'full_name': f'{first_name} {last_name}',
                'position': position,
                'zone_id': zone['id'],
                'zone_name': zone['name'],
                'location': {
                    'x': zone['x'] + random.uniform(-50, 50),
                    'y': zone['y'] + random.uniform(-50, 50),
                    'z': random.uniform(-50, -5)
                },
                'status': random.choice(['active', 'active', 'active', 'break']),
                'heart_rate': random.randint(60, 95),
                'battery': random.randint(30, 100),
                'signal': random.randint(80, 100),
                'last_update': datetime.now(),
                'shift': random.choice(['Gündüz', 'Gece']),
                'entry_time': '08:00',
                'tag_id': tag_id,
                'phone': f'+90 555 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}',
                'email': f'{first_name.lower()}.{last_name.lower()}@minetracker.com'
            }
            self.personnel.append(person)
            
            # Create corresponding tag
            tag = {
                'id': tag_id,
                'person_id': person_id,
                'person_name': f'{first_name} {last_name}',
                'battery': random.randint(30, 100),
                'signal_strength': random.randint(80, 100),
                'firmware_version': random.choice(['1.8.2', '1.9.0', '2.0.0']),
                'status': 'active' if person['status'] == 'active' else 'inactive',
                'last_seen': datetime.now(),
                'type': 'tag'
            }
            self.tags.append(tag)
    
    def update_locations(self):
        """Konumları güncelle (Anchor ve Tag simülasyonu)"""
        # Personel konumlarını güncelle - Anchor sinyalleriyle
        for person in self.personnel:
            if person['status'] == 'active' and random.random() < 0.4:
                # Hareket simülasyonu
                person['location']['x'] += random.uniform(-5, 5)
                person['location']['y'] += random.uniform(-5, 5)
                person['location']['z'] += random.uniform(-1, 1)
                
                # Sınırlar içinde tut
                person['location']['x'] = max(-500, min(500, person['location']['x']))
                person['location']['y'] = max(-400, min(400, person['location']['y']))
                person['location']['z'] = max(-100, min(-5, person['location']['z']))
                
                # Bölge güncelle
                person['zone_id'], person['zone_name'] = self.determine_zone(person['location'])
                
                # Kalp atışı güncelle
                person['heart_rate'] = max(60, min(110, person['heart_rate'] + random.randint(-3, 3)))
                
                # Batarya düşür (tag bataryası)
                if random.random() < 0.05:
                    person['battery'] = max(0, person['battery'] - random.randint(1, 3))
                    if person['battery'] < 20:
                        self.battery_alert.emit({
                            'type': 'personnel',
                            'id': person['id'],
                            'name': person['full_name'],
                            'battery': person['battery']
                        })
                
                # Update tag info
                tag = next((t for t in self.tags if t['person_id'] == person['id']), None)
                if tag:
                    tag['battery'] = person['battery']
                    tag['signal_strength'] = person['signal']
                    tag['last_seen'] = datetime.now()
                
                person['last_update'] = datetime.now()
                
                # Konum güncellemesi sinyali
                self.location_updated.emit({
                    'type': 'personnel',
                    'data': person
                })
        
        # Anchor durumlarını güncelle (az sıklıkta)
        if random.random() < 0.1:
            for anchor in self.anchors:
                # Batarya yavaş düşüş
                if random.random() < 0.05:
                    anchor['battery'] = max(50, anchor['battery'] - random.randint(0, 1))
                    if anchor['battery'] < 70:
                        self.battery_alert.emit({
                            'type': 'anchor',
                            'id': anchor['id'],
                            'name': anchor['name'],
                            'battery': anchor['battery']
                        })
                
                # Sinyal gücü hafif değişim
                anchor['signal_strength'] = max(85, min(100, 
                    anchor['signal_strength'] + random.randint(-2, 2)))
    
    def get_anchors(self):
        """Tüm anchor'ları al"""
        return self.anchors
    
    def get_tags(self):
        """Tüm tag'leri al"""
        return self.tags
    
    def get_tag_by_id(self, tag_id):
        """ID'ye göre tag bul"""
        for tag in self.tags:
            if tag['id'] == tag_id:
                return tag
        return None
    
    def get_anchor_by_id(self, anchor_id):
        """ID'ye göre anchor bul"""
        for anchor in self.anchors:
            if anchor['id'] == anchor_id:
                return anchor
        return None
    
    def update_anchor_status(self, anchor_id, status):
        """Anchor durumunu güncelle"""
        anchor = self.get_anchor_by_id(anchor_id)
        if anchor:
            anchor['status'] = status
            self.anchor_status_changed.emit({
                'id': anchor_id,
                'status': status,
                'anchor': anchor
            })
    
    def update_tag_status(self, tag_id, status):
        """Tag durumunu güncelle"""
        tag = self.get_tag_by_id(tag_id)
        if tag:
            tag['status'] = status
            self.tag_status_changed.emit({
                'id': tag_id,
                'status': status,
                'tag': tag
            })
    
    def determine_zone(self, location):
        """Koordinatlara göre bölge belirle - Anchor sinyaline göre"""
        x, y = location['x'], location['y']
        
        # En yakın anchor'ı bul
        min_dist = float('inf')
        closest_zone = self.zones[0]
        
        for zone in self.zones:
            dist = ((x - zone['x'])**2 + (y - zone['y'])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closest_zone = zone
        
        return closest_zone['id'], closest_zone['name']
    
    def get_personnel(self):
        """Tüm personeli al"""
        return self.personnel
    
    def get_gateways(self):
        """Tüm gateway'leri al (backward compatibility)"""
        return self.anchors
    
    def get_zones(self):
        """Tüm bölgeleri al"""
        return self.zones
    
    def get_person_by_id(self, person_id):
        """ID'ye göre personel bul"""
        for person in self.personnel:
            if person['id'] == person_id:
                return person
        return None
    
    def trigger_emergency(self, entity_id, entity_type='personnel'):
        """Acil durum tetikle"""
        entity = self.get_person_by_id(entity_id)
        if entity:
            entity['status'] = 'emergency'
            self.emergency_signal.emit({
                'type': 'personnel',
                'id': entity_id,
                'name': entity['full_name'],
                'position': entity['position'],
                'location': entity['location'],
                'zone': entity['zone_name'],
                'timestamp': datetime.now().isoformat()
            })
    
    def get_statistics(self):
        """İstatistikleri al - Personel, Anchor ve Tag"""
        active_personnel = sum(1 for p in self.personnel if p['status'] == 'active')
        on_break = sum(1 for p in self.personnel if p['status'] == 'break')
        emergency_count = sum(1 for p in self.personnel if p['status'] == 'emergency')
        
        avg_battery_personnel = sum(p['battery'] for p in self.personnel) / len(self.personnel) if self.personnel else 0
        low_battery_personnel = sum(1 for p in self.personnel if p['battery'] < 20)
        
        # Anchor stats
        online_anchors = sum(1 for a in self.anchors if a['status'] == 'online')
        avg_battery_anchors = sum(a['battery'] for a in self.anchors) / len(self.anchors) if self.anchors else 0
        low_battery_anchors = sum(1 for a in self.anchors if a['battery'] < 70)
        
        # Tag stats
        active_tags = sum(1 for t in self.tags if t['status'] == 'active')
        avg_battery_tags = sum(t['battery'] for t in self.tags) / len(self.tags) if self.tags else 0
        low_battery_tags = sum(1 for t in self.tags if t['battery'] < 20)
        
        return {
            'personnel': {
                'total': len(self.personnel),
                'active': active_personnel,
                'on_break': on_break,
                'emergency': emergency_count,
                'avg_battery': round(avg_battery_personnel, 1),
                'low_battery': low_battery_personnel
            },
            'anchors': {
                'total': len(self.anchors),
                'online': online_anchors,
                'offline': len(self.anchors) - online_anchors,
                'avg_battery': round(avg_battery_anchors, 1),
                'low_battery': low_battery_anchors
            },
            'tags': {
                'total': len(self.tags),
                'active': active_tags,
                'inactive': len(self.tags) - active_tags,
                'avg_battery': round(avg_battery_tags, 1),
                'low_battery': low_battery_tags
            },
            'gateways': {  # Backward compatibility
                'total': len(self.anchors),
                'online': online_anchors,
                'offline': len(self.anchors) - online_anchors
            }
        }

