"""Real-time Chart Widget - Ultra Modern"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from collections import deque
import math

class RealtimeChart(QWidget):
    """Real-time line chart with gradient fill"""
    
    def __init__(self, title="Chart", max_points=50, y_range=(0, 100)):
        super().__init__()
        self.title = title
        self.max_points = max_points
        self.y_range = y_range
        self.data_series = deque(maxlen=max_points)
        self.setMinimumHeight(200)
        
        # Colors
        self.line_color = QColor(MineTrackerTheme.PRIMARY)
        self.fill_color = QColor(MineTrackerTheme.PRIMARY)
        self.fill_color.setAlpha(50)
        self.grid_color = QColor(MineTrackerTheme.BORDER)
    
    def add_data_point(self, value):
        """Yeni veri noktası ekle"""
        self.data_series.append(value)
        self.update()
    
    def clear_data(self):
        """Verileri temizle"""
        self.data_series.clear()
        self.update()
    
    def paintEvent(self, event):
        """Chart çiz"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(MineTrackerTheme.SURFACE))
        
        if len(self.data_series) < 2:
            # No data message
            painter.setPen(QColor(MineTrackerTheme.TEXT_SECONDARY))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Veri Bekleniyor...")
            return
        
        # Chart area
        margin = 40
        chart_width = self.width() - 2 * margin
        chart_height = self.height() - 2 * margin
        
        # Grid çiz
        painter.setPen(QPen(self.grid_color, 1))
        for i in range(5):
            y = margin + (chart_height * i / 4)
            painter.drawLine(margin, int(y), self.width() - margin, int(y))
        
        # Data points
        points = []
        for i, value in enumerate(self.data_series):
            x = margin + (chart_width * i / (self.max_points - 1))
            
            # Normalize value to chart range
            normalized = (value - self.y_range[0]) / (self.y_range[1] - self.y_range[0])
            normalized = max(0, min(1, normalized))
            y = margin + chart_height - (chart_height * normalized)
            
            points.append(QPointF(x, y))
        
        # Fill gradient
        if len(points) >= 2:
            path = QPainterPath()
            path.moveTo(points[0].x(), self.height() - margin)
            path.lineTo(points[0])
            
            for point in points:
                path.lineTo(point)
            
            path.lineTo(points[-1].x(), self.height() - margin)
            path.closeSubpath()
            
            painter.fillPath(path, QBrush(self.fill_color))
        
        # Line
        painter.setPen(QPen(self.line_color, 3))
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])
        
        # Data points (circles)
        painter.setBrush(QBrush(self.line_color))
        for point in points:
            painter.drawEllipse(point, 4, 4)
        
        # Title
        painter.setPen(QColor(MineTrackerTheme.TEXT_PRIMARY))
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.drawText(margin, 20, self.title)
        
        # Current value
        if self.data_series:
            current_value = self.data_series[-1]
            painter.setFont(QFont('Arial', 14, QFont.Weight.Bold))
            painter.setPen(self.line_color)
            value_text = f"{current_value:.1f}"
            painter.drawText(self.width() - margin - 50, 20, value_text)
