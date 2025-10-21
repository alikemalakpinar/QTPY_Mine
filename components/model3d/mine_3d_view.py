"""3D Yeraltı Personel Takip Sistemi - Gateway & Tag Tabanlı"""
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
    """Gateway tabanlı personel takip sistemi - 3D görselleştirme"""
    
    def __init__(self, tracking_service):
        super().__init__()
        self.tracking = tracking_service
        self.setMinimumSize(800, 600)
        
        if not WEBENGINE_AVAILABLE:
            self.show_placeholder()
        else:
            self.load_3d_scene()
            self.tracking.location_updated.connect(self.update_position)
            QTimer.singleShot(2000, self.load_all_positions)
    
    def show_placeholder(self):
        """WebEngine yoksa placeholder"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("🗺️ 3D Harita\n\n⚠️ QtWebEngine gerekli!\n\npip install PyQt6-WebEngine")
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
        """Gateway & Tag tabanlı 3D sahne"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MineTracker - Gateway & Tag Tracking</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #0a0a0f;
            overflow: hidden; 
            font-family: 'Segoe UI', -apple-system, sans-serif;
        }
        #container { width: 100vw; height: 100vh; }
        
        /* Bilgi Paneli - Minimalist */
        #info-panel {
            position: absolute;
            top: 25px;
            left: 25px;
            background: rgba(15, 15, 20, 0.95);
            padding: 25px;
            border-radius: 20px;
            border: 2px solid rgba(0, 212, 255, 0.3);
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            min-width: 300px;
        }
        
        .panel-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .panel-icon {
            font-size: 28px;
        }
        
        .panel-title {
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 700;
        }
        
        .panel-subtitle {
            color: #B0B0B0;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            margin: 10px 0;
            border-left: 3px solid;
            transition: all 0.3s;
        }
        
        .stat-card:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(3px);
        }
        
        .stat-card.personnel { border-left-color: #00FF88; }
        .stat-card.gateway { border-left-color: #00D4FF; }
        .stat-card.zones { border-left-color: #9966FF; }
        
        .stat-label {
            color: #909090;
            font-size: 12px;
            margin-bottom: 5px;
        }
        
        .stat-value {
            color: #FFFFFF;
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: baseline;
            gap: 8px;
        }
        
        .stat-unit {
            font-size: 14px;
            color: #707070;
            font-weight: 400;
        }
        
        /* Status Indicator */
        .status-online {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #00FF88;
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-right: 8px;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; box-shadow: 0 0 10px #00FF88; }
            50% { opacity: 0.5; box-shadow: 0 0 5px #00FF88; }
        }
        
        /* Lejant - Temiz */
        #legend {
            position: absolute;
            top: 25px;
            right: 25px;
            background: rgba(15, 15, 20, 0.95);
            padding: 20px;
            border-radius: 16px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }
        
        .legend-title {
            color: #FFFFFF;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 12px 0;
            gap: 12px;
        }
        
        .legend-icon {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            box-shadow: 0 0 15px currentColor;
            border: 2px solid currentColor;
        }
        
        .legend-text {
            color: #E0E0E0;
            font-size: 13px;
            font-weight: 500;
        }
        
        /* Kontroller */
        #controls {
            position: absolute;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 15, 20, 0.95);
            padding: 15px 30px;
            border-radius: 30px;
            border: 2px solid rgba(0, 212, 255, 0.2);
            backdrop-filter: blur(20px);
            display: flex;
            gap: 30px;
        }
        
        .control-item {
            color: #909090;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .control-key {
            background: rgba(255, 255, 255, 0.1);
            color: #00D4FF;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 11px;
        }
        
        /* Gateway Status - Sağ Alt */
        #gateway-status {
            position: absolute;
            bottom: 25px;
            right: 25px;
            background: rgba(15, 15, 20, 0.95);
            padding: 15px 20px;
            border-radius: 12px;
            border: 2px solid rgba(0, 212, 255, 0.3);
            backdrop-filter: blur(20px);
        }
        
        .gateway-title {
            color: #00D4FF;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .gateway-list {
            display: flex;
            gap: 10px;
        }
        
        .gateway-indicator {
            width: 10px;
            height: 10px;
            background: #00FF88;
            border-radius: 50%;
            box-shadow: 0 0 10px #00FF88;
        }
        
        /* Yükleme */
        #loading {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0a0a0f;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            transition: opacity 0.5s;
        }
        
        #loading.hidden {
            opacity: 0;
            pointer-events: none;
        }
        
        .loader {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(0, 212, 255, 0.2);
            border-top: 3px solid #00D4FF;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: #00D4FF;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <!-- Yükleme -->
    <div id="loading">
        <div class="loader"></div>
        <div class="loading-text">⛏️ Sistem başlatılıyor...</div>
    </div>

    <!-- 3D Container -->
    <div id="container"></div>
    
    <!-- Bilgi Paneli -->
    <div id="info-panel">
        <div class="panel-header">
            <span class="panel-icon">⛏️</span>
            <div>
                <div class="panel-title">MineTracker</div>
                <div class="panel-subtitle">
                    <span class="status-online"></span>Sistem Aktif
                </div>
            </div>
        </div>
        
        <div class="stat-card personnel">
            <div class="stat-label">👷 PERSONEL</div>
            <div class="stat-value">
                <span id="personnel-count">0</span>
                <span class="stat-unit">kişi</span>
            </div>
        </div>
        
        <div class="stat-card gateway">
            <div class="stat-label">📡 GATEWAY</div>
            <div class="stat-value">
                <span id="gateway-count">6</span>
                <span class="stat-unit">aktif</span>
            </div>
        </div>
        
        <div class="stat-card zones">
            <div class="stat-label">📍 BÖLGE</div>
            <div class="stat-value">
                <span id="zones-count">6</span>
                <span class="stat-unit">alan</span>
            </div>
        </div>
    </div>
    
    <!-- Lejant -->
    <div id="legend">
        <div class="legend-title">
            <span>📍</span>
            <span>Göstergeler</span>
        </div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #00FF88; color: #00FF88;"></div>
            <span class="legend-text">Personel Tag</span>
        </div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #00D4FF; color: #00D4FF;"></div>
            <span class="legend-text">Gateway</span>
        </div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #FF3366; color: #FF3366;"></div>
            <span class="legend-text">Acil Durum</span>
        </div>
    </div>
    
    <!-- Kontroller -->
    <div id="controls">
        <div class="control-item">
            <span class="control-key">Fare</span>
            <span>Döndür</span>
        </div>
        <div class="control-item">
            <span class="control-key">Scroll</span>
            <span>Zoom</span>
        </div>
        <div class="control-item">
            <span class="control-key">WASD</span>
            <span>Hareket</span>
        </div>
    </div>
    
    <!-- Gateway Status -->
    <div id="gateway-status">
        <div class="gateway-title">📡 GATEWAY STATUS</div>
        <div class="gateway-list" id="gateway-indicators"></div>
    </div>

    <script>
        // ============================================
        // SAHNE - MİNİMALİST & PROFESYONELİ
        // ============================================
        
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0f);
        scene.fog = new THREE.FogExp2(0x0a0a0f, 0.0006);
        
        // Kamera
        const camera = new THREE.PerspectiveCamera(
            65, 
            window.innerWidth / window.innerHeight, 
            1, 
            3000
        );
        camera.position.set(400, 350, 600);
        camera.lookAt(0, 0, 0);
        
        // Renderer - Yüksek Kalite
        const renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('container').appendChild(renderer.domElement);
        
        // ============================================
        // IŞIKLANDIRMA - PROFESYONEL
        // ============================================
        
        // Ambient
        const ambientLight = new THREE.AmbientLight(0x3a3a4a, 0.5);
        scene.add(ambientLight);
        
        // Ana ışık
        const mainLight = new THREE.DirectionalLight(0xffffff, 1.0);
        mainLight.position.set(200, 500, 200);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.left = -600;
        mainLight.shadow.camera.right = 600;
        mainLight.shadow.camera.top = 600;
        mainLight.shadow.camera.bottom = -600;
        scene.add(mainLight);
        
        // ============================================
        // MADEN ZEMİNİ - TEMİZ
        // ============================================
        
        const floorGeometry = new THREE.PlaneGeometry(1600, 1400, 80, 80);
        const vertices = floorGeometry.attributes.position.array;
        
        // Hafif pürüz
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i + 2] = Math.random() * 3;
        }
        floorGeometry.attributes.position.needsUpdate = true;
        floorGeometry.computeVertexNormals();
        
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2a2a30,
            roughness: 0.9,
            metalness: 0.1
        });
        
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Grid - İnce çizgiler
        const gridHelper = new THREE.GridHelper(1600, 40, 0x3a3a4a, 0x2a2a30);
        gridHelper.position.y = 0.1;
        scene.add(gridHelper);
        
        // ============================================
        // MADEN BÖLGE PLATFORMLARI - GATEWAY'LER
        // ============================================
        
        const zones = [
            { name: 'Ana Şaft', x: 0, z: 0, color: 0x00D4FF },
            { name: 'Sektör A', x: -350, z: -200, color: 0x00FF88 },
            { name: 'Sektör B', x: 350, z: -200, color: 0xFFB800 },
            { name: 'Sektör C', x: 0, z: 280, color: 0x9966FF },
            { name: 'İşleme', x: -250, z: 350, color: 0xFF3366 },
            { name: 'Atölye', x: 250, z: 350, color: 0x00CCFF }
        ];
        
        // Gateway göstergeleri için HTML
        const gatewayIndicators = document.getElementById('gateway-indicators');
        
        zones.forEach((zone, index) => {
            // Platform - Daha ince ve elegant
            const platform = new THREE.Mesh(
                new THREE.CylinderGeometry(45, 50, 6, 32),
                new THREE.MeshStandardMaterial({ 
                    color: zone.color,
                    emissive: zone.color,
                    emissiveIntensity: 0.3,
                    roughness: 0.4,
                    metalness: 0.5
                })
            );
            platform.position.set(zone.x, 3, zone.z);
            platform.castShadow = true;
            platform.receiveShadow = true;
            scene.add(platform);
            
            // Parlayan halka - İnce
            const ring = new THREE.Mesh(
                new THREE.RingGeometry(48, 52, 32),
                new THREE.MeshBasicMaterial({ 
                    color: zone.color,
                    transparent: true,
                    opacity: 0.4,
                    side: THREE.DoubleSide
                })
            );
            ring.position.set(zone.x, 6.5, zone.z);
            ring.rotation.x = -Math.PI / 2;
            scene.add(ring);
            
            // Gateway cihazı - 3D model
            const gatewayGroup = new THREE.Group();
            
            // Ana gövde
            const body = new THREE.Mesh(
                new THREE.CylinderGeometry(8, 10, 25, 16),
                new THREE.MeshStandardMaterial({
                    color: 0x2a2a2a,
                    metalness: 0.8,
                    roughness: 0.2
                })
            );
            body.castShadow = true;
            gatewayGroup.add(body);
            
            // LED göstergesi
            const led = new THREE.Mesh(
                new THREE.SphereGeometry(3, 16, 16),
                new THREE.MeshBasicMaterial({
                    color: zone.color,
                    emissive: zone.color,
                    emissiveIntensity: 1.0
                })
            );
            led.position.y = 10;
            gatewayGroup.add(led);
            
            // Anten
            const antenna = new THREE.Mesh(
                new THREE.CylinderGeometry(0.5, 0.5, 15, 8),
                new THREE.MeshStandardMaterial({
                    color: 0x4a4a4a,
                    metalness: 0.9,
                    roughness: 0.1
                })
            );
            antenna.position.y = 20;
            gatewayGroup.add(antenna);
            
            // Sinyal dalgaları
            for (let i = 1; i <= 3; i++) {
                const wave = new THREE.Mesh(
                    new THREE.TorusGeometry(15 * i, 0.5, 8, 32),
                    new THREE.MeshBasicMaterial({
                        color: zone.color,
                        transparent: true,
                        opacity: 0.3 / i
                    })
                );
                wave.position.y = 20;
                wave.rotation.x = Math.PI / 2;
                gatewayGroup.add(wave);
            }
            
            gatewayGroup.position.set(zone.x, 15, zone.z);
            scene.add(gatewayGroup);
            
            // Bölge ışığı - Daha soft
            const zoneLight = new THREE.PointLight(zone.color, 1.0, 120);
            zoneLight.position.set(zone.x, 40, zone.z);
            scene.add(zoneLight);
            
            // Gateway status indicator
            const indicator = document.createElement('div');
            indicator.className = 'gateway-indicator';
            indicator.style.background = `#${zone.color.toString(16).padStart(6, '0')}`;
            indicator.style.boxShadow = `0 0 10px #${zone.color.toString(16).padStart(6, '0')}`;
            gatewayIndicators.appendChild(indicator);
        });
        
        // ============================================
        // PERSONEL TAG TAKİBİ
        // ============================================
        
        const personnel = new Map();
        
        function createPersonnelTag(color) {
            const group = new THREE.Group();
            
            // Tag - Küre (giyilebilir cihaz)
            const tag = new THREE.Mesh(
                new THREE.SphereGeometry(6, 20, 20),
                new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: 0.6,
                    roughness: 0.3,
                    metalness: 0.4
                })
            );
            tag.castShadow = true;
            group.add(tag);
            
            // Parlama
            const glow = new THREE.Mesh(
                new THREE.SphereGeometry(9, 20, 20),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.25,
                    blending: THREE.AdditiveBlending
                })
            );
            group.add(glow);
            
            // Dikey konum işareti
            const beam = new THREE.Mesh(
                new THREE.CylinderGeometry(0.5, 0.5, 60, 8),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.25
                })
            );
            beam.position.y = 30;
            group.add(beam);
            
            // Zemin halkası
            const groundRing = new THREE.Mesh(
                new THREE.RingGeometry(8, 12, 32),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.5,
                    side: THREE.DoubleSide
                })
            );
            groundRing.rotation.x = -Math.PI / 2;
            groundRing.position.y = 0.5;
            group.add(groundRing);
            
            return group;
        }
        
        window.updateEntity = function(data) {
            const { id, type, location, battery, status } = data;
            
            // Sadece personel
            if (type !== 'personnel') return;
            
            if (!personnel.has(id)) {
                const color = status === 'emergency' ? 0xFF3366 : 0x00FF88;
                const tag = createPersonnelTag(color);
                personnel.set(id, tag);
                scene.add(tag);
            }
            
            const tag = personnel.get(id);
            
            // Pozisyon güncelleme - Smooth
            tag.position.x = location.x;
            tag.position.y = Math.abs(location.z) + 15;
            tag.position.z = location.y;
            
            // Acil durum
            if (status === 'emergency') {
                tag.children[0].material.color.setHex(0xFF3366);
                tag.children[0].material.emissive.setHex(0xFF3366);
                tag.children[0].material.emissiveIntensity = 1.0;
            }
            
            // Düşük batarya uyarısı
            if (battery < 20) {
                const pulse = Math.sin(Date.now() * 0.01) * 0.3 + 0.7;
                tag.children[1].material.opacity = pulse * 0.4;
            }
        };
        
        window.updateCounts = function(personnelCount, equipmentCount) {
            document.getElementById('personnel-count').textContent = personnelCount;
        };
        
        // ============================================
        // KAMERA KONTROLLERI
        // ============================================
        
        let targetRotation = 0;
        let targetElevation = 0.5;
        let isMouseDown = false;
        let cameraDistance = 700;
        
        document.addEventListener('mousedown', () => isMouseDown = true);
        document.addEventListener('mouseup', () => isMouseDown = false);
        
        document.addEventListener('mousemove', (e) => {
            if (isMouseDown) {
                targetRotation += e.movementX * 0.005;
                targetElevation = Math.max(0.1, Math.min(0.9, targetElevation + e.movementY * 0.005));
            }
        });
        
        document.addEventListener('wheel', (e) => {
            cameraDistance += e.deltaY * 0.5;
            cameraDistance = Math.max(300, Math.min(1200, cameraDistance));
        });
        
        // Klavye
        const keys = {};
        document.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
        document.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);
        
        // ============================================
        // ANİMASYON
        // ============================================
        
        let time = 0;
        
        function animate() {
            requestAnimationFrame(animate);
            time += 0.01;
            
            // Kamera
            const cameraX = Math.sin(targetRotation) * cameraDistance;
            const cameraZ = Math.cos(targetRotation) * cameraDistance;
            const cameraY = 200 + targetElevation * 400;
            
            camera.position.x += (cameraX - camera.position.x) * 0.05;
            camera.position.z += (cameraZ - camera.position.z) * 0.05;
            camera.position.y += (cameraY - camera.position.y) * 0.05;
            
            // WASD hareket
            if (keys['w']) camera.position.z -= 5;
            if (keys['s']) camera.position.z += 5;
            if (keys['a']) camera.position.x -= 5;
            if (keys['d']) camera.position.x += 5;
            
            camera.lookAt(0, 30, 0);
            
            // Halka animasyonları
            scene.children.forEach(child => {
                if (child.geometry && child.geometry.type === 'RingGeometry' && child.position.y > 5) {
                    child.material.opacity = 0.3 + Math.sin(time * 2) * 0.1;
                }
            });
            
            renderer.render(scene, camera);
        }
        
        // ============================================
        // BAŞLATMA
        // ============================================
        
        setTimeout(() => {
            document.getElementById('loading').classList.add('hidden');
        }, 1000);
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        console.log('✅ Gateway & Tag Tracking System Ready');
    </script>
</body>
</html>
        """
        self.setHtml(html_content)
    
    def update_position(self, data):
        """Konum güncellemesi - Sadece personel"""
        if not WEBENGINE_AVAILABLE:
            return
            
        entity_type = data['type']
        
        # Sadece personel takibi
        if entity_type != 'personnel':
            return
            
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
        """Tüm konumları yükle - Sadece personel"""
        if not WEBENGINE_AVAILABLE:
            return
            
        # Sadece personel
        for person in self.tracking.get_personnel():
            self.update_position({'type': 'personnel', 'data': person})
        
        # Sayıları güncelle
        stats = self.tracking.get_statistics()
        js_code = f"window.updateCounts({stats['personnel']['total']}, 0);"
        self.page().runJavaScript(js_code)
