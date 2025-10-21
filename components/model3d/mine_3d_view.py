"""3D Yeraltı Maden Görselleştirmesi - Ultra Gerçekçi"""
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
    """Ultra gerçekçi 3D yeraltı maden haritası"""
    
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
        """Ultra gerçekçi 3D yeraltı maden sahnesini yükle"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MineTracker 3D - Yeraltı Maden Haritası</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #000000;
            overflow: hidden; 
            font-family: -apple-system, 'Segoe UI', sans-serif;
        }
        #container { width: 100vw; height: 100vh; }
        
        /* Ana Bilgi Paneli - Sol Üst */
        #info-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(10, 10, 15, 0.95);
            padding: 20px;
            border-radius: 16px;
            border: 2px solid rgba(0, 212, 255, 0.4);
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
            min-width: 280px;
        }
        
        .panel-title {
            color: #00D4FF;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 12px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border-left: 3px solid;
        }
        
        .stat-row.personnel { border-left-color: #00FF88; }
        .stat-row.equipment { border-left-color: #FFB800; }
        .stat-row.depth { border-left-color: #9966FF; }
        
        .stat-label {
            color: #B0B0B0;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stat-value {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 700;
        }
        
        /* Derinlik Göstergesi - Sağ */
        #depth-gauge {
            position: absolute;
            right: 30px;
            top: 50%;
            transform: translateY(-50%);
            width: 60px;
            height: 400px;
            background: linear-gradient(to bottom, 
                rgba(0, 212, 255, 0.3) 0%,
                rgba(153, 102, 255, 0.3) 50%,
                rgba(255, 51, 102, 0.3) 100%);
            border-radius: 30px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 15px 10px;
        }
        
        .depth-marker {
            color: white;
            font-size: 11px;
            margin: 8px 0;
            text-align: center;
            font-weight: 600;
        }
        
        /* Lejant - Sağ Üst */
        #legend {
            position: absolute;
            top: 20px;
            right: 120px;
            background: rgba(10, 10, 15, 0.95);
            padding: 18px;
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(15px);
        }
        
        .legend-title {
            color: #00D4FF;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
            gap: 10px;
        }
        
        .legend-icon {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            box-shadow: 0 0 10px currentColor;
        }
        
        .legend-text {
            color: #E0E0E0;
            font-size: 13px;
        }
        
        /* Kontroller - Alt */
        #controls {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(10, 10, 15, 0.95);
            padding: 15px 25px;
            border-radius: 25px;
            border: 2px solid rgba(0, 212, 255, 0.3);
            backdrop-filter: blur(15px);
            display: flex;
            gap: 25px;
            align-items: center;
        }
        
        .control-item {
            color: #B0B0B0;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .control-icon {
            color: #00D4FF;
            font-size: 16px;
        }
        
        /* Uyarı Sistemi */
        #alerts {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            max-width: 400px;
        }
        
        .alert {
            background: rgba(255, 51, 102, 0.95);
            color: white;
            padding: 15px 20px;
            border-radius: 12px;
            margin-bottom: 10px;
            border-left: 4px solid #FF0033;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 20px rgba(255, 51, 102, 0.4);
        }
        
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        /* Yükleme Ekranı */
        #loading {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000000;
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
            width: 60px;
            height: 60px;
            border: 4px solid rgba(0, 212, 255, 0.2);
            border-top: 4px solid #00D4FF;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: #00D4FF;
            margin-top: 20px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <!-- Yükleme Ekranı -->
    <div id="loading">
        <div class="loader"></div>
        <div class="loading-text">⛏️ Yeraltı haritası yükleniyor...</div>
    </div>

    <!-- 3D Container -->
    <div id="container"></div>
    
    <!-- Bilgi Paneli -->
    <div id="info-panel">
        <div class="panel-title">
            <span>⛏️</span>
            <span>MineTracker 3D</span>
        </div>
        <div class="stat-row personnel">
            <span class="stat-label">👷 Personel</span>
            <span class="stat-value" id="personnel-count">0</span>
        </div>
        <div class="stat-row equipment">
            <span class="stat-label">🚜 Ekipman</span>
            <span class="stat-value" id="equipment-count">0</span>
        </div>
        <div class="stat-row depth">
            <span class="stat-label">📏 Derinlik</span>
            <span class="stat-value" id="depth-value">-45m</span>
        </div>
    </div>
    
    <!-- Derinlik Göstergesi -->
    <div id="depth-gauge">
        <div class="depth-marker">0m</div>
        <div style="height: 30px; border-left: 2px dashed rgba(255,255,255,0.3); margin: 5px auto;"></div>
        <div class="depth-marker">-25m</div>
        <div style="height: 30px; border-left: 2px dashed rgba(255,255,255,0.3); margin: 5px auto;"></div>
        <div class="depth-marker">-50m</div>
        <div style="height: 30px; border-left: 2px dashed rgba(255,255,255,0.3); margin: 5px auto;"></div>
        <div class="depth-marker">-75m</div>
        <div style="height: 30px; border-left: 2px dashed rgba(255,255,255,0.3); margin: 5px auto;"></div>
        <div class="depth-marker">-100m</div>
    </div>
    
    <!-- Lejant -->
    <div id="legend">
        <div class="legend-title">📍 Semboller</div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #00FF88;"></div>
            <span class="legend-text">Personel</span>
        </div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #FFB800;"></div>
            <span class="legend-text">Ekipman</span>
        </div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #FF3366;"></div>
            <span class="legend-text">Acil Durum</span>
        </div>
        <div class="legend-item">
            <div class="legend-icon" style="background: #00D4FF;"></div>
            <span class="legend-text">Güvenli Bölge</span>
        </div>
    </div>
    
    <!-- Kontroller -->
    <div id="controls">
        <div class="control-item">
            <span class="control-icon">🖱️</span>
            <span>Sürükle: Döndür</span>
        </div>
        <div class="control-item">
            <span class="control-icon">🔍</span>
            <span>Scroll: Zoom</span>
        </div>
        <div class="control-item">
            <span class="control-icon">⌨️</span>
            <span>WASD: Hareket</span>
        </div>
    </div>
    
    <!-- Uyarılar -->
    <div id="alerts"></div>

    <script>
        // ============================================
        // SAHNE KURULUMU - ULTRA GERÇEKÇİ
        // ============================================
        
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0f);
        scene.fog = new THREE.FogExp2(0x0a0a0f, 0.0008);
        
        // Kamera - Perspektif
        const camera = new THREE.PerspectiveCamera(
            60, 
            window.innerWidth / window.innerHeight, 
            0.1, 
            3000
        );
        camera.position.set(500, 400, 700);
        camera.lookAt(0, 0, 0);
        
        // Renderer - Yüksek Kalite
        const renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        document.getElementById('container').appendChild(renderer.domElement);
        
        // ============================================
        // IŞIKLANDIRMA - MADEN ORTAMI
        // ============================================
        
        // Ambient - Zayıf yeraltı ışığı
        const ambientLight = new THREE.AmbientLight(0x4a3520, 0.3);
        scene.add(ambientLight);
        
        // Ana ışık - Yukarıdan (giriş ışığı)
        const mainLight = new THREE.DirectionalLight(0xffa366, 0.8);
        mainLight.position.set(0, 500, 0);
        mainLight.castShadow = true;
        mainLight.shadow.camera.left = -800;
        mainLight.shadow.camera.right = 800;
        mainLight.shadow.camera.top = 800;
        mainLight.shadow.camera.bottom = -800;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        scene.add(mainLight);
        
        // Nokta ışıklar - Maden lambaları (turuncu/sarı)
        const lampColors = [0xffaa44, 0xff8844, 0xffcc66];
        const lampPositions = [
            [0, 100, 0],
            [-300, 80, -200],
            [300, 80, -200],
            [0, 80, 300],
            [-200, 90, 200],
            [200, 90, 200]
        ];
        
        lampPositions.forEach((pos, i) => {
            const lamp = new THREE.PointLight(
                lampColors[i % lampColors.length], 
                1.2, 
                300
            );
            lamp.position.set(pos[0], pos[1], pos[2]);
            lamp.castShadow = true;
            scene.add(lamp);
            
            // Işık görsel efekti
            const lampGlow = new THREE.Mesh(
                new THREE.SphereGeometry(8, 16, 16),
                new THREE.MeshBasicMaterial({ 
                    color: lampColors[i % lampColors.length],
                    transparent: true,
                    opacity: 0.8
                })
            );
            lampGlow.position.copy(lamp.position);
            scene.add(lampGlow);
        });
        
        // Spot ışıklar - Çalışma alanları
        const spotLight1 = new THREE.SpotLight(0xffffff, 1.5);
        spotLight1.position.set(-200, 200, 0);
        spotLight1.angle = Math.PI / 6;
        spotLight1.penumbra = 0.3;
        spotLight1.castShadow = true;
        scene.add(spotLight1);
        
        // ============================================
        // MADEN ZEMİNİ - GERÇEKÇİ KAYA DOKUSU
        // ============================================
        
        const floorGeometry = new THREE.PlaneGeometry(2000, 2000, 100, 100);
        const vertices = floorGeometry.attributes.position.array;
        
        // Pürüzlü zemin için noise
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i + 2] = Math.random() * 5 - Math.random() * 8;
        }
        floorGeometry.attributes.position.needsUpdate = true;
        floorGeometry.computeVertexNormals();
        
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x3a2a1a,
            roughness: 0.95,
            metalness: 0.1,
            flatShading: true
        });
        
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.position.y = -5;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // ============================================
        // MADEN TÜNELLERİ VE YAPILAR
        // ============================================
        
        const tunnelMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2a1a0a,
            roughness: 0.9,
            metalness: 0.05,
            side: THREE.DoubleSide
        });
        
        // Ana tünel - Yatay
        const mainTunnelGeom = new THREE.CylinderGeometry(40, 40, 800, 12, 1, false);
        const mainTunnel = new THREE.Mesh(mainTunnelGeom, tunnelMaterial);
        mainTunnel.rotation.z = Math.PI / 2;
        mainTunnel.position.set(0, 40, 0);
        mainTunnel.castShadow = true;
        mainTunnel.receiveShadow = true;
        scene.add(mainTunnel);
        
        // Yan tüneller
        for (let i = -300; i <= 300; i += 200) {
            const sideTunnel = new THREE.Mesh(
                new THREE.CylinderGeometry(35, 35, 600, 10),
                tunnelMaterial
            );
            sideTunnel.rotation.x = Math.PI / 2;
            sideTunnel.position.set(i, 35, 0);
            sideTunnel.castShadow = true;
            scene.add(sideTunnel);
        }
        
        // Destek kirişleri (ahşap)
        const beamMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x4a3520,
            roughness: 0.8
        });
        
        for (let i = -400; i <= 400; i += 80) {
            // Dikey destek
            const beam = new THREE.Mesh(
                new THREE.BoxGeometry(8, 100, 8),
                beamMaterial
            );
            beam.position.set(i, 50, Math.sin(i * 0.01) * 150);
            beam.castShadow = true;
            scene.add(beam);
            
            // Yatay destek
            if (i % 160 === 0) {
                const crossBeam = new THREE.Mesh(
                    new THREE.BoxGeometry(160, 8, 8),
                    beamMaterial
                );
                crossBeam.position.set(i, 95, Math.sin(i * 0.01) * 150);
                scene.add(crossBeam);
            }
        }
        
        // ============================================
        // MADEN BÖLGE PLATFORMLARI - RENKLENDIRILMIŞ
        // ============================================
        
        const zones = [
            { name: 'Ana Şaft', x: 0, z: 0, color: 0x00D4FF, icon: '⛏️' },
            { name: 'Sektör A', x: -350, z: -200, color: 0x00FF88, icon: '🔨' },
            { name: 'Sektör B', x: 350, z: -200, color: 0xFFB800, icon: '⚙️' },
            { name: 'Sektör C', x: 0, z: 280, color: 0xFF3366, icon: '🔧' },
            { name: 'İşleme', x: -250, z: 350, color: 0x9966FF, icon: '⚒️' },
            { name: 'Atölye', x: 250, z: 350, color: 0x00CCFF, icon: '🛠️' }
        ];
        
        zones.forEach(zone => {
            // Platform tabanı
            const platform = new THREE.Mesh(
                new THREE.CylinderGeometry(55, 60, 8, 32),
                new THREE.MeshStandardMaterial({ 
                    color: zone.color,
                    emissive: zone.color,
                    emissiveIntensity: 0.4,
                    roughness: 0.3,
                    metalness: 0.6
                })
            );
            platform.position.set(zone.x, 4, zone.z);
            platform.castShadow = true;
            platform.receiveShadow = true;
            scene.add(platform);
            
            // Parlayan halka
            const ring = new THREE.Mesh(
                new THREE.RingGeometry(52, 65, 32),
                new THREE.MeshBasicMaterial({ 
                    color: zone.color,
                    transparent: true,
                    opacity: 0.5,
                    side: THREE.DoubleSide
                })
            );
            ring.position.set(zone.x, 8.5, zone.z);
            ring.rotation.x = -Math.PI / 2;
            scene.add(ring);
            
            // Işın efekti
            const lightBeam = new THREE.Mesh(
                new THREE.CylinderGeometry(45, 50, 200, 32, 1, true),
                new THREE.MeshBasicMaterial({
                    color: zone.color,
                    transparent: true,
                    opacity: 0.15,
                    side: THREE.DoubleSide
                })
            );
            lightBeam.position.set(zone.x, 100, zone.z);
            scene.add(lightBeam);
            
            // Bölge ışığı
            const zoneLight = new THREE.PointLight(zone.color, 1.5, 150);
            zoneLight.position.set(zone.x, 50, zone.z);
            scene.add(zoneLight);
        });
        
        // ============================================
        // MADEN EKİPMANLARI (STATİK MODELLER)
        // ============================================
        
        // Konveyör bantları
        for (let i = -300; i <= 300; i += 150) {
            const conveyor = new THREE.Group();
            
            // Bant tabanı
            const base = new THREE.Mesh(
                new THREE.BoxGeometry(100, 10, 30),
                new THREE.MeshStandardMaterial({ 
                    color: 0x2a2a2a,
                    metalness: 0.7,
                    roughness: 0.3
                })
            );
            base.position.y = 10;
            conveyor.add(base);
            
            // Bant yüzeyi
            const belt = new THREE.Mesh(
                new THREE.BoxGeometry(98, 2, 25),
                new THREE.MeshStandardMaterial({ 
                    color: 0x1a1a1a,
                    roughness: 0.8
                })
            );
            belt.position.y = 16;
            conveyor.add(belt);
            
            conveyor.position.set(i, 0, -100);
            conveyor.rotation.y = Math.PI / 4;
            scene.add(conveyor);
        }
        
        // Maden arabaları (ray üzerinde)
        const railMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x4a4a4a,
            metalness: 0.8,
            roughness: 0.2
        });
        
        for (let i = -400; i <= 400; i += 200) {
            // Ray
            const rail = new THREE.Mesh(
                new THREE.BoxGeometry(4, 4, 600),
                railMaterial
            );
            rail.position.set(i, 2, 0);
            scene.add(rail);
            
            // Araba
            const cart = new THREE.Group();
            const cartBody = new THREE.Mesh(
                new THREE.BoxGeometry(30, 20, 40),
                new THREE.MeshStandardMaterial({ 
                    color: 0x8b4513,
                    roughness: 0.7
                })
            );
            cart.add(cartBody);
            
            // Tekerlekler
            for (let j = -15; j <= 15; j += 30) {
                const wheel = new THREE.Mesh(
                    new THREE.CylinderGeometry(5, 5, 8, 16),
                    new THREE.MeshStandardMaterial({ color: 0x2a2a2a })
                );
                wheel.rotation.z = Math.PI / 2;
                wheel.position.set(j, -10, 15);
                cart.add(wheel.clone());
                wheel.position.z = -15;
                cart.add(wheel);
            }
            
            cart.position.set(i, 15, Math.sin(i * 0.01) * 100);
            scene.add(cart);
        }
        
        // ============================================
        // PARTİKÜL SİSTEMİ - TOZ VE DUMANçı
        // ============================================
        
        const particleCount = 2000;
        const particles = new THREE.BufferGeometry();
        const particlePositions = new Float32Array(particleCount * 3);
        const particleVelocities = [];
        
        for (let i = 0; i < particleCount; i++) {
            particlePositions[i * 3] = (Math.random() - 0.5) * 1500;
            particlePositions[i * 3 + 1] = Math.random() * 200;
            particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 1500;
            
            particleVelocities.push({
                x: (Math.random() - 0.5) * 0.1,
                y: Math.random() * 0.2,
                z: (Math.random() - 0.5) * 0.1
            });
        }
        
        particles.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
        
        const particleMaterial = new THREE.PointsMaterial({
            color: 0x8b7355,
            size: 2,
            transparent: true,
            opacity: 0.3,
            blending: THREE.AdditiveBlending
        });
        
        const particleSystem = new THREE.Points(particles, particleMaterial);
        scene.add(particleSystem);
        
        // ============================================
        // CİHAZ TAKİP SİSTEMİ
        // ============================================
        
        const entities = new Map();
        
        function createEntityMarker(type, color) {
            const group = new THREE.Group();
            
            // Ana marker
            const geometry = type === 'personnel' 
                ? new THREE.SphereGeometry(8, 16, 16)
                : new THREE.BoxGeometry(14, 14, 14);
            
            const material = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.6,
                roughness: 0.2,
                metalness: 0.5
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.castShadow = true;
            group.add(mesh);
            
            // Parlama efekti
            const glowGeom = type === 'personnel'
                ? new THREE.SphereGeometry(12, 16, 16)
                : new THREE.BoxGeometry(20, 20, 20);
            
            const glowMat = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.25,
                blending: THREE.AdditiveBlending
            });
            
            const glow = new THREE.Mesh(glowGeom, glowMat);
            group.add(glow);
            
            // Dikey ışın
            const beam = new THREE.Mesh(
                new THREE.CylinderGeometry(1, 1, 100, 8),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.3
                })
            );
            beam.position.y = 50;
            group.add(beam);
            
            // Zemin işareti
            const groundMarker = new THREE.Mesh(
                new THREE.RingGeometry(10, 15, 32),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.6,
                    side: THREE.DoubleSide
                })
            );
            groundMarker.rotation.x = -Math.PI / 2;
            groundMarker.position.y = -20;
            group.add(groundMarker);
            
            return group;
        }
        
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
                
                const marker = createEntityMarker(type, color);
                entities.set(id, marker);
                scene.add(marker);
            }
            
            const marker = entities.get(id);
            
            // Smooth pozisyon geçişi
            marker.position.x = location.x;
            marker.position.y = Math.abs(location.z) + 25;
            marker.position.z = location.y;
            
            // Batarya düşükse alarm
            if (battery < 20) {
                marker.children[0].material.emissiveIntensity = 0.9;
                const pulse = Math.sin(Date.now() * 0.01) * 0.3 + 0.7;
                marker.children[1].material.opacity = pulse * 0.5;
            }
            
            // Acil durum
            if (status === 'emergency') {
                marker.children[0].material.color.setHex(0xFF3366);
                marker.children[0].material.emissive.setHex(0xFF3366);
                marker.children[0].material.emissiveIntensity = 1.0;
                
                // Uyarı oluştur
                showAlert(`🚨 ${type === 'personnel' ? 'PERSONEL' : 'EKİPMAN'} ACİL DURUMU: ${id}`);
            }
        };
        
        window.updateCounts = function(personnel, equipment) {
            document.getElementById('personnel-count').textContent = personnel;
            document.getElementById('equipment-count').textContent = equipment;
        };
        
        function showAlert(message) {
            const alertsDiv = document.getElementById('alerts');
            const alert = document.createElement('div');
            alert.className = 'alert';
            alert.textContent = message;
            alertsDiv.appendChild(alert);
            
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        }
        
        // ============================================
        // KAMERA KONTROLLERI
        // ============================================
        
        let mouseX = 0, mouseY = 0;
        let targetRotation = 0;
        let targetElevation = 0.5;
        let isMouseDown = false;
        let cameraDistance = 800;
        
        document.addEventListener('mousedown', () => isMouseDown = true);
        document.addEventListener('mouseup', () => isMouseDown = false);
        
        document.addEventListener('mousemove', (e) => {
            if (isMouseDown) {
                const deltaX = e.movementX * 0.005;
                const deltaY = e.movementY * 0.005;
                targetRotation += deltaX;
                targetElevation = Math.max(0.1, Math.min(0.9, targetElevation + deltaY));
            }
        });
        
        document.addEventListener('wheel', (e) => {
            cameraDistance += e.deltaY * 0.5;
            cameraDistance = Math.max(300, Math.min(1500, cameraDistance));
        });
        
        // Klavye kontrolleri
        const keys = {};
        document.addEventListener('keydown', (e) => keys[e.key] = true);
        document.addEventListener('keyup', (e) => keys[e.key] = false);
        
        // ============================================
        // ANİMASYON DÖNGÜSÜ
        // ============================================
        
        let time = 0;
        
        function animate() {
            requestAnimationFrame(animate);
            time += 0.01;
            
            // Kamera hareketi
            const cameraX = Math.sin(targetRotation) * cameraDistance;
            const cameraZ = Math.cos(targetRotation) * cameraDistance;
            const cameraY = 200 + targetElevation * 600;
            
            camera.position.x += (cameraX - camera.position.x) * 0.05;
            camera.position.z += (cameraZ - camera.position.z) * 0.05;
            camera.position.y += (cameraY - camera.position.y) * 0.05;
            
            // Klavye ile hareket
            if (keys['w']) camera.position.z -= 5;
            if (keys['s']) camera.position.z += 5;
            if (keys['a']) camera.position.x -= 5;
            if (keys['d']) camera.position.x += 5;
            
            camera.lookAt(0, 50, 0);
            
            // Partikül animasyonu
            const positions = particleSystem.geometry.attributes.position.array;
            for (let i = 0; i < particleCount; i++) {
                const idx = i * 3;
                positions[idx] += particleVelocities[i].x;
                positions[idx + 1] += particleVelocities[i].y;
                positions[idx + 2] += particleVelocities[i].z;
                
                // Sınırlar
                if (positions[idx + 1] > 200) {
                    positions[idx + 1] = 0;
                    positions[idx] = (Math.random() - 0.5) * 1500;
                    positions[idx + 2] = (Math.random() - 0.5) * 1500;
                }
            }
            particleSystem.geometry.attributes.position.needsUpdate = true;
            
            // Bölge halkaları pulse efekti
            zones.forEach((zone, index) => {
                const pulse = Math.sin(time * 2 + index) * 0.2 + 0.5;
                scene.children.forEach(child => {
                    if (child.geometry && child.geometry.type === 'RingGeometry') {
                        if (Math.abs(child.position.x - zone.x) < 1 && 
                            Math.abs(child.position.z - zone.z) < 1) {
                            child.material.opacity = pulse;
                        }
                    }
                });
            });
            
            // Işık nabızları
            lampPositions.forEach((pos, i) => {
                scene.children.forEach(child => {
                    if (child instanceof THREE.PointLight && 
                        Math.abs(child.position.x - pos[0]) < 1) {
                        child.intensity = 1.0 + Math.sin(time * 3 + i) * 0.3;
                    }
                });
            });
            
            renderer.render(scene, camera);
        }
        
        // ============================================
        // BAŞLATMA
        // ============================================
        
        setTimeout(() => {
            document.getElementById('loading').classList.add('hidden');
        }, 1500);
        
        animate();
        
        // Pencere resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        console.log('⛏️ MineTracker 3D Yüklendi - Ultra Gerçekçi Mod');
    </script>
</body>
</html>
        """
        self.setHtml(html_content)
    
    def update_position(self, data):
        """Konum güncellemesi"""
        if not WEBENGINE_AVAILABLE:
            return
            
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
            return
            
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
