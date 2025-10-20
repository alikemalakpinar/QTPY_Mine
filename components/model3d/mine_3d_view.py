# components/model3d/advanced_3d_twin.py - WebGL + Three.js Integration
import json
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import *

class Advanced3DMineVisualization(QWebEngineView):
    """Advanced 3D visualization using Three.js"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.personnel_data = []
        self.equipment_data = []
        self.load_3d_scene()
        
    def load_3d_scene(self):
        """Load Three.js 3D scene"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>MineGuard 3D Digital Twin</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #0a0a0a; overflow: hidden; }
        #container { width: 100vw; height: 100vh; }
        #ui-overlay {
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            background: rgba(0,0,0,0.7);
            padding: 15px;
            border-radius: 10px;
            z-index: 1000;
        }
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .active { background-color: #28a745; }
        .warning { background-color: #ffc107; }
        .danger { background-color: #dc3545; }
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="ui-overlay">
        <h3>🏔️ MineGuard Digital Twin</h3>
        <div><span class="status-indicator active"></span>Personnel: <span id="personnel-count">147</span></div>
        <div><span class="status-indicator active"></span>Equipment: <span id="equipment-count">58</span></div>
        <div><span class="status-indicator warning"></span>Alerts: <span id="alert-count">3</span></div>
        <br>
        <div>🎮 Controls:</div>
        <div>• Mouse: Rotate view</div>
        <div>• Wheel: Zoom</div>
        <div>• Arrow keys: Move</div>
    </div>

    <script>
        class MineGuard3D {
            constructor() {
                this.scene = new THREE.Scene();
                this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
                this.renderer = new THREE.WebGLRenderer({ antialias: true });
                this.personnel = [];
                this.equipment = [];
                
                this.init();
                this.createMineStructure();
                this.createLighting();
                this.addPersonnel();
                this.addEquipment();
                this.animate();
                this.addControls();
            }
            
            init() {
                this.renderer.setSize(window.innerWidth, window.innerHeight);
                this.renderer.setClearColor(0x001122);
                this.renderer.shadowMap.enabled = true;
                this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                document.getElementById('container').appendChild(this.renderer.domElement);
                
                this.camera.position.set(0, 200, 300);
                this.camera.lookAt(0, 0, 0);
            }
            
            createMineStructure() {
                // Mine terrain
                const terrainGeometrsdadsasdy = new THREE.PlaneGeometry(1000, 1000, 50, 50);
                const terrainMaterial = new THREE.MeshLambertMaterial({ 
                    color: 0x4a4a2a,
                    wireframe: false 
                });
                
                // Add height variations
                const vertices = terrainGeometry.attributes.position.array;
                for (let i = 0; i < vertices.length; i += 3) {
                    vertices[i + 2] = Math.sin(vertices[i] * 0.01) * Math.cos(vertices[i + 1] * 0.01) * 20;
                }
                terrainGeometry.attributes.position.needsUpdate = true;
                terrainGeometry.computeVertexNormals();
                
                const terrain = new THREE.Mesh(terrainGeometry, terrainMaterial);
                terrain.rotation.x = -Math.PI / 2;
                terrain.receiveShadow = true;
                this.scene.add(terrain);
                
                // Mine tunnels
                this.createTunnels();
                
                // Processing buildings
                this.createBuildings();
                
                // Safety zones
                this.createSafetyZones();
            }
            
            createTunnels() {
                const tunnelMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x666666,
                    transparent: true,
                    opacity: 0.8 
                });
                
                // Main horizontal tunnels
                const tunnelGeometry = new THREE.CylinderGeometry(5, 5, 400, 16);
                
                for (let i = 0; i < 5; i++) {
                    const tunnel = new THREE.Mesh(tunnelGeometry, tunnelMaterial);
                    tunnel.rotation.z = Math.PI / 2;
                    tunnel.position.set(0, 10, (i - 2) * 100);
                    tunnel.castShadow = true;
                    this.scene.add(tunnel);
                }
                
                // Vertical shafts
                const shaftGeometry = new THREE.CylinderGeometry(8, 8, 100, 16);
                const shaft = new THREE.Mesh(shaftGeometry, tunnelMaterial);
                shaft.position.set(0, -40, 0);
                shaft.castShadow = true;
                this.scene.add(shaft);
            }
            
            createBuildings() {
                // Processing plant
                const buildingGeometry = new THREE.BoxGeometry(60, 40, 40);
                const buildingMaterial = new THREE.MeshPhongMaterial({ color: 0x8b4513 });
                
                const processingPlant = new THREE.Mesh(buildingGeometry, buildingMaterial);
                processingPlant.position.set(-200, 20, 100);
                processingPlant.castShadow = true;
                processingPlant.receiveShadow = true;
                this.scene.add(processingPlant);
                
                // Workshop
                const workshop = new THREE.Mesh(buildingGeometry, buildingMaterial);
                workshop.position.set(200, 20, 150);
                workshop.castShadow = true;
                workshop.receiveShadow = true;
                this.scene.add(workshop);
                
                // Control tower
                const towerGeometry = new THREE.CylinderGeometry(8, 12, 60, 12);
                const towerMaterial = new THREE.MeshPhongMaterial({ color: 0x4682b4 });
                const controlTower = new THREE.Mesh(towerGeometry, towerMaterial);
                controlTower.position.set(0, 30, 0);
                controlTower.castShadow = true;
                this.scene.add(controlTower);
            }
            
            createSafetyZones() {
                const zones = [
                    { name: 'Safe Zone', color: 0x00ff00, position: [0, 1, 0], radius: 80 },
                    { name: 'Caution Zone', color: 0xffff00, position: [-150, 1, -100], radius: 60 },
                    { name: 'Restricted Zone', color: 0xff0000, position: [150, 1, 100], radius: 50 }
                ];
                
                zones.forEach(zone => {
                    const geometry = new THREE.RingGeometry(zone.radius - 5, zone.radius, 32);
                    const material = new THREE.MeshBasicMaterial({ 
                        color: zone.color,
                        transparent: true,
                        opacity: 0.3,
                        side: THREE.DoubleSide
                    });
                    
                    const ring = new THREE.Mesh(geometry, material);
                    ring.rotation.x = -Math.PI / 2;
                    ring.position.set(...zone.position);
                    this.scene.add(ring);
                });
            }
            
            createLighting() {
                // Ambient light
                const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
                this.scene.add(ambientLight);
                
                // Directional light (sun)
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(200, 300, 100);
                directionalLight.castShadow = true;
                directionalLight.shadow.mapSize.width = 2048;
                directionalLight.shadow.mapSize.height = 2048;
                directionalLight.shadow.camera.near = 0.5;
                directionalLight.shadow.camera.far = 1000;
                directionalLight.shadow.camera.left = -300;
                directionalLight.shadow.camera.right = 300;
                directionalLight.shadow.camera.top = 300;
                directionalLight.shadow.camera.bottom = -300;
                this.scene.add(directionalLight);
                
                // Spotlights for dramatic effect
                const spotlight = new THREE.SpotLight(0xffffff, 0.5);
                spotlight.position.set(0, 200, 0);
                spotlight.target.position.set(0, 0, 0);
                spotlight.castShadow = true;
                this.scene.add(spotlight);
                this.scene.add(spotlight.target);
            }
            
            addPersonnel() {
                const personnelGeometry = new THREE.SphereGeometry(2, 8, 6);
                
                for (let i = 0; i < 147; i++) {
                    const status = Math.random();
                    let color = 0x00ff00; // Green for active
                    
                    if (status > 0.8) color = 0xffff00; // Yellow for break
                    if (status > 0.9) color = 0xff0000; // Red for emergency
                    
                    const material = new THREE.MeshPhongMaterial({ color: color });
                    const person = new THREE.Mesh(personnelGeometry, material);
                    
                    // Random positions within mine area
                    person.position.set(
                        (Math.random() - 0.5) * 400,
                        5 + Math.random() * 10,
                        (Math.random() - 0.5) * 400
                    );
                    
                    person.castShadow = true;
                    person.userData = {
                        type: 'personnel',
                        id: `W-${String(i + 1).padStart(3, '0')}`,
                        status: status > 0.9 ? 'emergency' : status > 0.8 ? 'break' : 'active'
                    };
                    
                    this.personnel.push(person);
                    this.scene.add(person);
                }
            }
            
            addEquipment() {
                const equipmentTypes = [
                    { geometry: new THREE.BoxGeometry(12, 8, 20), color: 0xffa500, name: 'Excavator' },
                    { geometry: new THREE.BoxGeometry(10, 6, 16), color: 0x4169e1, name: 'Loader' },
                    { geometry: new THREE.BoxGeometry(8, 10, 24), color: 0x32cd32, name: 'Truck' },
                    { geometry: new THREE.ConeGeometry(4, 15, 8), color: 0xff4500, name: 'Drill' }
                ];
                
                for (let i = 0; i < 58; i++) {
                    const type = equipmentTypes[i % equipmentTypes.length];
                    const material = new THREE.MeshPhongMaterial({ color: type.color });
                    const equipment = new THREE.Mesh(type.geometry, material);
                    
                    equipment.position.set(
                        (Math.random() - 0.5) * 600,
                        10,
                        (Math.random() - 0.5) * 600
                    );
                    
                    equipment.rotation.y = Math.random() * Math.PI * 2;
                    equipment.castShadow = true;
                    equipment.receiveShadow = true;
                    
                    equipment.userData = {
                        type: 'equipment',
                        id: `EQ-${String(i + 1).padStart(3, '0')}`,
                        name: type.name,
                        status: Math.random() > 0.1 ? 'operational' : 'maintenance'
                    };
                    
                    this.equipment.push(equipment);
                    this.scene.add(equipment);
                }
            }
            
            addControls() {
                this.mouseX = 0;
                this.mouseY = 0;
                this.isMouseDown = false;
                
                const container = this.renderer.domElement;
                
                container.addEventListener('mousedown', (e) => {
                    this.isMouseDown = true;
                    this.mouseX = e.clientX;
                    this.mouseY = e.clientY;
                });
                
                container.addEventListener('mouseup', () => {
                    this.isMouseDown = false;
                });
                
                container.addEventListener('mousemove', (e) => {
                    if (this.isMouseDown) {
                        const deltaX = e.clientX - this.mouseX;
                        const deltaY = e.clientY - this.mouseY;
                        
                        // Rotate camera around center
                        const spherical = new THREE.Spherical();
                        spherical.setFromVector3(this.camera.position);
                        spherical.theta -= deltaX * 0.01;
                        spherical.phi += deltaY * 0.01;
                        spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi));
                        
                        this.camera.position.setFromSpherical(spherical);
                        this.camera.lookAt(0, 0, 0);
                        
                        this.mouseX = e.clientX;
                        this.mouseY = e.clientY;
                    }
                });
                
                container.addEventListener('wheel', (e) => {
                    const scale = e.deltaY > 0 ? 1.1 : 0.9;
                    this.camera.position.multiplyScalar(scale);
                });
                
                // Keyboard controls
                window.addEventListener('keydown', (e) => {
                    const speed = 10;
                    switch(e.code) {
                        case 'ArrowUp':
                            this.camera.position.z -= speed;
                            break;
                        case 'ArrowDown':
                            this.camera.position.z += speed;
                            break;
                        case 'ArrowLeft':
                            this.camera.position.x -= speed;
                            break;
                        case 'ArrowRight':
                            this.camera.position.x += speed;
                            break;
                    }
                    this.camera.lookAt(0, 0, 0);
                });
            }
            
            animate() {
                requestAnimationFrame(() => this.animate());
                
                // Animate personnel movement
                this.personnel.forEach((person, index) => {
                    if (Math.random() < 0.01) { // 1% chance to move each frame
                        person.position.x += (Math.random() - 0.5) * 2;
                        person.position.z += (Math.random() - 0.5) * 2;
                        
                        // Keep within bounds
                        person.position.x = Math.max(-400, Math.min(400, person.position.x));
                        person.position.z = Math.max(-400, Math.min(400, person.position.z));
                    }
                    
                    // Subtle animation
                    person.position.y = 5 + Math.sin(Date.now() * 0.001 + index) * 0.5;
                });
                
                // Animate equipment
                this.equipment.forEach((equipment, index) => {
                    if (equipment.userData.status === 'operational') {
                        equipment.rotation.y += 0.01;
                    }
                });
                
                this.renderer.render(this.scene, this.camera);
            }
            
            updateData(personnelData, equipmentData) {
                // Update real-time data from Python backend
                document.getElementById('personnel-count').textContent = personnelData.length;
                document.getElementById('equipment-count').textContent = equipmentData.length;
            }
        }
        
        // Initialize the 3D scene
        window.mineGuard3D = new MineGuard3D();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            window.mineGuard3D.camera.aspect = window.innerWidth / window.innerHeight;
            window.mineGuard3D.camera.updateProjectionMatrix();
            window.mineGuard3D.renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        // Expose functions for Python communication
        window.updateMineData = function(data) {
            window.mineGuard3D.updateData(data.personnel, data.equipment);
        };
    </script>
</body>
</html>
        """
        
        self.setHtml(html_content)
        
    def update_mine_data(self, personnel_data, equipment_data):
        """Update 3D visualization with real-time data"""
        data = {
            'personnel': personnel_data,
            'equipment': equipment_data
        }
        
        # Execute JavaScript to update the 3D scene
        self.page().runJavaScript(
            f"window.updateMineData({json.dumps(data)});"
        )