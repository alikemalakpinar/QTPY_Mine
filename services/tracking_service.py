"""Gerçek zamanlı personel ve ekipman takip servisi"""
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import random
from datetime import datetime

class TrackingService(QObject):
    """Personel ve ekipman takip servisi"""
    
    # Signals
    location_updated = pyqtSignal(dict)  # Konum güncellemesi
    battery_alert = pyqtSignal(dict)  # Batarya uyarısı
    emergency_signal = pyqtSignal(dict)  # Acil durum sinyali
    status_changed = pyqtSignal(dict)  # Durum değişikliği
    
    def __init__(self):
        super().__init__()
        self.personnel = []
        self.equipment = []
        self.zones = [
            {'id': 'ZONE_A', 'name': 'Ana Şaft', 'color': '#00D4FF', 'x': 0, 'y': 0},
            {'id': 'ZONE_B', 'name': 'Sektör A', 'color': '#00FF88', 'x': -300, 'y': -150},
            {'id': 'ZONE_C', 'name': 'Sektör B', 'color': '#FFB800', 'x': 300, 'y': -150},
            {'id': 'ZONE_D', 'name': 'Sektör C', 'color': '#FF3366', 'x': 0, 'y': 200},
            {'id': 'ZONE_E', 'name': 'İşleme', 'color': '#9966FF', 'x': -200, 'y': 300},
            {'id': 'ZONE_F', 'name': 'Atölye', 'color': '#00CCFF', 'x': 200, 'y': 300}
        ]
        
        self.init_personnel()
        self.init_equipment()
        
        # Gerçek zamanlı güncelleme timer'ı
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
            person = {
                'id': f'P{i:03d}',
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
                'entry_time': '08:00'
            }
            self.personnel.append(person)
    
    def init_equipment(self):
        """Demo ekipman verisi oluştur"""
        equipment_list = [
            ('Ekskavatör #1', 'Ağır Ekipman', 'Heavy'),
            ('Yükleyici #2', 'Ağır Ekipman', 'Heavy'),
            ('Matkap #3', 'Delme', 'Drilling'),
            ('Kamyon #4', 'Taşıma', 'Transport'),
            ('Vinç #5', 'Destek', 'Support'),
            ('Konveyör #6', 'Taşıma', 'Transport'),
            ('Kompresör #7', 'Destek', 'Support'),
            ('Jeneratör #8', 'Destek', 'Support'),
            ('Pompa #9', 'Destek', 'Support'),
            ('Kırıcı #10', 'İşleme', 'Processing')
        ]
        
        for i, (name, type_tr, type_en) in enumerate(equipment_list, 1):
            zone = random.choice(self.zones)
            equipment = {
                'id': f'E{i:03d}',
                'name': name,
                'type': type_tr,
                'type_en': type_en,
                'zone_id': zone['id'],
                'zone_name': zone['name'],
                'location': {
                    'x': zone['x'] + random.uniform(-60, 60),
                    'y': zone['y'] + random.uniform(-60, 60),
                    'z': random.uniform(-30, -2)
                },
                'status': random.choice(['online', 'online', 'online', 'maintenance', 'offline']),
                'battery': random.randint(40, 100),
                'fuel': random.randint(20, 100),
                'signal': random.randint(75, 100),
                'health_score': random.randint(70, 100),
                'operator': random.choice([p['full_name'] for p in self.personnel[:5]]),
                'last_maintenance': '2024-12-01',
                'operating_hours': random.randint(500, 5000),
                'last_update': datetime.now()
            }
            self.equipment.append(equipment)
    
    def update_locations(self):
        """Konumları güncelle (simulasyon)"""
        # Personel konumlarını güncelle
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
                
                # Batarya düşür
                if random.random() < 0.05:
                    person['battery'] = max(0, person['battery'] - random.randint(1, 3))
                    if person['battery'] < 20:
                        self.battery_alert.emit({
                            'type': 'personnel',
                            'id': person['id'],
                            'name': person['full_name'],
                            'battery': person['battery']
                        })
                
                person['last_update'] = datetime.now()
                
                # Konum güncellemesi sinyali
                self.location_updated.emit({
                    'type': 'personnel',
                    'data': person
                })
        
        # Ekipman konumlarını güncelle
        for equip in self.equipment:
            if equip['status'] == 'online' and random.random() < 0.3:
                equip['location']['x'] += random.uniform(-3, 3)
                equip['location']['y'] += random.uniform(-3, 3)
                
                equip['location']['x'] = max(-500, min(500, equip['location']['x']))
                equip['location']['y'] = max(-400, min(400, equip['location']['y']))
                
                equip['zone_id'], equip['zone_name'] = self.determine_zone(equip['location'])
                
                # Yakıt ve batarya düşür
                if random.random() < 0.03:
                    equip['fuel'] = max(0, equip['fuel'] - random.randint(1, 2))
                    equip['battery'] = max(0, equip['battery'] - random.randint(1, 2))
                
                equip['last_update'] = datetime.now()
                
                self.location_updated.emit({
                    'type': 'equipment',
                    'data': equip
                })
    
    def determine_zone(self, location):
        """Koordinatlara göre bölge belirle"""
        x, y = location['x'], location['y']
        
        # En yakın bölgeyi bul
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
    
    def get_equipment(self):
        """Tüm ekipmanı al"""
        return self.equipment
    
    def get_zones(self):
        """Tüm bölgeleri al"""
        return self.zones
    
    def get_person_by_id(self, person_id):
        """ID'ye göre personel bul"""
        for person in self.personnel:
            if person['id'] == person_id:
                return person
        return None
    
    def get_equipment_by_id(self, equipment_id):
        """ID'ye göre ekipman bul"""
        for equip in self.equipment:
            if equip['id'] == equipment_id:
                return equip
        return None
    
    def trigger_emergency(self, entity_id, entity_type='personnel'):
        """Acil durum tetikle"""
        if entity_type == 'personnel':
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
        else:
            entity = self.get_equipment_by_id(entity_id)
            if entity:
                entity['status'] = 'emergency'
                self.emergency_signal.emit({
                    'type': 'equipment',
                    'id': entity_id,
                    'name': entity['name'],
                    'location': entity['location'],
                    'zone': entity['zone_name'],
                    'timestamp': datetime.now().isoformat()
                })
    
    def get_statistics(self):
        """İstatistikleri al"""
        active_personnel = sum(1 for p in self.personnel if p['status'] == 'active')
        on_break = sum(1 for p in self.personnel if p['status'] == 'break')
        emergency_count = sum(1 for p in self.personnel if p['status'] == 'emergency')
        
        online_equipment = sum(1 for e in self.equipment if e['status'] == 'online')
        maintenance_equipment = sum(1 for e in self.equipment if e['status'] == 'maintenance')
        offline_equipment = sum(1 for e in self.equipment if e['status'] == 'offline')
        
        avg_battery_personnel = sum(p['battery'] for p in self.personnel) / len(self.personnel) if self.personnel else 0
        avg_battery_equipment = sum(e['battery'] for e in self.equipment) / len(self.equipment) if self.equipment else 0
        
        low_battery_personnel = sum(1 for p in self.personnel if p['battery'] < 20)
        low_battery_equipment = sum(1 for e in self.equipment if e['battery'] < 20)
        
        return {
            'personnel': {
                'total': len(self.personnel),
                'active': active_personnel,
                'on_break': on_break,
                'emergency': emergency_count,
                'avg_battery': round(avg_battery_personnel, 1),
                'low_battery': low_battery_personnel
            },
            'equipment': {
                'total': len(self.equipment),
                'online': online_equipment,
                'maintenance': maintenance_equipment,
                'offline': offline_equipment,
                'avg_battery': round(avg_battery_equipment, 1),
                'low_battery': low_battery_equipment
            }
        }
