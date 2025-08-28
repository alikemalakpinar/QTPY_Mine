# components/model3d/mine_3d_view.py - Advanced 3D Digital Twin System
import math
import random
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtOpenGL import QOpenGLWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

class Mine3DDigitalTwin(QOpenGLWidget):
    """Revolutionary 3D Digital Twin of Mining Operations"""
    
    def __init__(self):
        super().__init__()
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom_level = 1.0
        self.last_pos = QPoint()
        
        # Digital Twin Data
        self.personnel_positions = []
        self.equipment_positions = []
        self.safety_zones = []
        self.real_time_data = {}
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(100)  # 10 FPS for smooth animation
        
        self.setMinimumSize(800, 600)
        self.generate_mock_mine_data()
    
    def generate_mock_mine_data(self):
        """Generate realistic mining operation data"""
        # Personnel positions (147 active)
        for i in range(147):
            self.personnel_positions.append({
                'id': f'W-{i+1:03d}',
                'name': f'Worker {i+1}',
                'x': random.uniform(-400, 400),
                'y': random.uniform(-300, 300),
                'z': random.uniform(-50, 0),  # Underground levels
                'status': random.choice(['active', 'break', 'moving']),
                'heart_rate': random.randint(60, 100),
                'safety_score': random.uniform(0.7, 1.0)
            })
        
        # Equipment positions
        equipment_types = ['Excavator', 'Loader', 'Truck', 'Drill', 'Crusher']
        for i, eq_type in enumerate(equipment_types * 12):  # 60 pieces total
            self.equipment_positions.append({
                'id': f'{eq_type[:3].upper()}-{i+1:03d}',
                'type': eq_type,
                'x': random.uniform(-450, 450),
                'y': random.uniform(-350, 350),
                'z': random.uniform(-40, 5),
                'status': random.choice(['operational', 'maintenance', 'offline']),
                'efficiency': random.uniform(0.6, 0.95),
                'fuel_level': random.randint(20, 100)
            })
        
        # Safety zones
        self.safety_zones = [
            {'name': 'Sector A', 'x': -200, 'y': -150, 'radius': 80, 'risk': 'low'},
            {'name': 'Sector B', 'x': 200, 'y': -150, 'radius': 90, 'risk': 'medium'},
            {'name': 'Sector C', 'x': 0, 'y': 200, 'radius': 100, 'risk': 'high'},
            {'name': 'Processing', 'x': -300, 'y': 100, 'radius': 60, 'risk': 'medium'},
            {'name': 'Workshop', 'x': 300, 'y': 150, 'radius': 50, 'risk': 'low'}
        ]
    
    def paintGL(self):
        """Render 3D mine visualization"""
        # This is a simplified 3D rendering using PyQt6's built-in capabilities
        # In production, would use OpenGL or integrate with Three.js
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Clear background
        painter.fillRect(self.rect(), QColor(15, 23, 35))  # Dark mine-like background
        
        # Apply transformations
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self.zoom_level, self.zoom_level)
        
        # Draw mine infrastructure
        self.draw_mine_infrastructure(painter)
        
        # Draw safety zones
        self.draw_safety_zones(painter)
        
        # Draw equipment
        self.draw_equipment(painter)
        
        # Draw personnel
        self.draw_personnel(painter)
        
        # Draw real-time data overlay
        self.draw_data_overlay(painter)
        
        painter.end()
    
    def draw_mine_infrastructure(self, painter):
        """Draw mine tunnels, shafts and infrastructure"""
        # Mine shaft
        shaft_pen = QPen(QColor(100, 120, 140), 3)
        painter.setPen(shaft_pen)
        painter.setBrush(QBrush(QColor(40, 50, 60, 100)))
        
        # Main shaft
        painter.drawEllipse(-30, -30, 60, 60)
        
        # Tunnels
        tunnel_pen = QPen(QColor(80, 100, 120), 2)
        painter.setPen(tunnel_pen)
        
        # Horizontal tunnels
        for y in [-200, -100, 0, 100, 200]:
            painter.drawLine(-400, y, 400, y)
        
        # Vertical tunnels
        for x in [-300, -150, 0, 150, 300]:
            painter.drawLine(x, -300, x, 300)
        
        # Processing plant
        plant_pen = QPen(QColor(150, 150, 100), 2)
        painter.setPen(plant_pen)
        painter.setBrush(QBrush(QColor(80, 80, 50, 120)))
        painter.drawRect(-350, 80, 100, 60)
        
        # Conveyor belts
        conveyor_pen = QPen(QColor(120, 100, 80), 3)
        painter.setPen(conveyor_pen)
        painter.drawLine(-300, 120, 300, 120)
    
    def draw_safety_zones(self, painter):
        """Draw safety zones with risk indication"""
        for zone in self.safety_zones:
            risk_colors = {
                'low': QColor(40, 150, 40, 80),
                'medium': QColor(150, 150, 40, 80),
                'high': QColor(150, 40, 40, 80)
            }
            
            color = risk_colors.get(zone['risk'], risk_colors['low'])
            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            
            painter.drawEllipse(
                zone['x'] - zone['radius'],
                zone['y'] - zone['radius'],
                zone['radius'] * 2,
                zone['radius'] * 2
            )
            
            # Zone label
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            painter.drawText(zone['x'] - 30, zone['y'], zone['name'])
    
    def draw_equipment(self, painter):
        """Draw equipment with real-time status"""
        for equipment in self.equipment_positions:
            # Equipment status colors
            status_colors = {
                'operational': QColor(40, 200, 40),
                'maintenance': QColor(200, 200, 40),
                'offline': QColor(200, 40, 40)
            }
            
            color = status_colors.get(equipment['status'], status_colors['operational'])
            
            # Draw equipment icon
            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            
            # Different shapes for different equipment
            if equipment['type'] == 'Excavator':
                painter.drawRect(equipment['x']-6, equipment['y']-6, 12, 12)
            elif equipment['type'] == 'Truck':
                painter.drawEllipse(equipment['x']-5, equipment['y']-5, 10, 10)
            elif equipment['type'] == 'Drill':
                points = [
                    QPoint(equipment['x'], equipment['y']-6),
                    QPoint(equipment['x']-5, equipment['y']+6),
                    QPoint(equipment['x']+5, equipment['y']+6)
                ]
                painter.drawPolygon(points)
            else:
                painter.drawRect(equipment['x']-4, equipment['y']-4, 8, 8)
            
            # Status indicator
            if equipment['status'] != 'operational':
                painter.setPen(QPen(QColor(255, 255, 255), 1))
                painter.setFont(QFont("Arial", 8))
                painter.drawText(equipment['x'] + 8, equipment['y'], equipment['status'][:4])
    
    def draw_personnel(self, painter):
        """Draw personnel with safety indicators"""
        for person in self.personnel_positions:
            # Personnel status colors
            if person['status'] == 'active':
                color = QColor(100, 200, 255)  # Blue for active
            elif person['status'] == 'break':
                color = QColor(255, 200, 100)  # Orange for break
            else:
                color = QColor(200, 100, 255)  # Purple for moving
            
            # Safety score affects brightness
            brightness = int(person['safety_score'] * 255)
            color.setAlpha(brightness)
            
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            
            # Draw person as small circle
            painter.drawEllipse(person['x']-2, person['y']-2, 4, 4)
            
            # Health indicator for critical personnel
            if person['heart_rate'] > 90 or person['safety_score'] < 0.8:
                painter.setPen(QPen(QColor(255, 50, 50), 2))
                painter.drawEllipse(person['x']-4, person['y']-4, 8, 8)
    
    def draw_data_overlay(self, painter):
        """Draw real-time data overlay"""
        # Reset transformations for overlay
        painter.resetTransform()
        
        # HUD Background
        hud_rect = QRect(10, 10, 250, 200)
        painter.setPen(QPen(QColor(255, 255, 255, 50), 1))
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.drawRect(hud_rect)
        
        # Real-time statistics
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        stats_text = [
            "🏔️ DIGITAL TWIN ACTIVE",
            "",
            f"👥 Personnel: {len(self.personnel_positions)}",
            f"🚛 Equipment: {len(self.equipment_positions)}",
            f"🛡️ Safety Zones: {len(self.safety_zones)}",
            "",
            f"🟢 Operational: {sum(1 for e in self.equipment_positions if e['status'] == 'operational')}",
            f"🟡 Maintenance: {sum(1 for e in self.equipment_positions if e['status'] == 'Maintenance')}",
            f"🔴 Offline: {sum(1 for e in self.equipment_positions if e['status'] == 'offline')}",
            "",
            f"⏱️ Last Update: {datetime.now().strftime('%H:%M:%S')}"
        ]