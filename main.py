#!/usr/bin/env python3
"""
MineTracker - Professional Underground Mining Personnel & Device Tracking System
Real-time location tracking with 3D visualization
Modular Architecture with Turkish/English Support
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.app import MineTrackerApp

class ModernTheme:
    """Modern dark theme with professional colors"""
    
    # Color Palette
    BACKGROUND = "#0F0F0F"
    SURFACE = "#1A1A1A"
    SURFACE_LIGHT = "#252525"
    PRIMARY = "#00D4FF"
    PRIMARY_DARK = "#0099CC"
    SUCCESS = "#00FF88"
    WARNING = "#FFB800"
    DANGER = "#FF3366"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    BORDER = "#2A2A2A"
    
    @staticmethod
    def get_app_style():
        return f"""
        QMainWindow {{
            background: {ModernTheme.BACKGROUND};
        }}
        
        QWidget {{
            background: {ModernTheme.BACKGROUND};
            color: {ModernTheme.TEXT_PRIMARY};
            font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif;
            font-size: 14px;
        }}
        
        QPushButton {{
            background: {ModernTheme.SURFACE_LIGHT};
            color: {ModernTheme.TEXT_PRIMARY};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
        }}
        
        QPushButton:hover {{
            background: {ModernTheme.PRIMARY_DARK};
            border-color: {ModernTheme.PRIMARY};
        }}
        
        QPushButton:pressed {{
            background: {ModernTheme.PRIMARY};
        }}
        
        QLabel {{
            color: {ModernTheme.TEXT_PRIMARY};
            background: transparent;
        }}
        
        QLineEdit, QComboBox {{
            background: {ModernTheme.SURFACE};
            color: {ModernTheme.TEXT_PRIMARY};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }}
        
        QLineEdit:focus, QComboBox:focus {{
            border-color: {ModernTheme.PRIMARY};
            outline: none;
        }}
        
        QTableWidget {{
            background: {ModernTheme.SURFACE};
            border: none;
            border-radius: 12px;
            gridline-color: {ModernTheme.BORDER};
        }}
        
        QTableWidget::item {{
            padding: 12px;
            border-bottom: 1px solid {ModernTheme.BORDER};
        }}
        
        QHeaderView::section {{
            background: {ModernTheme.SURFACE_LIGHT};
            color: {ModernTheme.TEXT_SECONDARY};
            border: none;
            padding: 12px;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
        }}
        
        QScrollBar:vertical {{
            background: {ModernTheme.SURFACE};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {ModernTheme.SURFACE_LIGHT};
            border-radius: 5px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {ModernTheme.PRIMARY_DARK};
        }}
        """


class Device:
    """Device/Tracker model"""
    def __init__(self, device_id, device_type, assigned_to, battery, location):
        self.id = device_id
        self.type = device_type  # "Personnel" or "Equipment"
        self.assigned_to = assigned_to
        self.battery = battery
        self.location = location  # {"x": 0, "y": 0, "z": 0, "zone": "Sector A"}
        self.last_update = datetime.now()
        self.status = "Active"
        self.signal_strength = random.randint(85, 100)


class DeviceTracker(QObject):
    """Device tracking engine with real-time updates"""
    
    location_updated = pyqtSignal(dict)
    battery_alert = pyqtSignal(str, int)
    emergency_signal = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.devices = {}
        self.zones = ["Main Shaft", "Sector A", "Sector B", "Sector C", "Processing", "Workshop"]
        self.init_sample_devices()
        
        # Real-time update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_device_locations)
        self.update_timer.start(2000)  # Update every 2 seconds
        
    def init_sample_devices(self):
        """Initialize sample devices for demonstration"""
        personnel_names = [
            "John Smith", "Sarah Johnson", "Mike Wilson", "Lisa Brown", "David Chen",
            "Emma Davis", "Tom Anderson", "Jane Roberts", "Chris Martin", "Amy Taylor",
            "Steve Williams", "Maria Garcia", "James Miller", "Patricia Jones", "Robert Moore"
        ]
        
        # Create personnel trackers
        for i, name in enumerate(personnel_names, 1):
            device_id = f"PT{i:03d}"  # PT001, PT002, etc.
            location = {
                "x": random.uniform(-300, 300),
                "y": random.uniform(-200, 200),
                "z": random.uniform(-50, 0),
                "zone": random.choice(self.zones)
            }
            device = Device(
                device_id,
                "Personnel",
                name,
                random.randint(20, 100),
                location
            )
            self.devices[device_id] = device
        
        # Create equipment trackers
        equipment_types = [
            ("Excavator #1", "Heavy Equipment"),
            ("Loader #2", "Heavy Equipment"),
            ("Drill #3", "Drilling"),
            ("Truck #4", "Transport"),
            ("Crane #5", "Support")
        ]
        
        for i, (equip_name, equip_type) in enumerate(equipment_types, 1):
            device_id = f"ET{i:03d}"  # ET001, ET002, etc.
            location = {
                "x": random.uniform(-400, 400),
                "y": random.uniform(-300, 300),
                "z": random.uniform(-30, 0),
                "zone": random.choice(self.zones)
            }
            device = Device(
                device_id,
                "Equipment",
                equip_name,
                random.randint(40, 100),
                location
            )
            self.devices[device_id] = device
    
    def update_device_locations(self):
        """Simulate real-time location updates"""
        for device_id, device in self.devices.items():
            # Simulate movement
            if random.random() < 0.3:  # 30% chance of movement
                device.location["x"] += random.uniform(-5, 5)
                device.location["y"] += random.uniform(-5, 5)
                device.location["z"] += random.uniform(-1, 1)
                
                # Keep within bounds
                device.location["x"] = max(-500, min(500, device.location["x"]))
                device.location["y"] = max(-400, min(400, device.location["y"]))
                device.location["z"] = max(-100, min(0, device.location["z"]))
                
                # Update zone based on position
                device.location["zone"] = self.determine_zone(device.location)
                
            # Simulate battery drain
            if random.random() < 0.1:  # 10% chance
                device.battery = max(0, device.battery - random.randint(1, 3))
                if device.battery < 20:
                    self.battery_alert.emit(device_id, device.battery)
            
            # Update signal strength
            device.signal_strength = random.randint(75, 100)
            device.last_update = datetime.now()
            
            # Emit location update
            self.location_updated.emit({
                "device_id": device_id,
                "location": device.location,
                "timestamp": device.last_update.isoformat()
            })
    
    def determine_zone(self, location):
        """Determine zone based on coordinates"""
        x, y = location["x"], location["y"]
        
        if abs(x) < 50 and abs(y) < 50:
            return "Main Shaft"
        elif x < -200:
            return "Sector A"
        elif x > 200:
            return "Sector B"
        elif y > 150:
            return "Sector C"
        elif y < -150:
            return "Processing"
        else:
            return "Workshop"
    
    def get_device_by_id(self, device_id):
        return self.devices.get(device_id)
    
    def get_all_devices(self):
        return list(self.devices.values())
    
    def trigger_emergency(self, device_id):
        """Trigger emergency signal for a device"""
        if device_id in self.devices:
            device = self.devices[device_id]
            self.emergency_signal.emit({
                "device_id": device_id,
                "assigned_to": device.assigned_to,
                "location": device.location,
                "timestamp": datetime.now().isoformat(),
                "type": "SOS"
            })


class Mine3DVisualization(QWebEngineView):
    """3D Visualization using Three.js"""
    
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.setMinimumSize(800, 600)
        self.load_3d_scene()
        
        # Connect to tracker updates
        self.tracker.location_updated.connect(self.update_device_position)
        
    def load_3d_scene(self):
        """Load Three.js 3D visualization"""
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
            background: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stat {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            min-width: 200px;
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
            font-weight: 600;
        }
        .controls {
            position: absolute;
            bottom: 20px;
            left: 20px;
            color: #B0B0B0;
            font-size: 12px;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="info">
        <h3 style="margin: 0 0 15px 0; color: #00D4FF;">⛏️ MineTracker 3D</h3>
        <div class="stat">
            <span class="stat-label">Personnel</span>
            <span class="stat-value" id="personnel-count">15</span>
        </div>
        <div class="stat">
            <span class="stat-label">Equipment</span>
            <span class="stat-value" id="equipment-count">5</span>
        </div>
        <div class="stat">
            <span class="stat-label">Active Zones</span>
            <span class="stat-value" id="zones-count">6</span>
        </div>
    </div>
    <div class="controls">
        🖱️ Drag: Rotate | Scroll: Zoom | Arrow Keys: Pan
    </div>

    <script>
        // Scene setup
        const scene = new THREE.Scene();
        scene.fog = new THREE.Fog(0x0F0F0F, 100, 1500);
        
        const camera = new THREE.PerspectiveCamera(
            75, window.innerWidth / window.innerHeight, 0.1, 2000
        );
        camera.position.set(300, 400, 500);
        camera.lookAt(0, 0, 0);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x0F0F0F);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(100, 200, 100);
        directionalLight.castShadow = true;
        directionalLight.shadow.camera.left = -500;
        directionalLight.shadow.camera.right = 500;
        directionalLight.shadow.camera.top = 500;
        directionalLight.shadow.camera.bottom = -500;
        scene.add(directionalLight);
        
        // Mine floor with grid
        const gridHelper = new THREE.GridHelper(1000, 50, 0x00D4FF, 0x1A1A1A);
        scene.add(gridHelper);
        
        // Mine structure
        const floorGeometry = new THREE.PlaneGeometry(1000, 800);
        const floorMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x1A1A1A,
            roughness: 0.8,
            metalness: 0.2
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.position.y = -1;
        floor.receiveShadow = true;
        scene.add(floor);
        
        // Create mine tunnels
        const tunnelMaterial = new THREE.MeshStandardMaterial({ 
            color: 0x2A2A2A,
            transparent: true,
            opacity: 0.8,
            roughness: 0.7
        });
        
        // Main tunnel
        const mainTunnelGeom = new THREE.BoxGeometry(600, 50, 30);
        const mainTunnel = new THREE.Mesh(mainTunnelGeom, tunnelMaterial);
        mainTunnel.position.set(0, 25, 0);
        mainTunnel.castShadow = true;
        scene.add(mainTunnel);
        
        // Cross tunnels
        const crossTunnelGeom = new THREE.BoxGeometry(30, 50, 400);
        for (let i = -200; i <= 200; i += 200) {
            const tunnel = new THREE.Mesh(crossTunnelGeom, tunnelMaterial);
            tunnel.position.set(i, 25, 0);
            tunnel.castShadow = true;
            scene.add(tunnel);
        }
        
        // Zone markers
        const zones = [
            { name: 'Main Shaft', x: 0, y: 5, z: 0, color: 0x00D4FF },
            { name: 'Sector A', x: -300, y: 5, z: -150, color: 0x00FF88 },
            { name: 'Sector B', x: 300, y: 5, z: -150, color: 0xFFB800 },
            { name: 'Sector C', x: 0, y: 5, z: 200, color: 0xFF3366 },
            { name: 'Processing', x: -200, y: 5, z: 300, color: 0x9966FF },
            { name: 'Workshop', x: 200, y: 5, z: 300, color: 0x00CCFF }
        ];
        
        zones.forEach(zone => {
            // Zone platform
            const zoneGeom = new THREE.CylinderGeometry(40, 40, 3, 32);
            const zoneMat = new THREE.MeshStandardMaterial({ 
                color: zone.color,
                emissive: zone.color,
                emissiveIntensity: 0.2
            });
            const zoneMesh = new THREE.Mesh(zoneGeom, zoneMat);
            zoneMesh.position.set(zone.x, zone.y, zone.z);
            zoneMesh.castShadow = true;
            scene.add(zoneMesh);
            
            // Zone glow effect
            const glowGeom = new THREE.RingGeometry(35, 45, 32);
            const glowMat = new THREE.MeshBasicMaterial({ 
                color: zone.color,
                transparent: true,
                opacity: 0.3,
                side: THREE.DoubleSide
            });
            const glow = new THREE.Mesh(glowGeom, glowMat);
            glow.position.set(zone.x, zone.y + 1, zone.z);
            glow.rotation.x = -Math.PI / 2;
            scene.add(glow);
        });
        
        // Device tracking objects
        const devices = new Map();
        
        // Create device marker
        function createDeviceMarker(type, color) {
            const geometry = type === 'Personnel' 
                ? new THREE.SphereGeometry(5, 16, 16)
                : new THREE.BoxGeometry(10, 10, 10);
            
            const material = new THREE.MeshStandardMaterial({
                color: color,
                emissive: color,
                emissiveIntensity: 0.3
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.castShadow = true;
            
            // Add glow effect
            const glowGeom = type === 'Personnel'
                ? new THREE.SphereGeometry(8, 16, 16)
                : new THREE.BoxGeometry(14, 14, 14);
            
            const glowMat = new THREE.MeshBasicMaterial({
                color: color,
                transparent: true,
                opacity: 0.2
            });
            
            const glow = new THREE.Mesh(glowGeom, glowMat);
            mesh.add(glow);
            
            return mesh;
        }
        
        // Update device position
        window.updateDevice = function(data) {
            const { device_id, type, location, battery, status } = data;
            
            if (!devices.has(device_id)) {
                const color = type === 'Personnel' ? 0x00FF88 : 0xFFB800;
                const marker = createDeviceMarker(type, color);
                devices.set(device_id, marker);
                scene.add(marker);
            }
            
            const marker = devices.get(device_id);
            
            // Smooth position transition
            marker.position.x = location.x;
            marker.position.y = Math.abs(location.z) + 10;
            marker.position.z = location.y;
            
            // Battery-based opacity
            const opacity = battery / 100;
            marker.material.opacity = Math.max(0.5, opacity);
            
            // Status-based color
            if (status === 'Emergency') {
                marker.material.emissive = new THREE.Color(0xFF0000);
                marker.material.emissiveIntensity = 0.8;
            }
        };
        
        // Mouse controls
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
            }
        });
        
        // Zoom control
        document.addEventListener('wheel', (event) => {
            camera.position.z += event.deltaY * 0.5;
            camera.position.z = Math.max(200, Math.min(1000, camera.position.z));
        });
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            
            // Smooth camera rotation
            camera.position.x = Math.sin(targetRotationY) * 500;
            camera.position.z = Math.cos(targetRotationY) * 500;
            camera.position.y = 400 + Math.sin(targetRotationX) * 200;
            camera.lookAt(0, 0, 0);
            
            // Animate zone glows
            zones.forEach((zone, index) => {
                const time = Date.now() * 0.001;
                const glow = scene.children.find(
                    child => child.position.x === zone.x && 
                    child.position.z === zone.z && 
                    child.geometry instanceof THREE.RingGeometry
                );
                if (glow) {
                    glow.material.opacity = 0.2 + Math.sin(time + index) * 0.1;
                }
            });
            
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Handle window resize
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
    
    def update_device_position(self, data):
        """Update device position in 3D view"""
        device_id = data["device_id"]
        device = self.tracker.get_device_by_id(device_id)
        
        if device:
            update_data = {
                "device_id": device_id,
                "type": device.type,
                "location": device.location,
                "battery": device.battery,
                "status": device.status
            }
            
            # Execute JavaScript to update 3D position
            js_code = f"window.updateDevice({json.dumps(update_data)});"
            self.page().runJavaScript(js_code)


class DeviceListWidget(QWidget):
    """Modern device list with real-time updates"""
    
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.init_ui()
        
        # Connect to updates
        self.tracker.location_updated.connect(self.refresh_list)
        self.tracker.battery_alert.connect(self.show_battery_alert)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📍 Device Tracking")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 600;
                color: #00D4FF;
            }
        """)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search devices...")
        self.search_box.setMaximumWidth(300)
        self.search_box.textChanged.connect(self.filter_devices)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_box)
        
        layout.addLayout(header_layout)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.create_stat_card(stats_layout, "👥 Personnel", "15", ModernTheme.SUCCESS)
        self.create_stat_card(stats_layout, "🚜 Equipment", "5", ModernTheme.WARNING)
        self.create_stat_card(stats_layout, "🔋 Low Battery", "2", ModernTheme.DANGER)
        self.create_stat_card(stats_layout, "📡 Signal", "98%", ModernTheme.PRIMARY)
        
        layout.addLayout(stats_layout)
        
        # Device table
        self.create_device_table()
        layout.addWidget(self.device_table)
        
        # Refresh data
        self.refresh_list()
    
    def create_stat_card(self, parent_layout, label, value, color):
        """Create a statistics card"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background: {ModernTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {ModernTheme.BORDER};
                padding: 15px;
            }}
        """)
        card.setFixedHeight(100)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {ModernTheme.TEXT_SECONDARY};
                font-size: 12px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: 700;
            }}
        """)
        
        card_layout.addWidget(label_widget)
        card_layout.addWidget(value_widget)
        
        parent_layout.addWidget(card)
    
    def create_device_table(self):
        """Create the device tracking table"""
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(8)
        self.device_table.setHorizontalHeaderLabels([
            "Device ID", "Type", "Assigned To", "Zone", 
            "Battery", "Signal", "Last Update", "Actions"
        ])
        
        # Style the table
        self.device_table.setStyleSheet(f"""
            QTableWidget {{
                background: {ModernTheme.SURFACE};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        # Configure columns
        header = self.device_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.device_table.setColumnWidth(0, 100)
        self.device_table.setColumnWidth(1, 100)
        self.device_table.setColumnWidth(2, 150)
        self.device_table.setColumnWidth(3, 100)
        self.device_table.setColumnWidth(4, 100)
        self.device_table.setColumnWidth(5, 100)
        self.device_table.setColumnWidth(6, 150)
        
        # Remove row numbers
        self.device_table.verticalHeader().setVisible(False)
        
    def refresh_list(self):
        """Refresh the device list"""
        devices = self.tracker.get_all_devices()
        self.device_table.setRowCount(len(devices))
        
        for row, device in enumerate(devices):
            # Device ID
            id_item = QTableWidgetItem(device.id)
            id_item.setForeground(QBrush(QColor(ModernTheme.PRIMARY)))
            self.device_table.setItem(row, 0, id_item)
            
            # Type with icon
            type_text = f"{'👤' if device.type == 'Personnel' else '🚜'} {device.type}"
            self.device_table.setItem(row, 1, QTableWidgetItem(type_text))
            
            # Assigned to
            self.device_table.setItem(row, 2, QTableWidgetItem(device.assigned_to))
            
            # Zone
            zone_item = QTableWidgetItem(device.location["zone"])
            zone_item.setForeground(QBrush(QColor(ModernTheme.SUCCESS)))
            self.device_table.setItem(row, 3, zone_item)
            
            # Battery with color coding
            battery_item = QTableWidgetItem(f"{device.battery}%")
            if device.battery < 20:
                battery_item.setForeground(QBrush(QColor(ModernTheme.DANGER)))
            elif device.battery < 50:
                battery_item.setForeground(QBrush(QColor(ModernTheme.WARNING)))
            else:
                battery_item.setForeground(QBrush(QColor(ModernTheme.SUCCESS)))
            self.device_table.setItem(row, 4, battery_item)
            
            # Signal strength
            signal_item = QTableWidgetItem(f"{device.signal_strength}%")
            if device.signal_strength < 50:
                signal_item.setForeground(QBrush(QColor(ModernTheme.DANGER)))
            elif device.signal_strength < 75:
                signal_item.setForeground(QBrush(QColor(ModernTheme.WARNING)))
            else:
                signal_item.setForeground(QBrush(QColor(ModernTheme.SUCCESS)))
            self.device_table.setItem(row, 5, signal_item)
            
            # Last update
            time_diff = datetime.now() - device.last_update
            if time_diff.seconds < 60:
                time_text = "Just now"
            elif time_diff.seconds < 3600:
                time_text = f"{time_diff.seconds // 60} min ago"
            else:
                time_text = f"{time_diff.seconds // 3600} hours ago"
            self.device_table.setItem(row, 6, QTableWidgetItem(time_text))
            
            # Actions button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 5, 5, 5)
            actions_layout.setSpacing(5)
            
            locate_btn = QPushButton("📍")
            locate_btn.setFixedSize(30, 30)
            locate_btn.setToolTip("Locate on map")
            locate_btn.setStyleSheet("""
                QPushButton {
                    background: #00D4FF;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: #0099CC;
                }
            """)
            
            emergency_btn = QPushButton("🆘")
            emergency_btn.setFixedSize(30, 30)
            emergency_btn.setToolTip("Send emergency signal")
            emergency_btn.setStyleSheet("""
                QPushButton {
                    background: #FF3366;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: #CC0033;
                }
            """)
            emergency_btn.clicked.connect(lambda: self.tracker.trigger_emergency(device.id))
            
            actions_layout.addWidget(locate_btn)
            actions_layout.addWidget(emergency_btn)
            actions_layout.addStretch()
            
            self.device_table.setCellWidget(row, 7, actions_widget)
        
        # Set row height
        for row in range(self.device_table.rowCount()):
            self.device_table.setRowHeight(row, 50)
    
    def filter_devices(self, text):
        """Filter devices based on search text"""
        for row in range(self.device_table.rowCount()):
            show_row = False
            for col in range(self.device_table.columnCount() - 1):  # Exclude actions column
                item = self.device_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show_row = True
                    break
            self.device_table.setRowHidden(row, not show_row)
    
    def show_battery_alert(self, device_id, battery_level):
        """Show battery alert notification"""
        msg = QMessageBox(self)
        msg.setWindowTitle("⚠️ Low Battery Alert")
        msg.setText(f"Device {device_id} battery is critically low: {battery_level}%")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStyleSheet(ModernTheme.get_app_style())
        msg.exec()


class DashboardWidget(QWidget):
    """Main dashboard with overview"""
    
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.init_ui()
        
        # Connect to emergency signals
        self.tracker.emergency_signal.connect(self.show_emergency_alert)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("🎯 Operations Dashboard")
        header.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 700;
                color: #00D4FF;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(header)
        
        # Real-time stats grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Create dashboard cards
        cards = [
            ("👥 Total Personnel", "15", "Underground", ModernTheme.SUCCESS),
            ("🚜 Active Equipment", "5", "Operating", ModernTheme.WARNING),
            ("📍 Active Zones", "6", "Monitored", ModernTheme.PRIMARY),
            ("🔋 Avg. Battery", "78%", "Healthy", ModernTheme.SUCCESS),
            ("📡 Network Status", "98%", "Excellent", ModernTheme.SUCCESS),
            ("⏱️ Avg. Response", "1.2s", "Real-time", ModernTheme.PRIMARY),
            ("⚠️ Active Alerts", "0", "All Clear", ModernTheme.SUCCESS),
            ("🛡️ Safety Score", "94%", "Optimal", ModernTheme.SUCCESS)
        ]
        
        for i, (title, value, subtitle, color) in enumerate(cards):
            card = self.create_dashboard_card(title, value, subtitle, color)
            stats_grid.addWidget(card, i // 4, i % 4)
        
        layout.addLayout(stats_grid)
        
        # Activity feed
        self.create_activity_feed()
        layout.addWidget(self.activity_widget)
        
    def create_dashboard_card(self, title, value, subtitle, color):
        """Create a dashboard statistics card"""
        card = QWidget()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QWidget {{
                background: {ModernTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {ModernTheme.BORDER};
            }}
            QWidget:hover {{
                border-color: {color};
                background: {ModernTheme.SURFACE_LIGHT};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {ModernTheme.TEXT_SECONDARY};
                font-size: 12px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 32px;
                font-weight: 700;
            }}
        """)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: {ModernTheme.TEXT_SECONDARY};
                font-size: 11px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()
        
        return card
    
    def create_activity_feed(self):
        """Create real-time activity feed"""
        self.activity_widget = QWidget()
        self.activity_widget.setStyleSheet(f"""
            QWidget {{
                background: {ModernTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {ModernTheme.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(self.activity_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Feed header
        feed_header = QHBoxLayout()
        
        feed_title = QLabel("📊 Real-time Activity")
        feed_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #00D4FF;
            }
        """)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setFixedSize(80, 30)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ModernTheme.SURFACE_LIGHT};
                border: 1px solid {ModernTheme.BORDER};
                border-radius: 6px;
                color: {ModernTheme.TEXT_SECONDARY};
                font-size: 12px;
            }}
            QPushButton:hover {{
                background: {ModernTheme.PRIMARY_DARK};
                color: white;
            }}
        """)
        
        feed_header.addWidget(feed_title)
        feed_header.addStretch()
        feed_header.addWidget(clear_btn)
        
        layout.addLayout(feed_header)
        
        # Activity list
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background: {ModernTheme.BACKGROUND};
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
                color: {ModernTheme.TEXT_PRIMARY};
            }}
            QListWidget::item:hover {{
                background: {ModernTheme.SURFACE_LIGHT};
            }}
        """)
        
        # Add sample activities
        activities = [
            ("✅", "PT001 - John Smith entered Sector A", "2 min ago"),
            ("🔋", "ET003 - Drill #3 battery at 45%", "5 min ago"),
            ("📍", "PT005 - David Chen moved to Processing", "8 min ago"),
            ("✅", "Safety check completed in Sector B", "15 min ago"),
            ("🚜", "ET001 - Excavator #1 started operation", "23 min ago")
        ]
        
        for icon, text, time in activities:
            item_text = f"{icon} {text} • {time}"
            self.activity_list.addItem(item_text)
        
        layout.addWidget(self.activity_list)
        
        clear_btn.clicked.connect(self.activity_list.clear)
    
    def show_emergency_alert(self, emergency_data):
        """Show emergency alert dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("🚨 EMERGENCY ALERT")
        msg.setText(f"""
Emergency Signal Received!

Device: {emergency_data['device_id']}
Person: {emergency_data['assigned_to']}
Location: {emergency_data['location']['zone']}
Coordinates: X:{emergency_data['location']['x']:.1f}, Y:{emergency_data['location']['y']:.1f}
Time: {emergency_data['timestamp']}
        """)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStyleSheet(ModernTheme.get_app_style())
        msg.exec()


class MineTrackerApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.tracker = DeviceTracker()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("MineTracker - Underground Safety & Device Tracking System")
        self.setGeometry(100, 100, 1600, 900)
        
        # Apply modern theme
        self.setStyleSheet(ModernTheme.get_app_style())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create navigation sidebar
        self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create main content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background: {ModernTheme.BACKGROUND};
            }}
        """)
        
        # Add pages
        self.dashboard = DashboardWidget(self.tracker)
        self.device_list = DeviceListWidget(self.tracker)
        self.visualization_3d = Mine3DVisualization(self.tracker)
        
        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.device_list)
        self.content_stack.addWidget(self.visualization_3d)
        
        main_layout.addWidget(self.content_stack, 1)
        
        # Create status bar
        self.create_status_bar()
        
        # Set initial page
        self.content_stack.setCurrentIndex(0)
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet(f"""
            QWidget {{
                background: {ModernTheme.SURFACE};
                border-right: 1px solid {ModernTheme.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_widget = QWidget()
        logo_widget.setFixedHeight(80)
        logo_widget.setStyleSheet(f"""
            QWidget {{
                background: {ModernTheme.SURFACE_LIGHT};
                border-bottom: 1px solid {ModernTheme.BORDER};
            }}
        """)
        
        logo_layout = QHBoxLayout(logo_widget)
        logo_label = QLabel("⛏️ MineTracker")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #00D4FF;
                padding: 20px;
            }
        """)
        logo_layout.addWidget(logo_label)
        
        layout.addWidget(logo_widget)
        
        # Navigation buttons
        nav_buttons = [
            ("🎯 Dashboard", 0),
            ("📍 Device Tracking", 1),
            ("🗺️ 3D Visualization", 2)
        ]
        
        self.nav_btn_group = QButtonGroup()
        
        for text, index in nav_buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setFixedHeight(60)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-left: 3px solid transparent;
                    color: {ModernTheme.TEXT_SECONDARY};
                    font-size: 16px;
                    font-weight: 500;
                    text-align: left;
                    padding-left: 25px;
                }}
                QPushButton:hover {{
                    background: {ModernTheme.SURFACE_LIGHT};
                    color: {ModernTheme.TEXT_PRIMARY};
                }}
                QPushButton:checked {{
                    background: {ModernTheme.SURFACE_LIGHT};
                    border-left-color: {ModernTheme.PRIMARY};
                    color: {ModernTheme.PRIMARY};
                }}
            """)
            btn.clicked.connect(lambda checked, idx=index: self.content_stack.setCurrentIndex(idx))
            
            if index == 0:
                btn.setChecked(True)
            
            self.nav_btn_group.addButton(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Emergency button
        emergency_btn = QPushButton("🚨 EMERGENCY")
        emergency_btn.setFixedHeight(60)
        emergency_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ModernTheme.DANGER};
                border: none;
                color: white;
                font-size: 18px;
                font-weight: 700;
                margin: 20px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background: #CC0033;
            }}
            QPushButton:pressed {{
                background: #990022;
            }}
        """)
        emergency_btn.clicked.connect(self.trigger_emergency_protocol)
        layout.addWidget(emergency_btn)
    
    def create_status_bar(self):
        """Create status bar"""
        status = self.statusBar()
        status.setStyleSheet(f"""
            QStatusBar {{
                background: {ModernTheme.SURFACE};
                color: {ModernTheme.TEXT_SECONDARY};
                border-top: 1px solid {ModernTheme.BORDER};
                font-size: 12px;
                padding: 5px;
            }}
        """)
        
        # Add status widgets
        status.showMessage("✅ System Online • 📡 Connected • 🔐 Secure")
        
        # Add time display
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"color: {ModernTheme.TEXT_SECONDARY};")
        status.addPermanentWidget(self.time_label)
        
        # Update time
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"🕐 {current_time}")
    
    def trigger_emergency_protocol(self):
        """Trigger emergency protocol"""
        reply = QMessageBox.critical(
            self,
            "🚨 Emergency Protocol",
            "Activate emergency protocol?\n\nThis will:\n• Alert all personnel\n• Notify emergency services\n• Activate evacuation procedures",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self,
                "Emergency Activated",
                "✅ Emergency protocol activated!\n\n• All personnel notified\n• Emergency services contacted\n• Evacuation routes displayed"
            )


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set application metadata
    app.setApplicationName("MineTracker")
    app.setOrganizationName("MineGuard Technologies")
    app.setApplicationDisplayName("MineTracker - Underground Safety System")
    
    # Create and show main window
    window = MineTrackerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()