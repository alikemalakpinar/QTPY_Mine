"""Premium 3D Mine Visualization - Cinematic Quality with Advanced Effects"""
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
    """Premium cinematic 3D mine visualization with SOS camera zoom"""

    def __init__(self, tracking_service):
        super().__init__()
        self.tracking = tracking_service
        self.setMinimumSize(800, 600)

        if not WEBENGINE_AVAILABLE:
            self.show_placeholder()
        else:
            self.load_3d_scene()
            self.tracking.location_updated.connect(self.update_position)
            self.tracking.emergency_signal.connect(self.on_emergency)
            QTimer.singleShot(2000, self.load_all_positions)

    def show_placeholder(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("3D Visualization\n\nQtWebEngine required\npip install PyQt6-WebEngine")
        label.setStyleSheet("color: #8b949e; font-size: 14px; padding: 40px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

    def load_3d_scene(self):
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MineTracker 3D Pro - Cinematic Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #05070a 0%, #0a0e14 100%);
            overflow: hidden;
            font-family: 'SF Pro Display', 'Inter', -apple-system, 'Segoe UI', sans-serif;
        }
        #container { width: 100vw; height: 100vh; }

        .glass-panel {
            position: absolute;
            background: linear-gradient(135deg, rgba(13, 17, 23, 0.95) 0%, rgba(22, 27, 34, 0.9) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(88, 166, 255, 0.15);
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }

        .info-panel {
            top: 24px;
            left: 24px;
            padding: 24px;
            min-width: 300px;
        }

        .panel-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }

        .panel-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .panel-title-group {
            flex: 1;
        }

        .panel-title {
            font-size: 20px;
            font-weight: 800;
            color: #f0f6fc;
            letter-spacing: -0.5px;
        }

        .panel-subtitle {
            font-size: 12px;
            color: #58a6ff;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(33, 38, 45, 0.8) 0%, rgba(22, 27, 34, 0.8) 100%);
            border-radius: 14px;
            padding: 16px;
            border: 1px solid rgba(48, 54, 61, 0.5);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            border-color: rgba(88, 166, 255, 0.3);
            transform: translateY(-2px);
        }

        .stat-value {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            font-size: 11px;
            color: #8b949e;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }

        .legend {
            top: 24px;
            right: 24px;
            padding: 20px;
            min-width: 200px;
        }

        .legend-title {
            font-size: 13px;
            font-weight: 700;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 16px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(48, 54, 61, 0.3);
        }

        .legend-item:last-child {
            border-bottom: none;
        }

        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 14px;
            box-shadow: 0 0 20px currentColor;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
        }

        .legend-text {
            font-size: 13px;
            color: #f0f6fc;
            font-weight: 500;
        }

        .controls-panel {
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            padding: 16px 32px;
            display: flex;
            gap: 32px;
        }

        .control-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .control-key {
            background: linear-gradient(135deg, rgba(88, 166, 255, 0.2) 0%, rgba(163, 113, 247, 0.2) 100%);
            padding: 6px 12px;
            border-radius: 8px;
            color: #58a6ff;
            font-weight: 700;
            font-size: 12px;
            border: 1px solid rgba(88, 166, 255, 0.3);
        }

        .control-text {
            color: #8b949e;
            font-size: 12px;
        }

        .zone-indicator {
            bottom: 100px;
            right: 24px;
            padding: 16px 20px;
            min-width: 180px;
        }

        .zone-label {
            font-size: 10px;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .zone-name {
            font-size: 18px;
            font-weight: 700;
            color: #f0f6fc;
        }

        .zone-status {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #3fb950;
            box-shadow: 0 0 10px #3fb950;
        }

        .status-text {
            font-size: 12px;
            color: #3fb950;
            font-weight: 600;
        }

        /* Loading animation */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #05070a 0%, #0a0e14 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            transition: opacity 0.5s ease;
        }

        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(88, 166, 255, 0.1);
            border-top: 3px solid #58a6ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .loading-text {
            margin-top: 24px;
            color: #8b949e;
            font-size: 14px;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div id="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <div class="loading-text">Initializing 3D Scene...</div>
    </div>

    <div id="container"></div>

    <div class="glass-panel info-panel">
        <div class="panel-header">
            <div class="panel-icon">⛏️</div>
            <div class="panel-title-group">
                <div class="panel-title">Mine Status</div>
                <div class="panel-subtitle">REAL-TIME MONITORING</div>
            </div>
        </div>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-value" id="personnel-count">0</div>
                <div class="stat-label">Personnel</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">6</div>
                <div class="stat-label">Anchors</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">12</div>
                <div class="stat-label">Galleries</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">6</div>
                <div class="stat-label">Chambers</div>
            </div>
        </div>
    </div>

    <div class="glass-panel legend">
        <div class="legend-title">Map Legend</div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #3fb950; color: #3fb950;"></div>
            <span class="legend-text">Personnel</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #58a6ff; color: #58a6ff;"></div>
            <span class="legend-text">Anchor Device</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #a371f7; color: #a371f7;"></div>
            <span class="legend-text">Main Gallery</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #d29922; color: #d29922;"></div>
            <span class="legend-text">Work Chamber</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: #f85149; color: #f85149;"></div>
            <span class="legend-text">Emergency</span>
        </div>
    </div>

    <div class="glass-panel controls-panel">
        <div class="control-item">
            <span class="control-key">🖱️ Drag</span>
            <span class="control-text">Rotate View</span>
        </div>
        <div class="control-item">
            <span class="control-key">⚲ Scroll</span>
            <span class="control-text">Zoom</span>
        </div>
        <div class="control-item">
            <span class="control-key">W A S D</span>
            <span class="control-text">Move Camera</span>
        </div>
        <div class="control-item">
            <span class="control-key">R</span>
            <span class="control-text">Reset View</span>
        </div>
    </div>

    <div class="glass-panel zone-indicator">
        <div class="zone-label">Current View</div>
        <div class="zone-name" id="current-zone">Main Shaft</div>
        <div class="zone-status">
            <div class="status-dot"></div>
            <span class="status-text">Active</span>
        </div>
    </div>

    <script>
        // Hide loading after scene is ready
        setTimeout(() => {
            document.getElementById('loading').style.opacity = '0';
            setTimeout(() => {
                document.getElementById('loading').style.display = 'none';
            }, 500);
        }, 1500);

        // Scene setup
        const scene = new THREE.Scene();

        // Create gradient background
        const canvas = document.createElement('canvas');
        canvas.width = 2;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 512);
        gradient.addColorStop(0, '#0a0e14');
        gradient.addColorStop(0.5, '#05070a');
        gradient.addColorStop(1, '#0d1117');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 2, 512);
        const backgroundTexture = new THREE.CanvasTexture(canvas);
        scene.background = backgroundTexture;

        // Enhanced fog for depth
        scene.fog = new THREE.FogExp2(0x05070a, 0.0006);

        const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 4000);
        camera.position.set(0, 500, 800);

        const renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        renderer.outputEncoding = THREE.sRGBEncoding;
        document.getElementById('container').appendChild(renderer.domElement);

        // Enhanced Lighting System
        const ambientLight = new THREE.AmbientLight(0x1a2030, 0.4);
        scene.add(ambientLight);

        // Main directional light with shadows
        const mainLight = new THREE.DirectionalLight(0xffffff, 0.6);
        mainLight.position.set(300, 600, 300);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 4096;
        mainLight.shadow.mapSize.height = 4096;
        mainLight.shadow.camera.near = 100;
        mainLight.shadow.camera.far = 2000;
        mainLight.shadow.camera.left = -800;
        mainLight.shadow.camera.right = 800;
        mainLight.shadow.camera.top = 800;
        mainLight.shadow.camera.bottom = -800;
        mainLight.shadow.bias = -0.0001;
        scene.add(mainLight);

        // Rim light for dramatic effect
        const rimLight = new THREE.DirectionalLight(0x58a6ff, 0.3);
        rimLight.position.set(-200, 200, -200);
        scene.add(rimLight);

        // Fill light
        const fillLight = new THREE.DirectionalLight(0xa371f7, 0.15);
        fillLight.position.set(200, 100, -300);
        scene.add(fillLight);

        // Ground plane with premium material
        const groundGeometry = new THREE.PlaneGeometry(3000, 3000, 100, 100);
        const vertices = groundGeometry.attributes.position.array;
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i + 2] = Math.random() * 2 - 1;
        }
        groundGeometry.computeVertexNormals();

        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0x0d1117,
            roughness: 0.95,
            metalness: 0.05,
            envMapIntensity: 0.5
        });

        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        scene.add(ground);

        // Premium grid with gradient effect
        const gridSize = 2500;
        const gridDivisions = 50;

        // Create custom grid with fade effect
        const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, 0x21262d, 0x161b22);
        gridHelper.position.y = 0.5;
        gridHelper.material.opacity = 0.4;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);

        // Particle system for ambient atmosphere
        const particleCount = 500;
        const particleGeometry = new THREE.BufferGeometry();
        const particlePositions = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            particlePositions[i] = (Math.random() - 0.5) * 2000;
            particlePositions[i + 1] = Math.random() * 300 + 10;
            particlePositions[i + 2] = (Math.random() - 0.5) * 2000;
        }

        particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

        const particleMaterial = new THREE.PointsMaterial({
            color: 0x58a6ff,
            size: 2,
            transparent: true,
            opacity: 0.3,
            sizeAttenuation: true
        });

        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);

        // ===============================
        // MAIN SHAFT - Premium Design
        // ===============================
        function createMainShaft() {
            const shaftGroup = new THREE.Group();

            // Base platform with emission
            const platformGeometry = new THREE.CylinderGeometry(70, 75, 12, 64);
            const platformMaterial = new THREE.MeshStandardMaterial({
                color: 0x161b22,
                roughness: 0.4,
                metalness: 0.8,
                emissive: 0x58a6ff,
                emissiveIntensity: 0.05
            });
            const platform = new THREE.Mesh(platformGeometry, platformMaterial);
            platform.position.y = 6;
            platform.castShadow = true;
            platform.receiveShadow = true;
            shaftGroup.add(platform);

            // Glowing ring
            const ringGeometry = new THREE.TorusGeometry(68, 5, 32, 128);
            const ringMaterial = new THREE.MeshStandardMaterial({
                color: 0x58a6ff,
                emissive: 0x58a6ff,
                emissiveIntensity: 0.8,
                metalness: 0.9,
                roughness: 0.1,
                transparent: true,
                opacity: 0.9
            });
            const ring = new THREE.Mesh(ringGeometry, ringMaterial);
            ring.position.y = 6;
            ring.rotation.x = Math.PI / 2;
            shaftGroup.add(ring);

            // Outer decorative ring
            const outerRing = new THREE.Mesh(
                new THREE.TorusGeometry(78, 2, 16, 64),
                new THREE.MeshStandardMaterial({
                    color: 0xa371f7,
                    emissive: 0xa371f7,
                    emissiveIntensity: 0.5,
                    metalness: 0.8,
                    roughness: 0.2
                })
            );
            outerRing.position.y = 6;
            outerRing.rotation.x = Math.PI / 2;
            shaftGroup.add(outerRing);

            // Central pillar with glow
            const pillarGeometry = new THREE.CylinderGeometry(4, 4, 100, 16);
            const pillarMaterial = new THREE.MeshStandardMaterial({
                color: 0x58a6ff,
                emissive: 0x58a6ff,
                emissiveIntensity: 0.6,
                metalness: 0.7,
                roughness: 0.3
            });
            const pillar = new THREE.Mesh(pillarGeometry, pillarMaterial);
            pillar.position.y = 50;
            shaftGroup.add(pillar);

            // Point light at shaft
            const shaftLight = new THREE.PointLight(0x58a6ff, 2, 200);
            shaftLight.position.y = 50;
            shaftGroup.add(shaftLight);

            // Holographic rings around pillar
            for (let i = 1; i <= 3; i++) {
                const holoRing = new THREE.Mesh(
                    new THREE.TorusGeometry(12 + i * 6, 0.5, 8, 32),
                    new THREE.MeshBasicMaterial({
                        color: 0x58a6ff,
                        transparent: true,
                        opacity: 0.3 / i
                    })
                );
                holoRing.position.y = 30 + i * 20;
                holoRing.rotation.x = Math.PI / 2;
                holoRing.userData.floatOffset = i * 0.5;
                shaftGroup.add(holoRing);
            }

            return shaftGroup;
        }

        const mainShaft = createMainShaft();
        scene.add(mainShaft);

        // ===============================
        // GALLERIES - Premium Design
        // ===============================
        function createGallery(startX, startZ, endX, endZ, width = 24, color = 0xa371f7) {
            const gallery = new THREE.Group();

            const length = Math.sqrt((endX - startX)**2 + (endZ - startZ)**2);
            const angle = Math.atan2(endZ - startZ, endX - startX);
            const midX = (startX + endX) / 2;
            const midZ = (startZ + endZ) / 2;

            // Gallery floor with gradient effect
            const floorGeometry = new THREE.BoxGeometry(length, 3, width);
            const floorMaterial = new THREE.MeshStandardMaterial({
                color: 0x161b22,
                roughness: 0.7,
                metalness: 0.3
            });
            const floor = new THREE.Mesh(floorGeometry, floorMaterial);
            floor.position.set(midX, 1.5, midZ);
            floor.rotation.y = angle;
            floor.receiveShadow = true;
            gallery.add(floor);

            // Rails with emission
            const railMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.4,
                metalness: 0.9,
                roughness: 0.2
            });

            for (let side of [-1, 1]) {
                const rail = new THREE.Mesh(
                    new THREE.BoxGeometry(length, 4, 2),
                    railMaterial
                );
                const offsetX = Math.sin(angle) * (width / 2 - 1) * side;
                const offsetZ = -Math.cos(angle) * (width / 2 - 1) * side;
                rail.position.set(midX + offsetX, 3, midZ + offsetZ);
                rail.rotation.y = angle;
                rail.castShadow = true;
                gallery.add(rail);
            }

            // Gallery lights
            const numLights = Math.max(2, Math.floor(length / 80));
            for (let i = 0; i <= numLights; i++) {
                const t = i / numLights;
                const x = startX + (endX - startX) * t;
                const z = startZ + (endZ - startZ) * t;

                // Light fixture
                const fixtureGeometry = new THREE.SphereGeometry(2, 16, 16);
                const fixtureMaterial = new THREE.MeshStandardMaterial({
                    color: color,
                    emissive: color,
                    emissiveIntensity: 1
                });
                const fixture = new THREE.Mesh(fixtureGeometry, fixtureMaterial);
                fixture.position.set(x, 25, z);
                gallery.add(fixture);

                // Point light
                const light = new THREE.PointLight(color, 0.8, 100);
                light.position.set(x, 25, z);
                gallery.add(light);
            }

            return gallery;
        }

        // Main galleries
        const galleries = [
            { start: [0, 0], end: [-400, -250], color: 0x3fb950 },   // Sector A
            { start: [0, 0], end: [400, -250], color: 0xd29922 },    // Sector B
            { start: [0, 0], end: [0, 350], color: 0xa371f7 },       // Sector C
            { start: [0, 0], end: [-300, 400], color: 0xf778ba },    // Processing
            { start: [0, 0], end: [300, 400], color: 0x39d2c0 }      // Workshop
        ];

        galleries.forEach(g => {
            const gallery = createGallery(g.start[0], g.start[1], g.end[0], g.end[1], 26, g.color);
            scene.add(gallery);
        });

        // Connection galleries
        const connections = [
            { start: [-400, -250], end: [400, -250], color: 0x58a6ff },
            { start: [-300, 400], end: [300, 400], color: 0x39d2c0 }
        ];

        connections.forEach(g => {
            const gallery = createGallery(g.start[0], g.start[1], g.end[0], g.end[1], 22, g.color);
            scene.add(gallery);
        });

        // ===============================
        // WORKING CHAMBERS - Premium Design
        // ===============================
        function createWorkingChamber(x, z, size, color, name) {
            const chamber = new THREE.Group();
            chamber.userData.name = name;

            // Main platform
            const platformGeometry = new THREE.BoxGeometry(size, 6, size);
            const platformMaterial = new THREE.MeshStandardMaterial({
                color: 0x161b22,
                roughness: 0.5,
                metalness: 0.5,
                emissive: color,
                emissiveIntensity: 0.02
            });
            const platform = new THREE.Mesh(platformGeometry, platformMaterial);
            platform.position.set(x, 3, z);
            platform.castShadow = true;
            platform.receiveShadow = true;
            chamber.add(platform);

            // Border walls with glow
            const borderMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.5,
                metalness: 0.8,
                roughness: 0.2
            });

            const wallHeight = 8;
            const wallThickness = 3;

            // Four walls
            const walls = [
                { pos: [x, wallHeight/2, z - size/2 + wallThickness/2], size: [size, wallHeight, wallThickness] },
                { pos: [x, wallHeight/2, z + size/2 - wallThickness/2], size: [size, wallHeight, wallThickness] },
                { pos: [x - size/2 + wallThickness/2, wallHeight/2, z], size: [wallThickness, wallHeight, size] },
                { pos: [x + size/2 - wallThickness/2, wallHeight/2, z], size: [wallThickness, wallHeight, size] }
            ];

            walls.forEach(w => {
                const wall = new THREE.Mesh(
                    new THREE.BoxGeometry(...w.size),
                    borderMaterial
                );
                wall.position.set(...w.pos);
                wall.castShadow = true;
                chamber.add(wall);
            });

            // Corner accent lights
            const corners = [
                [x - size/2 + 5, z - size/2 + 5],
                [x + size/2 - 5, z - size/2 + 5],
                [x - size/2 + 5, z + size/2 - 5],
                [x + size/2 - 5, z + size/2 - 5]
            ];

            corners.forEach(([cx, cz]) => {
                const cornerLight = new THREE.Mesh(
                    new THREE.SphereGeometry(2, 16, 16),
                    new THREE.MeshStandardMaterial({
                        color: color,
                        emissive: color,
                        emissiveIntensity: 1
                    })
                );
                cornerLight.position.set(cx, 10, cz);
                chamber.add(cornerLight);
            });

            // Central area light
            const areaLight = new THREE.PointLight(color, 1.5, 120);
            areaLight.position.set(x, 40, z);
            chamber.add(areaLight);

            // Central marker pillar
            const markerGeometry = new THREE.CylinderGeometry(3, 3, 60, 12);
            const markerMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.7,
                metalness: 0.6,
                roughness: 0.4
            });
            const marker = new THREE.Mesh(markerGeometry, markerMaterial);
            marker.position.set(x, 30, z);
            chamber.add(marker);

            return chamber;
        }

        // Create chambers
        const chambers = [
            { name: 'Main Shaft', x: 0, z: 0, size: 90, color: 0x58a6ff },
            { name: 'Sector A', x: -400, z: -250, size: 80, color: 0x3fb950 },
            { name: 'Sector B', x: 400, z: -250, size: 80, color: 0xd29922 },
            { name: 'Sector C', x: 0, z: 350, size: 80, color: 0xa371f7 },
            { name: 'Processing', x: -300, z: 400, size: 75, color: 0xf778ba },
            { name: 'Workshop', x: 300, z: 400, size: 75, color: 0x39d2c0 }
        ];

        const chamberObjects = [];
        chambers.forEach(c => {
            const chamber = createWorkingChamber(c.x, c.z, c.size, c.color, c.name);
            chamberObjects.push({ mesh: chamber, data: c });
            scene.add(chamber);
        });

        // ===============================
        // ANCHOR DEVICES - Premium Design
        // ===============================
        function createAnchor(x, z, color) {
            const anchor = new THREE.Group();

            // Main body
            const bodyGeometry = new THREE.CylinderGeometry(6, 8, 22, 24);
            const bodyMaterial = new THREE.MeshStandardMaterial({
                color: 0x21262d,
                metalness: 0.9,
                roughness: 0.2
            });
            const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
            body.castShadow = true;
            anchor.add(body);

            // LED indicator with glow
            const ledGeometry = new THREE.SphereGeometry(3.5, 24, 24);
            const ledMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 1.2,
                metalness: 0.4,
                roughness: 0.3
            });
            const led = new THREE.Mesh(ledGeometry, ledMaterial);
            led.position.y = 9;
            anchor.add(led);

            // Antenna
            const antennaGeometry = new THREE.CylinderGeometry(0.6, 0.6, 18, 8);
            const antennaMaterial = new THREE.MeshStandardMaterial({
                color: 0x484f58,
                metalness: 0.95,
                roughness: 0.1
            });
            const antenna = new THREE.Mesh(antennaGeometry, antennaMaterial);
            antenna.position.y = 20;
            anchor.add(antenna);

            // Antenna tip
            const tipGeometry = new THREE.SphereGeometry(1.2, 16, 16);
            const tipMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.8
            });
            const tip = new THREE.Mesh(tipGeometry, tipMaterial);
            tip.position.y = 30;
            anchor.add(tip);

            // Signal waves with animation support
            for (let i = 1; i <= 4; i++) {
                const waveGeometry = new THREE.TorusGeometry(12 * i, 0.6, 8, 48);
                const waveMaterial = new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.15 / i
                });
                const wave = new THREE.Mesh(waveGeometry, waveMaterial);
                wave.position.y = 20;
                wave.rotation.x = Math.PI / 2;
                wave.userData.waveIndex = i;
                anchor.add(wave);
            }

            // Point light
            const anchorLight = new THREE.PointLight(color, 0.8, 80);
            anchorLight.position.y = 15;
            anchor.add(anchorLight);

            anchor.position.set(x, 12, z);
            return anchor;
        }

        // Create anchors at chambers
        const anchors = [];
        chambers.forEach(c => {
            const anchor = createAnchor(c.x, c.z, c.color);
            anchors.push(anchor);
            scene.add(anchor);
        });

        // ===============================
        // PERSONNEL TAGS
        // ===============================
        const personnel = new Map();

        function createPersonnelTag(color) {
            const group = new THREE.Group();

            // Main sphere with glow
            const tagGeometry = new THREE.SphereGeometry(5, 32, 32);
            const tagMaterial = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.6,
                roughness: 0.3,
                metalness: 0.4
            });
            const tag = new THREE.Mesh(tagGeometry, tagMaterial);
            tag.castShadow = true;
            group.add(tag);

            // Outer glow
            const glowGeometry = new THREE.SphereGeometry(8, 24, 24);
            const glowMaterial = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.15
            });
            const glow = new THREE.Mesh(glowGeometry, glowMaterial);
            group.add(glow);

            // Vertical beam
            const beamGeometry = new THREE.CylinderGeometry(0.4, 0.4, 50, 8);
            const beamMaterial = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.15
            });
            const beam = new THREE.Mesh(beamGeometry, beamMaterial);
            beam.position.y = 25;
            group.add(beam);

            // Ring indicator
            const ringGeometry = new THREE.TorusGeometry(7, 0.3, 8, 32);
            const ringMaterial = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.4
            });
            const ring = new THREE.Mesh(ringGeometry, ringMaterial);
            ring.rotation.x = Math.PI / 2;
            ring.position.y = 0.5;
            group.add(ring);

            return group;
        }

        window.updateEntity = function(data) {
            const { id, type, location, status } = data;

            if (type !== 'personnel') return;

            if (!personnel.has(id)) {
                const color = status === 'emergency' ? 0xf85149 : 0x3fb950;
                const tag = createPersonnelTag(color);
                personnel.set(id, tag);
                scene.add(tag);
            }

            const tag = personnel.get(id);
            tag.position.set(location.x, Math.abs(location.z) + 12, location.y);

            if (status === 'emergency') {
                tag.children[0].material.color.setHex(0xf85149);
                tag.children[0].material.emissive.setHex(0xf85149);
            }
        };

        window.updateCounts = function(count) {
            document.getElementById('personnel-count').textContent = count;
        };

        // Cinematic camera zoom to emergency location
        window.cinematicZoomTo = function(x, y, z) {
            const targetX = x || 0;
            const targetZ = y || 0;  // y maps to z in 3D
            const targetY = Math.abs(z || 0) + 50;

            // Set camera target smoothly
            const startTarget = { x: cameraTarget.x, z: cameraTarget.z };
            const startDist = cameraDistance;
            const startElev = targetElevation;
            const duration = 1500; // ms
            const startTime = Date.now();

            function animateZoom() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease out cubic
                const ease = 1 - Math.pow(1 - progress, 3);

                cameraTarget.x = startTarget.x + (targetX - startTarget.x) * ease;
                cameraTarget.z = startTarget.z + (targetZ - startTarget.z) * ease;
                cameraDistance = startDist + (400 - startDist) * ease;
                targetElevation = startElev + (0.35 - startElev) * ease;

                if (progress < 1) {
                    requestAnimationFrame(animateZoom);
                }
            }
            animateZoom();

            // Flash red warning overlay
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(248, 81, 73, 0.2);
                pointer-events: none; z-index: 999;
                animation: emergencyFlash 0.6s ease-out 3;
            `;
            const style = document.createElement('style');
            style.textContent = `
                @keyframes emergencyFlash {
                    0% { opacity: 0; }
                    30% { opacity: 1; }
                    100% { opacity: 0; }
                }
            `;
            document.head.appendChild(style);
            document.body.appendChild(overlay);
            setTimeout(() => overlay.remove(), 2000);
        };

        // ===============================
        // CAMERA CONTROLS
        // ===============================
        let targetRotation = 0;
        let targetElevation = 0.45;
        let isMouseDown = false;
        let cameraDistance = 900;
        let cameraTarget = new THREE.Vector3(0, 0, 0);

        document.addEventListener('mousedown', (e) => {
            if (e.button === 0) isMouseDown = true;
        });
        document.addEventListener('mouseup', () => isMouseDown = false);
        document.addEventListener('mouseleave', () => isMouseDown = false);

        document.addEventListener('mousemove', (e) => {
            if (isMouseDown) {
                targetRotation += e.movementX * 0.004;
                targetElevation = Math.max(0.1, Math.min(0.85, targetElevation + e.movementY * 0.002));
            }
        });

        document.addEventListener('wheel', (e) => {
            cameraDistance += e.deltaY * 0.6;
            cameraDistance = Math.max(350, Math.min(1500, cameraDistance));
        });

        const keys = {};
        document.addEventListener('keydown', (e) => {
            keys[e.key.toLowerCase()] = true;
            if (e.key.toLowerCase() === 'r') {
                // Reset camera
                targetRotation = 0;
                targetElevation = 0.45;
                cameraDistance = 900;
                cameraTarget.set(0, 0, 0);
            }
        });
        document.addEventListener('keyup', (e) => keys[e.key.toLowerCase()] = false);

        // ===============================
        // ANIMATION LOOP
        // ===============================
        let time = 0;

        function animate() {
            requestAnimationFrame(animate);
            time += 0.008;

            // Smooth camera movement
            const cameraX = Math.sin(targetRotation) * cameraDistance;
            const cameraZ = Math.cos(targetRotation) * cameraDistance;
            const cameraY = 120 + targetElevation * 500;

            camera.position.x += (cameraX + cameraTarget.x - camera.position.x) * 0.04;
            camera.position.z += (cameraZ + cameraTarget.z - camera.position.z) * 0.04;
            camera.position.y += (cameraY - camera.position.y) * 0.04;

            // WASD movement
            const moveSpeed = 6;
            if (keys['w']) cameraTarget.z -= moveSpeed * Math.cos(targetRotation);
            if (keys['w']) cameraTarget.x -= moveSpeed * Math.sin(targetRotation);
            if (keys['s']) cameraTarget.z += moveSpeed * Math.cos(targetRotation);
            if (keys['s']) cameraTarget.x += moveSpeed * Math.sin(targetRotation);
            if (keys['a']) cameraTarget.x -= moveSpeed * Math.cos(targetRotation);
            if (keys['a']) cameraTarget.z += moveSpeed * Math.sin(targetRotation);
            if (keys['d']) cameraTarget.x += moveSpeed * Math.cos(targetRotation);
            if (keys['d']) cameraTarget.z -= moveSpeed * Math.sin(targetRotation);

            camera.lookAt(cameraTarget);

            // Animate particles
            const positions = particles.geometry.attributes.position.array;
            for (let i = 1; i < positions.length; i += 3) {
                positions[i] += 0.1;
                if (positions[i] > 300) positions[i] = 10;
            }
            particles.geometry.attributes.position.needsUpdate = true;

            // Animate anchor waves
            anchors.forEach(anchor => {
                anchor.children.forEach(child => {
                    if (child.userData.waveIndex) {
                        child.scale.setScalar(1 + Math.sin(time * 2 + child.userData.waveIndex) * 0.1);
                        child.material.opacity = (0.15 / child.userData.waveIndex) * (0.8 + Math.sin(time * 3) * 0.2);
                    }
                });
            });

            // Animate main shaft rings
            mainShaft.children.forEach(child => {
                if (child.userData.floatOffset !== undefined) {
                    child.rotation.z = time + child.userData.floatOffset;
                    child.position.y = 30 + child.userData.floatOffset * 20 + Math.sin(time + child.userData.floatOffset) * 3;
                }
            });

            // Animate personnel tags
            personnel.forEach(tag => {
                if (tag.children[3]) {
                    tag.children[3].rotation.z = time * 2;
                }
            });

            // Update current zone based on camera position
            const closestChamber = chamberObjects.reduce((closest, current) => {
                const dist = Math.sqrt(
                    Math.pow(cameraTarget.x - current.data.x, 2) +
                    Math.pow(cameraTarget.z - current.data.z, 2)
                );
                if (!closest || dist < closest.dist) {
                    return { chamber: current, dist: dist };
                }
                return closest;
            }, null);

            if (closestChamber && closestChamber.dist < 200) {
                document.getElementById('current-zone').textContent = closestChamber.chamber.data.name;
            } else {
                document.getElementById('current-zone').textContent = 'Overview';
            }

            renderer.render(scene, camera);
        }

        animate();

        // Handle window resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        console.log('✅ Premium 3D Mine Visualization Ready!');
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

    def on_emergency(self, data):
        """Cinematic camera zoom to emergency location"""
        if not WEBENGINE_AVAILABLE:
            return
        location = data.get('location', {})
        x = location.get('x', 0)
        y = location.get('y', 0)
        z = location.get('z', 0)
        js_code = f"window.cinematicZoomTo({x}, {y}, {z});"
        self.page().runJavaScript(js_code)

    def load_all_positions(self):
        if not WEBENGINE_AVAILABLE:
            return
        for person in self.tracking.get_personnel():
            self.update_position({'type': 'personnel', 'data': person})
        stats = self.tracking.get_statistics()
        js_code = f"window.updateCounts({stats['personnel']['total']});"
        self.page().runJavaScript(js_code)
