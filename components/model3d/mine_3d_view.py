"""Gerçekçi 3D Maden Haritası - Ana Şaft, Galeriler ve Odalar"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import json

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
    BaseClass = QWebEngineView
except ImportError:
    WEBENGINE_AVAILABLE = False
    BaseClass = QWidget

class Mine3DView(BaseClass):
    """Gerçekçi maden yapısı ile 3D görselleştirme"""
    
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
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("3D Visualization\n\nQtWebEngine required\npip install PyQt6-WebEngine")
        label.setStyleSheet("color: #6B7280; font-size: 14px; padding: 40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
    
    def load_3d_scene(self):
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Aico Maden Takip 3D</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #0a0b0d; 
            overflow: hidden; 
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
        }
        #container { width: 100vw; height: 100vh; }
        
        .info-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(17, 24, 39, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            min-width: 280px;
            color: white;
        }
        
        .panel-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 15px;
            color: #3B82F6;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stat-label { color: #9CA3AF; font-size: 13px; }
        .stat-value { color: #F9FAFB; font-size: 18px; font-weight: 700; }
        
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(17, 24, 39, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 16px;
            color: white;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
            font-size: 13px;
        }
        
        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 10px;
            box-shadow: 0 0 10px currentColor;
        }
        
        .controls {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(17, 24, 39, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 12px;
            padding: 12px 24px;
            color: #9CA3AF;
            font-size: 12px;
            display: flex;
            gap: 20px;
        }
        
        .control-key {
            background: rgba(255, 255, 255, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-weight: 600;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div class="info-panel">
        <div class="panel-title">⛏️ Maden Durumu</div>
        <div class="stat-row">
            <span class="stat-label">Personel (Yer Altı)</span>
            <span class="stat-value" id="personnel-count">0</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Anchor Cihazları</span>
            <span class="stat-value">6</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Aktif Galeriler</span>
            <span class="stat-value">12</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">İşletme Odaları</span>
            <span class="stat-value">6</span>
        </div>
    </div>
    
    <div class="legend">
        <div class="legend-item">
            <div class="legend-dot" style="background: #10B981; color: #10B981;"></div>
            <span>Personel</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #3B82F6; color: #3B82F6;"></div>
            <span>Anchor</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #8B5CF6; color: #8B5CF6;"></div>
            <span>Ana Galeri</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #F59E0B; color: #F59E0B;"></div>
            <span>İşletme Odası</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #EF4444; color: #EF4444;"></div>
            <span>Acil Durum</span>
        </div>
    </div>
    
    <div class="controls">
        <span><span class="control-key">🖱️ Mouse</span>Döndür</span>
        <span><span class="control-key">⚲ Scroll</span>Yakınlaş/Uzaklaş</span>
        <span><span class="control-key">WASD</span>Hareket</span>
    </div>

    <script>
        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0b0d);
        scene.fog = new THREE.FogExp2(0x0a0b0d, 0.0008);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 3000);
        camera.position.set(0, 400, 600);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x3a4556, 0.5);
        scene.add(ambientLight);
        
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(200, 400, 200);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        scene.add(mainLight);
        
        // Floor
        const floorGeometry = new THREE.PlaneGeometry(2000, 2000, 50, 50);
        const vertices = floorGeometry.attributes.position.array;
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i + 2] = Math.random() * 3;
        }
        floorGeometry.computeVertexNormals();
        
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x1a1f2e,
            roughness: 0.9,
            metalness: 0.1
        });
        
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Grid
        const gridHelper = new THREE.GridHelper(2000, 40, 0x2a3142, 0x1f2430);
        gridHelper.position.y = 0.1;
        gridHelper.material.opacity = 0.3;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);
        
        // ===============================
        // MADEN YAPISI - Ana Şaft (Giriş)
        // ===============================
        
        function createMainShaft() {
            const shaftGroup = new THREE.Group();
            
            // Ana Şaft Platformu (yüzeyde)
            const shaftPlatform = new THREE.Mesh(
                new THREE.CylinderGeometry(60, 60, 8, 32),
                new THREE.MeshStandardMaterial({ 
                    color: 0x2d3748,
                    roughness: 0.6,
                    metalness: 0.4
                })
            );
            shaftPlatform.position.y = 4;
            shaftPlatform.castShadow = true;
            shaftPlatform.receiveShadow = true;
            shaftGroup.add(shaftPlatform);
            
            // Şaft Çemberi
            const shaftRing = new THREE.Mesh(
                new THREE.TorusGeometry(58, 4, 16, 100),
                new THREE.MeshStandardMaterial({
                    color: 0x3B82F6,
                    emissive: 0x3B82F6,
                    emissiveIntensity: 0.3,
                    metalness: 0.8,
                    roughness: 0.2
                })
            );
            shaftRing.position.y = 4;
            shaftRing.rotation.x = Math.PI / 2;
            shaftGroup.add(shaftRing);
            
            // Işık
            const shaftLight = new THREE.PointLight(0x3B82F6, 1.5, 150);
            shaftLight.position.y = 40;
            shaftGroup.add(shaftLight);
            
            // "ANA ŞAFT" yazısı için marker
            const labelGeometry = new THREE.CylinderGeometry(3, 3, 80, 8);
            const labelMaterial = new THREE.MeshStandardMaterial({
                color: 0x3B82F6,
                emissive: 0x3B82F6,
                emissiveIntensity: 0.5
            });
            const label = new THREE.Mesh(labelGeometry, labelMaterial);
            label.position.y = 40;
            shaftGroup.add(label);
            
            return shaftGroup;
        }
        
        const mainShaft = createMainShaft();
        scene.add(mainShaft);
        
        // ===============================
        // GALERİLER (Tüneller)
        // ===============================
        
        function createGallery(startX, startZ, endX, endZ, width = 20, color = 0x8B5CF6) {
            const gallery = new THREE.Group();
            
            const length = Math.sqrt((endX - startX)**2 + (endZ - startZ)**2);
            const angle = Math.atan2(endZ - startZ, endX - startX);
            
            // Galeri taban
            const galleryFloor = new THREE.Mesh(
                new THREE.BoxGeometry(length, 2, width),
                new THREE.MeshStandardMaterial({
                    color: 0x2a3344,
                    roughness: 0.8
                })
            );
            galleryFloor.position.set(
                (startX + endX) / 2,
                1,
                (startZ + endZ) / 2
            );
            galleryFloor.rotation.y = angle;
            galleryFloor.receiveShadow = true;
            gallery.add(galleryFloor);
            
            // Galeri kenarları (raylar)
            const railMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.2,
                metalness: 0.8,
                roughness: 0.3
            });
            
            for (let side of [-1, 1]) {
                const rail = new THREE.Mesh(
                    new THREE.BoxGeometry(length, 3, 1.5),
                    railMaterial
                );
                rail.position.set(
                    (startX + endX) / 2,
                    2.5,
                    (startZ + endZ) / 2 + side * (width / 2 - 0.75)
                );
                rail.rotation.y = angle;
                gallery.add(rail);
            }
            
            // Galeri ışıkları
            const numLights = Math.floor(length / 60);
            for (let i = 0; i <= numLights; i++) {
                const t = i / numLights;
                const x = startX + (endX - startX) * t;
                const z = startZ + (endZ - startZ) * t;
                
                const light = new THREE.PointLight(color, 0.6, 80);
                light.position.set(x, 20, z);
                gallery.add(light);
                
                // Işık kaynağı göstergesi
                const bulb = new THREE.Mesh(
                    new THREE.SphereGeometry(1.5, 16, 16),
                    new THREE.MeshStandardMaterial({
                        color: color,
                        emissive: color,
                        emissiveIntensity: 1
                    })
                );
                bulb.position.set(x, 20, z);
                gallery.add(bulb);
            }
            
            return gallery;
        }
        
        // Ana galeriler (Ana Şaft'tan çıkan)
        const galleries = [
            // Sektör A'ya (sol üst)
            { start: [0, 0], end: [-350, -200], color: 0x10B981 },
            // Sektör B'ye (sağ üst)
            { start: [0, 0], end: [350, -200], color: 0xF59E0B },
            // Sektör C'ye (alt)
            { start: [0, 0], end: [0, 280], color: 0x8B5CF6 },
            // İşleme'ye (sol alt)
            { start: [0, 0], end: [-250, 350], color: 0xEC4899 },
            // Atölye'ye (sağ alt)
            { start: [0, 0], end: [250, 350], color: 0x06B6D4 }
        ];
        
        galleries.forEach(g => {
            const gallery = createGallery(g.start[0], g.start[1], g.end[0], g.end[1], 22, g.color);
            scene.add(gallery);
        });
        
        // Ara bağlantı galerileri
        const connectionGalleries = [
            { start: [-350, -200], end: [350, -200], color: 0x6366F1 }, // A-B arası
            { start: [-250, 350], end: [250, 350], color: 0x06B6D4 },  // İşleme-Atölye arası
        ];
        
        connectionGalleries.forEach(g => {
            const gallery = createGallery(g.start[0], g.start[1], g.end[0], g.end[1], 18, g.color);
            scene.add(gallery);
        });
        
        // ===============================
        // İŞLETME ODALARI (Çalışma Alanları)
        // ===============================
        
        function createWorkingChamber(x, z, size, color, name) {
            const chamber = new THREE.Group();
            
            // Oda platformu
            const platform = new THREE.Mesh(
                new THREE.BoxGeometry(size, 4, size),
                new THREE.MeshStandardMaterial({
                    color: 0x2d3748,
                    roughness: 0.7,
                    metalness: 0.3
                })
            );
            platform.position.set(x, 2, z);
            platform.castShadow = true;
            platform.receiveShadow = true;
            chamber.add(platform);
            
            // Oda sınırları
            const borderMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.3,
                metalness: 0.7,
                roughness: 0.3
            });
            
            const borderHeight = 6;
            const borderWidth = 2;
            
            // 4 kenar
            const borders = [
                { pos: [x, borderHeight/2, z - size/2 + borderWidth/2], size: [size, borderHeight, borderWidth] },
                { pos: [x, borderHeight/2, z + size/2 - borderWidth/2], size: [size, borderHeight, borderWidth] },
                { pos: [x - size/2 + borderWidth/2, borderHeight/2, z], size: [borderWidth, borderHeight, size] },
                { pos: [x + size/2 - borderWidth/2, borderHeight/2, z], size: [borderWidth, borderHeight, size] }
            ];
            
            borders.forEach(b => {
                const border = new THREE.Mesh(
                    new THREE.BoxGeometry(...b.size),
                    borderMaterial
                );
                border.position.set(...b.pos);
                chamber.add(border);
            });
            
            // Oda ışığı
            const light = new THREE.PointLight(color, 1.2, 100);
            light.position.set(x, 30, z);
            chamber.add(light);
            
            // İsim etiketi için tall marker
            const marker = new THREE.Mesh(
                new THREE.CylinderGeometry(2, 2, 50, 8),
                new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: 0.6
                })
            );
            marker.position.set(x, 25, z);
            chamber.add(marker);
            
            return chamber;
        }
        
        // İşletme odaları oluştur
        const workingChambers = [
            { name: 'Ana Şaft', x: 0, z: 0, size: 80, color: 0x3B82F6 },
            { name: 'Sektör A', x: -350, z: -200, size: 70, color: 0x10B981 },
            { name: 'Sektör B', x: 350, z: -200, size: 70, color: 0xF59E0B },
            { name: 'Sektör C', x: 0, z: 280, size: 70, color: 0x8B5CF6 },
            { name: 'İşleme', x: -250, z: 350, size: 65, color: 0xEC4899 },
            { name: 'Atölye', x: 250, z: 350, size: 65, color: 0x06B6D4 }
        ];
        
        workingChambers.forEach(c => {
            const chamber = createWorkingChamber(c.x, c.z, c.size, c.color, c.name);
            scene.add(chamber);
        });
        
        // ===============================
        // ANCHOR CİHAZLARI
        // ===============================
        
        function createAnchor(x, z, color) {
            const anchor = new THREE.Group();
            
            // Ana gövde
            const body = new THREE.Mesh(
                new THREE.CylinderGeometry(5, 6, 18, 16),
                new THREE.MeshStandardMaterial({
                    color: 0x2d3748,
                    metalness: 0.8,
                    roughness: 0.3
                })
            );
            body.castShadow = true;
            anchor.add(body);
            
            // LED gösterge
            const led = new THREE.Mesh(
                new THREE.SphereGeometry(2.5, 16, 16),
                new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: 1,
                    metalness: 0.3,
                    roughness: 0.4
                })
            );
            led.position.y = 7;
            anchor.add(led);
            
            // Anten
            const antenna = new THREE.Mesh(
                new THREE.CylinderGeometry(0.4, 0.4, 14, 8),
                new THREE.MeshStandardMaterial({
                    color: 0x4a5568,
                    metalness: 0.9,
                    roughness: 0.2
                })
            );
            antenna.position.y = 16;
            anchor.add(antenna);
            
            // Sinyal dalgaları
            for (let i = 1; i <= 3; i++) {
                const wave = new THREE.Mesh(
                    new THREE.TorusGeometry(10 * i, 0.4, 8, 32),
                    new THREE.MeshBasicMaterial({
                        color: color,
                        transparent: true,
                        opacity: 0.2 / i
                    })
                );
                wave.position.y = 16;
                wave.rotation.x = Math.PI / 2;
                anchor.add(wave);
            }
            
            anchor.position.set(x, 10, z);
            return anchor;
        }
        
        // Anchor'ları odaların köşelerine yerleştir
        workingChambers.forEach(c => {
            const anchor = createAnchor(c.x, c.z, c.color);
            scene.add(anchor);
        });
        
        // ===============================
        // PERSONEL TAGLERİ
        // ===============================
        
        const personnel = new Map();
        
        function createPersonnelTag(color) {
            const group = new THREE.Group();
            
            const tag = new THREE.Mesh(
                new THREE.SphereGeometry(4, 20, 20),
                new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: 0.5,
                    roughness: 0.4,
                    metalness: 0.3
                })
            );
            tag.castShadow = true;
            group.add(tag);
            
            const glow = new THREE.Mesh(
                new THREE.SphereGeometry(6, 20, 20),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.2
                })
            );
            group.add(glow);
            
            // Işın
            const beam = new THREE.Mesh(
                new THREE.CylinderGeometry(0.3, 0.3, 40, 8),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.2
                })
            );
            beam.position.y = 20;
            group.add(beam);
            
            return group;
        }
        
        window.updateEntity = function(data) {
            const { id, type, location, status } = data;
            
            if (type !== 'personnel') return;
            
            if (!personnel.has(id)) {
                const color = status === 'emergency' ? 0xEF4444 : 0x10B981;
                const tag = createPersonnelTag(color);
                personnel.set(id, tag);
                scene.add(tag);
            }
            
            const tag = personnel.get(id);
            tag.position.set(location.x, Math.abs(location.z) + 10, location.y);
            
            if (status === 'emergency') {
                tag.children[0].material.color.setHex(0xEF4444);
                tag.children[0].material.emissive.setHex(0xEF4444);
            }
        };
        
        window.updateCounts = function(count) {
            document.getElementById('personnel-count').textContent = count;
        };
        
        // ===============================
        // KAMERA KONTROLÜ
        // ===============================
        
        let targetRotation = 0;
        let targetElevation = 0.5;
        let isMouseDown = false;
        let cameraDistance = 700;
        
        document.addEventListener('mousedown', () => isMouseDown = true);
        document.addEventListener('mouseup', () => isMouseDown = false);
        
        document.addEventListener('mousemove', (e) => {
            if (isMouseDown) {
                targetRotation += e.movementX * 0.005;
                targetElevation = Math.max(0.1, Math.min(0.8, targetElevation + e.movementY * 0.003));
            }
        });
        
        document.addEventListener('wheel', (e) => {
            cameraDistance += e.deltaY * 0.5;
            cameraDistance = Math.max(300, Math.min(1200, cameraDistance));
        });
        
        const keys = {};
        document.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
        document.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);
        
        // ===============================
        // ANİMASYON
        // ===============================
        
        let time = 0;
        
        function animate() {
            requestAnimationFrame(animate);
            time += 0.01;
            
            const cameraX = Math.sin(targetRotation) * cameraDistance;
            const cameraZ = Math.cos(targetRotation) * cameraDistance;
            const cameraY = 100 + targetElevation * 400;
            
            camera.position.x += (cameraX - camera.position.x) * 0.05;
            camera.position.z += (cameraZ - camera.position.z) * 0.05;
            camera.position.y += (cameraY - camera.position.y) * 0.05;
            
            if (keys['w']) camera.position.z -= 5;
            if (keys['s']) camera.position.z += 5;
            if (keys['a']) camera.position.x -= 5;
            if (keys['d']) camera.position.x += 5;
            
            camera.lookAt(0, 0, 0);
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        console.log('✅ Gerçekçi Maden 3D Haritası Hazır!');
    </script>
</body>
</html>
        """
        self.setHtml(html_content)
    
    def update_position(self, data):
        if not WEBENGINE_AVAILABLE:
            return
        entity_type = data['type']
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
        if not WEBENGINE_AVAILABLE:
            return
        for person in self.tracking.get_personnel():
            self.update_position({'type': 'personnel', 'data': person})
        stats = self.tracking.get_statistics()
        js_code = f"window.updateCounts({stats['personnel']['total']});"
        self.page().runJavaScript(js_code)
