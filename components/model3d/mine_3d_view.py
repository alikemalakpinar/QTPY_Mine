"""Ultra Profesyonel 3D Harita - Enterprise Grade Design"""
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
    """Enterprise grade 3D visualization"""
    
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
    <title>MineTracker Pro</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #0a0b0d;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        #container {
            width: 100vw;
            height: 100vh;
        }
        
        /* Stats Panel - Clean & Minimal */
        .stats-panel {
            position: absolute;
            top: 32px;
            left: 32px;
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: saturate(180%) blur(20px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 24px;
            min-width: 280px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .stats-header {
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .stats-title {
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            color: #9CA3AF;
            margin-bottom: 4px;
        }
        
        .stats-subtitle {
            font-size: 20px;
            font-weight: 700;
            color: #F9FAFB;
            letter-spacing: -0.5px;
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }
        
        .stat-item:last-child {
            border-bottom: none;
        }
        
        .stat-label {
            font-size: 13px;
            color: #9CA3AF;
            font-weight: 500;
        }
        
        .stat-value {
            font-size: 22px;
            font-weight: 700;
            color: #F9FAFB;
            letter-spacing: -0.5px;
        }
        
        .stat-unit {
            font-size: 12px;
            font-weight: 500;
            color: #6B7280;
            margin-left: 4px;
        }
        
        .status-dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #10B981;
            margin-right: 8px;
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Legend - Minimal */
        .legend {
            position: absolute;
            top: 32px;
            right: 32px;
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: saturate(180%) blur(20px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 16px 20px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
        }
        
        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 12px;
            box-shadow: 0 0 12px currentColor;
        }
        
        .legend-text {
            font-size: 13px;
            color: #E5E7EB;
            font-weight: 500;
        }
        
        /* Controls - Bottom */
        .controls {
            position: absolute;
            bottom: 32px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: saturate(180%) blur(20px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 12px 24px;
            display: flex;
            gap: 32px;
        }
        
        .control-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: #9CA3AF;
            font-weight: 500;
        }
        
        .control-key {
            background: rgba(255, 255, 255, 0.08);
            color: #E5E7EB;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            font-family: 'SF Mono', 'Courier New', monospace;
        }
        
        /* Gateway Status */
        .gateway-status {
            position: absolute;
            bottom: 32px;
            right: 32px;
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: saturate(180%) blur(20px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .gateway-label {
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: #9CA3AF;
        }
        
        .gateway-indicators {
            display: flex;
            gap: 6px;
        }
        
        .gateway-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }
    </style>
</head>
<body>
    <div id="container"></div>
    
    <!-- Stats Panel -->
    <div class="stats-panel">
        <div class="stats-header">
            <div class="stats-title">Live Tracking</div>
            <div class="stats-subtitle">MineTracker Pro</div>
        </div>
        <div class="stat-item">
            <span class="stat-label">
                <span class="status-dot"></span>Personnel
            </span>
            <div>
                <span class="stat-value" id="personnel-count">0</span>
                <span class="stat-unit">active</span>
            </div>
        </div>
        <div class="stat-item">
            <span class="stat-label">Gateways</span>
            <div>
                <span class="stat-value">6</span>
                <span class="stat-unit">online</span>
            </div>
        </div>
        <div class="stat-item">
            <span class="stat-label">Coverage</span>
            <div>
                <span class="stat-value">100</span>
                <span class="stat-unit">%</span>
            </div>
        </div>
    </div>
    
    <!-- Legend -->
    <div class="legend">
        <div class="legend-item">
            <div class="legend-dot" style="background: #10B981; color: #10B981;"></div>
            <span class="legend-text">Personnel</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #3B82F6; color: #3B82F6;"></div>
            <span class="legend-text">Gateway</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #EF4444; color: #EF4444;"></div>
            <span class="legend-text">Alert</span>
        </div>
    </div>
    
    <!-- Controls -->
    <div class="controls">
        <div class="control-item">
            <span class="control-key">Mouse</span>
            <span>Rotate</span>
        </div>
        <div class="control-item">
            <span class="control-key">Scroll</span>
            <span>Zoom</span>
        </div>
        <div class="control-item">
            <span class="control-key">WASD</span>
            <span>Move</span>
        </div>
    </div>
    
    <!-- Gateway Status -->
    <div class="gateway-status">
        <span class="gateway-label">Gateway Status</span>
        <div class="gateway-indicators" id="gateway-indicators"></div>
    </div>

    <script>
        // Scene Setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0b0d);
        scene.fog = new THREE.FogExp2(0x0a0b0d, 0.0005);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 3000);
        camera.position.set(350, 300, 500);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.1;
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Lighting - Professional
        const ambientLight = new THREE.AmbientLight(0x3a4556, 0.6);
        scene.add(ambientLight);
        
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.9);
        mainLight.position.set(200, 400, 200);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.left = -500;
        mainLight.shadow.camera.right = 500;
        mainLight.shadow.camera.top = 500;
        mainLight.shadow.camera.bottom = -500;
        scene.add(mainLight);
        
        const fillLight = new THREE.DirectionalLight(0x5a6f8a, 0.4);
        fillLight.position.set(-200, 200, -200);
        scene.add(fillLight);
        
        // Floor - Clean & Minimal
        const floorGeometry = new THREE.PlaneGeometry(1600, 1400, 60, 60);
        const vertices = floorGeometry.attributes.position.array;
        
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i + 2] = Math.random() * 2;
        }
        floorGeometry.attributes.position.needsUpdate = true;
        floorGeometry.computeVertexNormals();
        
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x1a1f2e,
            roughness: 0.85,
            metalness: 0.15
        });
        
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Grid - Subtle
        const gridHelper = new THREE.GridHelper(1600, 32, 0x2a3142, 0x1f2430);
        gridHelper.position.y = 0.1;
        gridHelper.material.transparent = true;
        gridHelper.material.opacity = 0.3;
        scene.add(gridHelper);
        
        // Zones & Gateways - Professional
        const zones = [
            { name: 'Main Shaft', x: 0, z: 0, color: 0x3B82F6 },
            { name: 'Sector A', x: -350, z: -200, color: 0x10B981 },
            { name: 'Sector B', x: 350, z: -200, color: 0x8B5CF6 },
            { name: 'Sector C', x: 0, z: 280, color: 0xF59E0B },
            { name: 'Processing', x: -250, z: 350, color: 0xEC4899 },
            { name: 'Workshop', x: 250, z: 350, color: 0x06B6D4 }
        ];
        
        const gatewayIndicators = document.getElementById('gateway-indicators');
        
        zones.forEach((zone, index) => {
            // Platform - Minimalist
            const platform = new THREE.Mesh(
                new THREE.CylinderGeometry(40, 45, 4, 32),
                new THREE.MeshStandardMaterial({ 
                    color: zone.color,
                    emissive: zone.color,
                    emissiveIntensity: 0.15,
                    roughness: 0.5,
                    metalness: 0.4
                })
            );
            platform.position.set(zone.x, 2, zone.z);
            platform.castShadow = true;
            platform.receiveShadow = true;
            scene.add(platform);
            
            // Ring - Subtle
            const ring = new THREE.Mesh(
                new THREE.RingGeometry(43, 46, 32),
                new THREE.MeshBasicMaterial({ 
                    color: zone.color,
                    transparent: true,
                    opacity: 0.25,
                    side: THREE.DoubleSide
                })
            );
            ring.position.set(zone.x, 4.5, zone.z);
            ring.rotation.x = -Math.PI / 2;
            scene.add(ring);
            
            // Gateway Device - Clean Design
            const gateway = new THREE.Group();
            
            // Body
            const body = new THREE.Mesh(
                new THREE.CylinderGeometry(6, 7, 20, 16),
                new THREE.MeshStandardMaterial({
                    color: 0x2d3748,
                    metalness: 0.7,
                    roughness: 0.3
                })
            );
            body.castShadow = true;
            gateway.add(body);
            
            // LED - Parlayan gösterge
            const led = new THREE.Mesh(
                new THREE.SphereGeometry(2, 16, 16),
                new THREE.MeshStandardMaterial({
                    color: zone.color,
                    emissive: zone.color,
                    emissiveIntensity: 1.0,
                    metalness: 0.3,
                    roughness: 0.4
                })
            );
            led.position.y = 8;
            gateway.add(led);
            
            // Antenna
            const antenna = new THREE.Mesh(
                new THREE.CylinderGeometry(0.3, 0.3, 12, 8),
                new THREE.MeshStandardMaterial({
                    color: 0x4a5568,
                    metalness: 0.9,
                    roughness: 0.2
                })
            );
            antenna.position.y = 16;
            gateway.add(antenna);
            
            // Signal waves - Subtle
            for (let i = 1; i <= 2; i++) {
                const wave = new THREE.Mesh(
                    new THREE.TorusGeometry(12 * i, 0.3, 8, 32),
                    new THREE.MeshBasicMaterial({
                        color: zone.color,
                        transparent: true,
                        opacity: 0.15 / i
                    })
                );
                wave.position.y = 16;
                wave.rotation.x = Math.PI / 2;
                gateway.add(wave);
            }
            
            gateway.position.set(zone.x, 12, zone.z);
            scene.add(gateway);
            
            // Zone light - Subtle
            const light = new THREE.PointLight(zone.color, 0.6, 100);
            light.position.set(zone.x, 30, zone.z);
            scene.add(light);
            
            // Gateway indicator
            const dot = document.createElement('div');
            dot.className = 'gateway-dot';
            gatewayIndicators.appendChild(dot);
        });
        
        // Personnel Tags - Clean & Simple
        const personnel = new Map();
        
        function createPersonnelTag(color) {
            const group = new THREE.Group();
            
            const tag = new THREE.Mesh(
                new THREE.SphereGeometry(5, 20, 20),
                new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: 0.4,
                    roughness: 0.4,
                    metalness: 0.3
                })
            );
            tag.castShadow = true;
            group.add(tag);
            
            const glow = new THREE.Mesh(
                new THREE.SphereGeometry(7, 20, 20),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.15,
                    blending: THREE.AdditiveBlending
                })
            );
            group.add(glow);
            
            const beam = new THREE.Mesh(
                new THREE.CylinderGeometry(0.3, 0.3, 40, 8),
                new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.15
                })
            );
            beam.position.y = 20;
            group.add(beam);
            
            return group;
        }
        
        window.updateEntity = function(data) {
            const { id, type, location, battery, status } = data;
            
            if (type !== 'personnel') return;
            
            if (!personnel.has(id)) {
                const color = status === 'emergency' ? 0xEF4444 : 0x10B981;
                const tag = createPersonnelTag(color);
                personnel.set(id, tag);
                scene.add(tag);
            }
            
            const tag = personnel.get(id);
            tag.position.set(location.x, Math.abs(location.z) + 12, location.y);
            
            if (status === 'emergency') {
                tag.children[0].material.color.setHex(0xEF4444);
                tag.children[0].material.emissive.setHex(0xEF4444);
            }
        };
        
        window.updateCounts = function(count) {
            document.getElementById('personnel-count').textContent = count;
        };
        
        // Camera Controls - Smooth
        let targetRotation = 0.3;
        let targetElevation = 0.4;
        let isMouseDown = false;
        let cameraDistance = 600;
        
        document.addEventListener('mousedown', () => isMouseDown = true);
        document.addEventListener('mouseup', () => isMouseDown = false);
        
        document.addEventListener('mousemove', (e) => {
            if (isMouseDown) {
                targetRotation += e.movementX * 0.003;
                targetElevation = Math.max(0.1, Math.min(0.7, targetElevation + e.movementY * 0.003));
            }
        });
        
        document.addEventListener('wheel', (e) => {
            cameraDistance += e.deltaY * 0.3;
            cameraDistance = Math.max(300, Math.min(1000, cameraDistance));
        });
        
        const keys = {};
        document.addEventListener('keydown', (e) => keys[e.key.toLowerCase()] = true);
        document.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);
        
        // Animation Loop
        let time = 0;
        
        function animate() {
            requestAnimationFrame(animate);
            time += 0.01;
            
            const cameraX = Math.sin(targetRotation) * cameraDistance;
            const cameraZ = Math.cos(targetRotation) * cameraDistance;
            const cameraY = 150 + targetElevation * 350;
            
            camera.position.x += (cameraX - camera.position.x) * 0.05;
            camera.position.z += (cameraZ - camera.position.z) * 0.05;
            camera.position.y += (cameraY - camera.position.y) * 0.05;
            
            if (keys['w']) camera.position.z -= 3;
            if (keys['s']) camera.position.z += 3;
            if (keys['a']) camera.position.x -= 3;
            if (keys['d']) camera.position.x += 3;
            
            camera.lookAt(0, 20, 0);
            
            // Subtle animations
            scene.children.forEach(child => {
                if (child.geometry && child.geometry.type === 'RingGeometry') {
                    child.material.opacity = 0.2 + Math.sin(time) * 0.05;
                }
            });
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        console.log('MineTracker Pro - Enterprise Ready');
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
