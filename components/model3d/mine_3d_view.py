"""3D Maden Görselleştirme Component'i"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import json

# WebEngine kontrolü
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
    BaseClass = QWebEngineView
except ImportError:
    WEBENGINE_AVAILABLE = False
    BaseClass = QWidget

class Mine3DView(BaseClass):
    """3D maden harita görünümü - Three.js ile"""
    
    def __init__(self, tracking_service):
        super().__init__()
        self.tracking = tracking_service
        self.setMinimumSize(800, 600)
        
        if not WEBENGINE_AVAILABLE:
            # WebEngine yoksa basit placeholder göster
            self.show_placeholder()
        else:
            # 3D sahneyi yükle
            self.load_3d_scene()
            
            # Tracking güncellemelerini dinle
            self.tracking.location_updated.connect(self.update_position)
            
            # İlk yüklemede tüm konumları gönder
            QTimer.singleShot(2000, self.load_all_positions)
    
    def show_placeholder(self):
        """WebEngine yoksa placeholder göster"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("🗺️ 3D Harita\n\n⚠️ QtWebEngine bulunamadı!\n\nPip ile yükleyin:\npip install PyQt6-WebEngine")
        label.setStyleSheet("""
            QLabel {
                color: #FFB800;
                font-size: 18px;
                padding: 40px;
                background: #1A1A1A;
                border: 2px dashed #FFB800;
                border-radius: 12px;
            }
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
    
    def load_3d_scene(self):
        """Three.js 3D sahnesini yükle"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>MineTracker 3D</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #0F0F0F; overflow: hidden; }
        #container { width: 100%; height: 100%; }
        #info {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            font-family: -apple-system, sans-serif;
            background: rgba(0, 0, 0, 0.9);
            padding: 20px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 212, 255, 0.3);
            min-width: 250px;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }
        .stat-label {
            color: #B0B0B0;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat-value {
            color: #00D4FF;
            font-size: 18px;
            font-weight: 700;
        }
        .controls {
            position: absolute;
            bottom: 20px;
            left: 20px;
            color: #B0B0B0;
            font-size: 11px;
            background: rgba(0, 0, 0, 0.8);
            padding: 12px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            color: white;
            font-family: -apple-system, sans-serif;
            font-size: 12px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
        }
        .legend-color {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="info">
        <h3 style="margin: 0 0 15px 0; color: #00D4FF;">⛏️ MineTracker 3D</h3>
        <div class="stat">
            <span class="stat-label">Personel</span>
            <span class="stat-value" id="personnel-count">0</span>
        </div>
        <div class="stat">
            <span class="stat-label">Ekipman</span>
            <span class="stat-value" id="equipment-count">0</span>
        </div>
        <div class="stat">
            <span class="stat-label">Aktif Bölge</span>
            <span class="stat-value" id="zones-count">6</span>
        </div>
    </div>
    <div class="legend">
        <div style="font-weight: bold; margin-bottom: 10px; color: #00D4FF;">📍 Semboller</div>
        <div class="legend-item">
            <div class="legend-color" style="background: #00FF88;"></div>
            <span>👤 Personel</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #FFB800;"></div>
            <span>🚜 Ekipman</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #FF3366;"></div>
            <span>⚠️ Acil Durum</span>
        </div>
    </div>
    <div class="controls">
        🖊️ Fare: Döndür | Kaydırma: Yakınlaştır | Ok Tuşları: Hareket
    </div>

    <script>
        // Sahne ayarları
        const scene = new THREE.Scene();
        scene.fog = new THREE.Fog(0x0F0F0F, 200, 1500);
        
        const camera = new THREE.PerspectiveCamera(
            75, window.innerWidth / window.innerHeight, 0.1, 2000
        );
        camera.position.set(400, 500, 600);
        camera.lookAt(0, 0, 0);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x0F0F0F);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Işıklandırma
        const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
        directionalLight.position.set(200, 400, 200);
        directionalLight.castShadow = true;
        directionalLight.shadow.camera.left = -600;
        directionalLight.shadow.camera.right = 600;
        directionalLight.shadow.camera.top = 600;
        directionalLight.shadow.camera.bottom = -600;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        scene.add(directionalLight);
        
        // Nokta ışıklar (bölge amaçlı)
        const colors = [0x00D4FF, 0x00FF88, 0xFFB800, 0xFF3366, 0x9966FF, 0x00CCFF];
        colors.forEach((color, i) => {
            const light = new THREE.PointLight(color, 0.5, 150);
            const angle = (i / colors.length) * Math.PI * 2;
            light.position.set(
                Math.cos(angle) * 250,
                50,
                Math.sin(angle) * 250
            );
            scene.add(light);
        });
        
        // Maden zemin
        const gridHelper = new THREE.GridHelper(1200, 60, 0x00D4FF, 0x1A1A1A);
        scene.add(gridHelper);
        
        const floorGeometry = new THREE.PlaneGeometry(1200, 1000);
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x1A1A1A,
            roughness: 0.8,
            metalness: 0.2
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.position.y = -2;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Maden tünelleri
        const tunnelMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2A2A2A,
            transparent: true,
            opacity: 0.7,
            roughness: 0.9
        });
        
        // Ana tünel
        const mainTunnel = new THREE.Mesh(
            new THREE.BoxGeometry(700, 60, 40),
            tunnelMaterial
        );
        mainTunnel.position.set(0, 30, 0);
        mainTunnel.castShadow = true;
        scene.add(mainTunnel);
        
        // Yan tüneller
        [-250, 0, 250].forEach(x => {
            const tunnel = new THREE.Mesh(
                new THREE.BoxGeometry(40, 60, 500),
                tunnelMaterial
            );
            tunnel.position.set(x, 30, 0);
            tunnel.castShadow = true;
            scene.add(tunnel);
        });
        
        // Bölge işaretleri
        const zones = [
            { name: 'Ana Şaft', x: 0, z: 0, color: 0x00D4FF },
            { name: 'Sektör A', x: -300, z: -150, color: 0x00FF88 },
            { name: 'Sektör B', x: 300, z: -150, color: 0xFFB800 },
            { name: 'Sektör C', x: 0, z: 200, color: 0xFF3366 },
            { name: 'İşleme', x: -200, z: 300, color: 0x9966FF },
            { name: 'Atölye', x: 200, z: 300, color: 0x00CCFF }
        ];
        
        zones.forEach(zone => {
            // Platform
            const platform = new THREE.Mesh(
                new THREE.CylinderGeometry(45, 45, 4, 32),
                new THREE.MeshStandardMaterial({ 
                    color: zone.color,
                    emissive: zone.color,
                    emissiveIntensity: 0.3,
                    roughness: 0.5
                })
            );
            platform.position.set(zone.x, 2, zone.z);
            platform.castShadow = true;
            scene.add(platform);
            
            // Parlayan halka
            const ring = new THREE.Mesh(
                new THREE.RingGeometry(40, 50, 32),
                new THREE.MeshBasicMaterial({ 
                    color: zone.color,
                    transparent: true,
                    opacity: 0.4,
                    side: THREE.DoubleSide
                })
            );
            ring.position.set(zone.x, 3, zone.z);
            ring.rotation.x = -Math.PI / 2;
            scene.add(ring);
        });
        
        // Takip nesneleri
        const entities = new Map();
        
        // Cihaz markeri oluştur
        function createMarker(type, color) {
            const group = new THREE.Group();
            
            const geometry = type === 'personnel' 
                ? new THREE.SphereGeometry(6, 16, 16)
                : new THREE.BoxGeometry(12, 12, 12);
            
            const material = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.4,
                roughness: 0.3,
                metalness: 0.5
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.castShadow = true;
            group.add(mesh);
            
            // Parlama efekti
            const glowGeom = type === 'personnel'
                ? new THREE.SphereGeometry(9, 16, 16)
                : new THREE.BoxGeometry(16, 16, 16);
            
            const glowMat = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.3
            });
            
            const glow = new THREE.Mesh(glowGeom, glowMat);
            group.add(glow);
            
            return group;
        }
        
        // Konum güncelle
        window.updateEntity = function(data) {
            const { id, type, location, battery, status } = data;
            
            if (!entities.has(id)) {
                let color;
                if (status === 'emergency') {
                    color = 0xFF3366;
                } else if (type === 'personnel') {
                    color = 0x00FF88;
                } else {
                    color = 0xFFB800;
                }
                
                const marker = createMarker(type, color);
                entities.set(id, marker);
                scene.add(marker);
            }
            
            const marker = entities.get(id);
            
            // Yumuşak geçiş
            marker.position.x = location.x;
            marker.position.y = Math.abs(location.z) + 15;
            marker.position.z = location.y;
            
            // Durum rengini güncelle
            if (status === 'emergency') {
                marker.children[0].material.color.setHex(0xFF3366);
                marker.children[0].material.emissive.setHex(0xFF3366);
                marker.children[0].material.emissiveIntensity = 0.8;
            }
            
            // Batarya düşükse titret
            if (battery < 20) {
                marker.position.y += Math.sin(Date.now() * 0.01) * 2;
            }
        };
        
        // Sayıları güncelle
        window.updateCounts = function(personnel, equipment) {
            document.getElementById('personnel-count').textContent = personnel;
            document.getElementById('equipment-count').textContent = equipment;
        };
        
        // Kamera kontrolü
        let mouseX = 0, mouseY = 0;
        let targetRotationX = 0, targetRotationY = 0;
        let isMouseDown = false;
        
        document.addEventListener('mousedown', () => isMouseDown = true);
        document.addEventListener('mouseup', () => isMouseDown = false);
        
        document.addEventListener('mousemove', (event) => {
            if (isMouseDown) {
                mouseX = (event.clientX - window.innerWidth / 2) * 0.001;
                mouseY = (event.clientY - window.innerHeight / 2) * 0.001;
                targetRotationY += mouseX;
                targetRotationX += mouseY;
                targetRotationX = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, targetRotationX));
            }
        });
        
        // Zoom
        document.addEventListener('wheel', (event) => {
            const distance = camera.position.length();
            const newDistance = distance + event.deltaY * 0.5;
            const clampedDistance = Math.max(300, Math.min(1200, newDistance));
            const scale = clampedDistance / distance;
            camera.position.multiplyScalar(scale);
        });
        
        // Animasyon döngüsü
        function animate() {
            requestAnimationFrame(animate);
            
            // Kamera döndürme
            const distance = 700;
            camera.position.x = Math.sin(targetRotationY) * distance * Math.cos(targetRotationX);
            camera.position.z = Math.cos(targetRotationY) * distance * Math.cos(targetRotationX);
            camera.position.y = 500 + Math.sin(targetRotationX) * 300;
            camera.lookAt(0, 0, 0);
            
            // Halka animasyonu
            const time = Date.now() * 0.001;
            scene.children.forEach(child => {
                if (child.geometry && child.geometry.type === 'RingGeometry') {
                    child.material.opacity = 0.3 + Math.sin(time * 2) * 0.15;
                }
            });
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Pencere yeniden boyutlandırma
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
        """
        self.setHtml(html_content)
    
    def update_position(self, data):
        """Konum güncellemesi"""
        if not WEBENGINE_AVAILABLE:
            return  # WebEngine yoksa hiçbir şey yapma
            
        entity_type = data['type']
        entity_data = data['data']
        
        update_info = {
            'id': entity_data['id'],
            'type': entity_type,
            'location': entity_data['location'],
            'battery': entity_data['battery'],
            'status': entity_data.get('status', 'active')
        }
        
        js_code = f"window.updateEntity({json.dumps(update_info)});"
        self.page().runJavaScript(js_code)
    
    def load_all_positions(self):
        """Tüm konumları yükle"""
        if not WEBENGINE_AVAILABLE:
            return  # WebEngine yoksa hiçbir şey yapma
            
        # Personel
        for person in self.tracking.get_personnel():
            self.update_position({'type': 'personnel', 'data': person})
        
        # Ekipman
        for equipment in self.tracking.get_equipment():
            self.update_position({'type': 'equipment', 'data': equipment})
        
        # Sayıları güncelle
        stats = self.tracking.get_statistics()
        js_code = f"window.updateCounts({stats['personnel']['total']}, {stats['equipment']['total']});"
        self.page().runJavaScript(js_code)
