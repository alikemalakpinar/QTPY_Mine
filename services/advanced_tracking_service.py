"""Gelişmiş Tracking Service - Trilateration + Kalman Filter + TCP Integration"""
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import random
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from services.kalman_filter import KalmanFilter2D
from services.trilateration import (
    trilaterate_2d, trilaterate_3d, 
    calculate_distance, calculate_distance_3d,
    select_best_anchors, estimate_position_accuracy
)

class AdvancedTrackingService(QObject):
    """
    Enterprise-grade tracking service.
    
    Özellikler:
    - Trilateration (3+ anchor ile kesin konum)
    - Kalman Filtering (gürültü azaltma)
    - Moving Average Smoothing
    - Smart Anchor Selection
    - Hybrid Filtering
    - Position accuracy estimation
    """
    
    # Signals
    location_updated = pyqtSignal(dict)
    battery_alert = pyqtSignal(dict)
    emergency_signal = pyqtSignal(dict)
    position_calculated = pyqtSignal(dict)  # Raw + Filtered positions
    anchor_status_changed = pyqtSignal(dict)
    tag_status_changed = pyqtSignal(dict)
    
    def __init__(self, mode='hybrid'):
        """
        Args:
            mode: 'simulation', 'tcp', 'hybrid'
        """
        super().__init__()
        
        self.mode = mode  # simulation, tcp, hybrid
        self.anchors = []
        self.tags = []
        self.personnel = []
        self.zones = []
        
        # Tag tracking data
        self.tag_filters = {}  # tag_id -> KalmanFilter2D
        self.tag_raw_positions = {}  # tag_id -> [recent raw positions]
        self.tag_trails = {}  # tag_id -> [position history for visualization]
        self.tag_distances = {}  # tag_id -> {anchor_id: distance}
        self.snap_tags = {}  # anchor_id -> [tag_ids] (snapped within 45cm)
        
        # Configuration
        self.smoothing_factor = 0.3
        self.position_history_size = 5
        self.trail_max_length = 50
        self.snap_distance = 0.45  # 45cm
        self.min_position_change = 0.20  # 20cm - prevent jitter
        
        self.init_anchors()
        self.init_zones()
        self.init_personnel()
        
        # Update timer (simülasyon için)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_simulation)
        if self.mode in ['simulation', 'hybrid']:
            self.update_timer.start(2000)
    
    def init_anchors(self):
        """6 Anchor'ı başlat (mevcut sistem)"""
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
    
    def init_zones(self):
        """Bölgeleri başlat"""
        self.zones = [
            {'id': 'ZONE_A', 'name': 'Ana Şaft', 'color': '#00D4FF', 'x': 0, 'y': 0},
            {'id': 'ZONE_B', 'name': 'Sektör A', 'color': '#00FF88', 'x': -350, 'y': -200},
            {'id': 'ZONE_C', 'name': 'Sektör B', 'color': '#FFB800', 'x': 350, 'y': -200},
            {'id': 'ZONE_D', 'name': 'Sektör C', 'color': '#9966FF', 'x': 0, 'y': 280},
            {'id': 'ZONE_E', 'name': 'İşleme', 'color': '#FF3366', 'x': -250, 'y': 350},
            {'id': 'ZONE_F', 'name': 'Atölye', 'color': '#00CCFF', 'x': 250, 'y': 350}
        ]
    
    def init_personnel(self):
        """15 Personel başlat"""
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
            
            # Başlangıç konumu
            initial_x = zone['x'] + random.uniform(-50, 50)
            initial_y = zone['y'] + random.uniform(-50, 50)
            initial_z = random.uniform(-50, -5)
            
            # Personel
            person = {
                'id': person_id,
                'first_name': first_name,
                'last_name': last_name,
                'full_name': f'{first_name} {last_name}',
                'position': position,
                'zone_id': zone['id'],
                'zone_name': zone['name'],
                'location': {'x': initial_x, 'y': initial_y, 'z': initial_z},
                'raw_location': {'x': initial_x, 'y': initial_y, 'z': initial_z},
                'filtered_location': {'x': initial_x, 'y': initial_y, 'z': initial_z},
                'position_accuracy': 0.0,
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
            
            # Tag
            tag = {
                'id': tag_id,
                'person_id': person_id,
                'person_name': f'{first_name} {last_name}',
                'battery': person['battery'],
                'signal_strength': person['signal'],
                'firmware_version': random.choice(['1.8.2', '1.9.0', '2.0.0']),
                'status': 'active' if person['status'] == 'active' else 'inactive',
                'last_seen': datetime.now(),
                'type': 'tag'
            }
            self.tags.append(tag)
            
            # Kalman filter başlat
            self.tag_filters[tag_id] = KalmanFilter2D(
                process_variance=0.005,
                measurement_variance=0.5,
                initial_value=(initial_x, initial_y)
            )
            
            # Boş geçmiş
            self.tag_raw_positions[tag_id] = []
            self.tag_trails[tag_id] = []
    
    def update_simulation(self):
        """Simülasyon - konumları güncelle"""
        if self.mode not in ['simulation', 'hybrid']:
            return
        
        for person in self.personnel:
            if person['status'] != 'active':
                continue
            
            if random.random() < 0.4:
                # Simüle edilmiş hareket
                person['location']['x'] += random.uniform(-5, 5)
                person['location']['y'] += random.uniform(-5, 5)
                person['location']['z'] += random.uniform(-1, 1)
                
                # Sınırlar
                person['location']['x'] = max(-500, min(500, person['location']['x']))
                person['location']['y'] = max(-400, min(400, person['location']['y']))
                person['location']['z'] = max(-100, min(-5, person['location']['z']))
                
                # Simüle edilmiş anchor mesafeleri oluştur
                tag_id = person['tag_id']
                self.simulate_anchor_distances(tag_id, person['location'])
                
                # Trilateration ile konum hesapla
                self.calculate_tag_position(tag_id)
                
                # Kalp atışı
                person['heart_rate'] = max(60, min(110, person['heart_rate'] + random.randint(-3, 3)))
                
                # Batarya
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
                
                # Signal emit
                self.location_updated.emit({'type': 'personnel', 'data': person})
    
    def simulate_anchor_distances(self, tag_id: str, location: dict):
        """Simülasyon için anchor mesafelerini hesapla"""
        if tag_id not in self.tag_distances:
            self.tag_distances[tag_id] = {}
        
        tag_pos = (location['x'], location['y'], location['z'])
        
        for anchor in self.anchors:
            if anchor['status'] != 'online':
                continue
            
            anchor_pos = (anchor['x'], anchor['y'], anchor['z'])
            
            # Gerçek mesafe
            real_distance = calculate_distance_3d(tag_pos, anchor_pos)
            
            # Gürültü ekle (±0.1m - 0.5m)
            noise = random.uniform(-0.5, 0.5)
            measured_distance = max(0, real_distance + noise)
            
            # Kaydet
            self.tag_distances[tag_id][anchor['id']] = measured_distance
    
    def process_tcp_data(self, data: dict):
        """TCP'den gelen gerçek veriyi işle"""
        if 'measurements' not in data:
            return
        
        anchor_id = data.get('anchor_id')
        if not anchor_id:
            return
        
        for measurement in data['measurements']:
            tag_id = measurement.get('tag_id')
            
            # Mesafe
            distance = None
            if 'distance(m)' in measurement and isinstance(measurement['distance(m)'], dict):
                distance = measurement['distance(m)'].get('distance')
            else:
                distance = measurement.get('distance') or measurement.get('distance_m')
            
            if distance is None or tag_id is None:
                continue
            
            # Filtrele (0-20m arası)
            distance = float(distance)
            if distance < 0 or distance > 20:
                continue
            
            # Kaydet
            if tag_id not in self.tag_distances:
                self.tag_distances[tag_id] = {}
            
            self.tag_distances[tag_id][anchor_id] = distance
            
            # Tag yoksa oluştur (dinamik)
            if not any(t['id'] == tag_id for t in self.tags):
                self.create_dynamic_tag(tag_id)
            
            # Konum hesapla
            self.calculate_tag_position(tag_id)
    
    def calculate_tag_position(self, tag_id: str):
        """Trilateration + Kalman filter ile konum hesapla"""
        if tag_id not in self.tag_distances:
            return
        
        # Snap kontrolü - anchor'a çok yakınsa snap et
        for anchor_id, distance in self.tag_distances[tag_id].items():
            if distance <= self.snap_distance:
                self.snap_tag_to_anchor(tag_id, anchor_id)
                return
        
        # Snap'ten çıkar
        self.unsnap_tag(tag_id)
        
        # En az 3 anchor gerekli
        if len(self.tag_distances[tag_id]) < 3:
            return
        
        # Anchor ve mesafe listelerini hazırla
        anchor_data = []
        for anchor_id, distance in self.tag_distances[tag_id].items():
            anchor = next((a for a in self.anchors if a['id'] == anchor_id), None)
            if anchor and anchor['status'] == 'online':
                anchor_data.append({
                    'id': anchor_id,
                    'position': (anchor['x'], anchor['y'], anchor['z']),
                    'distance': distance
                })
        
        if len(anchor_data) < 3:
            return
        
        # Mevcut konumu al (varsa)
        person = next((p for p in self.personnel if p['tag_id'] == tag_id), None)
        current_position = None
        if person:
            current_position = (
                person['location']['x'],
                person['location']['y'],
                person['location']['z']
            )
        
        # Smart anchor selection (en iyi 3-4 anchor)
        if current_position and len(anchor_data) > 3:
            anchor_data = select_best_anchors(current_position, anchor_data)[:3]
        else:
            anchor_data = anchor_data[:3]
        
        # Trilateration
        anchors_2d = [(a['position'][0], a['position'][1]) for a in anchor_data]
        distances = [a['distance'] for a in anchor_data]
        
        raw_position = trilaterate_2d(anchors_2d, distances)
        
        if not raw_position:
            return
        
        # Z koordinatını anchor ortalamasından tahmin et
        avg_z = sum(a['position'][2] for a in anchor_data) / len(anchor_data)
        raw_position_3d = (raw_position[0], raw_position[1], avg_z)
        
        # Kalman filter
        if tag_id not in self.tag_filters:
            self.tag_filters[tag_id] = KalmanFilter2D(
                process_variance=0.005,
                measurement_variance=0.5,
                initial_value=raw_position
            )
        
        kalman_filtered = self.tag_filters[tag_id].update(raw_position)
        
        # Moving average smoothing
        if tag_id not in self.tag_raw_positions:
            self.tag_raw_positions[tag_id] = []
        
        self.tag_raw_positions[tag_id].append(raw_position)
        if len(self.tag_raw_positions[tag_id]) > self.position_history_size:
            self.tag_raw_positions[tag_id].pop(0)
        
        smoothed_position = self.apply_moving_average(tag_id)
        
        # Hybrid (Kalman + Moving Average)
        if smoothed_position:
            final_position = (
                0.6 * kalman_filtered[0] + 0.4 * smoothed_position[0],
                0.6 * kalman_filtered[1] + 0.4 * smoothed_position[1]
            )
        else:
            final_position = kalman_filtered
        
        final_position_3d = (final_position[0], final_position[1], avg_z)
        
        # Jitter önleme (20cm'den az değişim varsa güncelleme)
        if person and current_position:
            distance_change = calculate_distance_3d(final_position_3d, current_position)
            if distance_change < self.min_position_change:
                return
        
        # Accuracy estimation
        accuracy = estimate_position_accuracy(
            anchors_2d, distances, final_position
        )
        
        # Personeli güncelle
        if person:
            # Trail ekle
            if tag_id not in self.tag_trails:
                self.tag_trails[tag_id] = []
            
            self.tag_trails[tag_id].append({
                'x': person['location']['x'],
                'y': person['location']['y'],
                'z': person['location']['z'],
                'timestamp': datetime.now()
            })
            
            if len(self.tag_trails[tag_id]) > self.trail_max_length:
                self.tag_trails[tag_id].pop(0)
            
            # Konumu güncelle
            person['raw_location'] = {
                'x': raw_position_3d[0],
                'y': raw_position_3d[1],
                'z': raw_position_3d[2]
            }
            person['filtered_location'] = {
                'x': final_position_3d[0],
                'y': final_position_3d[1],
                'z': final_position_3d[2]
            }
            person['location'] = {
                'x': final_position_3d[0],
                'y': final_position_3d[1],
                'z': final_position_3d[2]
            }
            person['position_accuracy'] = accuracy
            
            # Bölge güncelle
            person['zone_id'], person['zone_name'] = self.determine_zone(person['location'])
            
            # Signal emit
            self.position_calculated.emit({
                'tag_id': tag_id,
                'person_id': person['id'],
                'raw': raw_position_3d,
                'kalman': (kalman_filtered[0], kalman_filtered[1], avg_z),
                'smoothed': (smoothed_position[0], smoothed_position[1], avg_z) if smoothed_position else None,
                'final': final_position_3d,
                'accuracy': accuracy,
                'anchors_used': [a['id'] for a in anchor_data]
            })
    
    def apply_moving_average(self, tag_id: str) -> Optional[Tuple[float, float]]:
        """Moving average smoothing"""
        if tag_id not in self.tag_raw_positions or not self.tag_raw_positions[tag_id]:
            return None
        
        positions = self.tag_raw_positions[tag_id]
        
        if len(positions) == 0:
            return None
        
        avg_x = sum(p[0] for p in positions) / len(positions)
        avg_y = sum(p[1] for p in positions) / len(positions)
        
        return (avg_x, avg_y)
    
    def snap_tag_to_anchor(self, tag_id: str, anchor_id: str):
        """Tag'ı anchor'a snap et (45cm içinde)"""
        anchor = next((a for a in self.anchors if a['id'] == anchor_id), None)
        if not anchor:
            return
        
        person = next((p for p in self.personnel if p['tag_id'] == tag_id), None)
        if not person:
            return
        
        # Snap listesine ekle
        if anchor_id not in self.snap_tags:
            self.snap_tags[anchor_id] = []
        if tag_id not in self.snap_tags[anchor_id]:
            self.snap_tags[anchor_id].append(tag_id)
        
        # Konumu anchor'a ayarla (birden fazla tag varsa offset ekle)
        num_tags = len(self.snap_tags[anchor_id])
        index = self.snap_tags[anchor_id].index(tag_id)
        
        if num_tags == 1:
            person['location'] = {'x': anchor['x'], 'y': anchor['y'], 'z': anchor['z']}
        else:
            # Dairesel dağılım
            radius = 0.2  # 20cm
            angle = (2 * math.pi * index) / num_tags
            offset_x = radius * math.cos(angle)
            offset_y = radius * math.sin(angle)
            
            person['location'] = {
                'x': anchor['x'] + offset_x,
                'y': anchor['y'] + offset_y,
                'z': anchor['z']
            }
        
        person['position_accuracy'] = 0.1  # Çok doğru (snap)
    
    def unsnap_tag(self, tag_id: str):
        """Tag'ı snap'ten çıkar"""
        for anchor_id in list(self.snap_tags.keys()):
            if tag_id in self.snap_tags[anchor_id]:
                self.snap_tags[anchor_id].remove(tag_id)
                if not self.snap_tags[anchor_id]:
                    del self.snap_tags[anchor_id]
    
    def create_dynamic_tag(self, tag_id: str):
        """Dinamik olarak yeni tag oluştur (TCP'den gelen veriler için)"""
        # Tag zaten varsa çık
        if any(t['id'] == tag_id for t in self.tags):
            return
        
        # Yeni tag
        tag = {
            'id': tag_id,
            'person_id': None,
            'person_name': f'Unknown-{tag_id}',
            'battery': 100,
            'signal_strength': 90,
            'firmware_version': '2.0.0',
            'status': 'active',
            'last_seen': datetime.now(),
            'type': 'tag'
        }
        self.tags.append(tag)
        
        # Dummy personel (opsiyonel - UI için)
        # Veya sadece tag olarak bırakabilirsin
    
    def determine_zone(self, location: dict) -> Tuple[str, str]:
        """Koordinatlara göre bölge belirle"""
        x, y = location['x'], location['y']
        
        min_dist = float('inf')
        closest_zone = self.zones[0]
        
        for zone in self.zones:
            dist = math.sqrt((x - zone['x'])**2 + (y - zone['y'])**2)
            if dist < min_dist:
                min_dist = dist
                closest_zone = zone
        
        return closest_zone['id'], closest_zone['name']
    
    # Public API methods
    def get_personnel(self):
        """Tüm personeli al"""
        return self.personnel
    
    def get_anchors(self):
        """Tüm anchor'ları al"""
        return self.anchors
    
    def get_gateways(self):
        """Backward compatibility"""
        return self.anchors
    
    def get_tags(self):
        """Tüm tag'leri al"""
        return self.tags
    
    def get_zones(self):
        """Tüm bölgeleri al"""
        return self.zones
    
    def get_tag_trail(self, tag_id: str) -> List[dict]:
        """Tag'ın hareket geçmişini al"""
        return self.tag_trails.get(tag_id, [])
    
    def get_tag_distances(self, tag_id: str) -> Dict[str, float]:
        """Tag için anchor mesafelerini al"""
        return self.tag_distances.get(tag_id, {})
    
    def get_statistics(self):
        """İstatistikleri al"""
        active_personnel = sum(1 for p in self.personnel if p['status'] == 'active')
        on_break = sum(1 for p in self.personnel if p['status'] == 'break')
        emergency_count = sum(1 for p in self.personnel if p['status'] == 'emergency')
        
        avg_battery_personnel = sum(p['battery'] for p in self.personnel) / len(self.personnel) if self.personnel else 0
        low_battery_personnel = sum(1 for p in self.personnel if p['battery'] < 20)
        
        online_anchors = sum(1 for a in self.anchors if a['status'] == 'online')
        avg_battery_anchors = sum(a['battery'] for a in self.anchors) / len(self.anchors) if self.anchors else 0
        low_battery_anchors = sum(1 for a in self.anchors if a['battery'] < 70)
        
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
            'gateways': {
                'total': len(self.anchors),
                'online': online_anchors,
                'offline': len(self.anchors) - online_anchors
            }
        }
    
    def trigger_emergency(self, entity_id: str, entity_type='personnel'):
        """Acil durum tetikle"""
        entity = next((p for p in self.personnel if p['id'] == entity_id), None)
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
    
    def set_mode(self, mode: str):
        """Tracking modunu değiştir"""
        self.mode = mode
        
        if mode in ['simulation', 'hybrid']:
            if not self.update_timer.isActive():
                self.update_timer.start(2000)
        else:
            if self.update_timer.isActive():
                self.update_timer.stop()
