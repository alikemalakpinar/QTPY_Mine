"""Modern Stat Card Component with Gradients"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme

class ModernStatCard(QWidget):
    """Ultra modern gradient stat card"""
    
    clicked = pyqtSignal()
    
    def __init__(self, icon, title, value, subtitle, color, gradient=True):
        super().__init__()
        self.icon = icon
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.color = QColor(color)
        self.gradient = gradient
        self.hover = False
        
        self.setFixedHeight(150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        
        self.init_ui()
    
    def init_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)
        
        # Üst - Icon ve Title
        top_layout = QHBoxLayout()
        
        self.icon_label = QLabel(self.icon)
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                color: {self.color.name()};
            }}
        """)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: 600;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
        """)
        
        top_layout.addWidget(self.icon_label)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        
        # Value
        self.value_label = QLabel(str(self.value))
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 42px;
                font-weight: 800;
                color: {self.color.name()};
                letter-spacing: -1px;
            }}
        """)
        
        # Subtitle
        self.subtitle_label = QLabel(self.subtitle)
        self.subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {MineTrackerTheme.TEXT_MUTED};
            }}
        """)
        self.subtitle_label.setWordWrap(True)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()
    
    def update_value(self, new_value):
        """Değeri güncelle"""
        self.value = new_value
        self.value_label.setText(str(new_value))
    
    def update_subtitle(self, new_subtitle):
        """Alt yazıyı güncelle"""
        self.subtitle = new_subtitle
        self.subtitle_label.setText(new_subtitle)
    
    def paintEvent(self, event):
        """Custom painting - gradient background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        rect = self.rect()
        
        if self.gradient:
            # Gradient
            gradient = QLinearGradient(0, 0, 0, rect.height())
            
            base_color = QColor(MineTrackerTheme.SURFACE_LIGHT)
            accent_color = QColor(self.color)
            accent_color.setAlpha(30 if not self.hover else 50)
            
            gradient.setColorAt(0, base_color)
            gradient.setColorAt(1, accent_color)
            
            painter.setBrush(QBrush(gradient))
        else:
            painter.setBrush(QBrush(QColor(MineTrackerTheme.SURFACE)))
        
        # Border
        border_color = QColor(self.color if self.hover else MineTrackerTheme.BORDER)
        painter.setPen(QPen(border_color, 2 if self.hover else 1))
        
        # Draw rounded rect
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 12, 12)
        
        super().paintEvent(event)
    
    def enterEvent(self, event):
        """Mouse enter - hover effect"""
        self.hover = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse leave"""
        self.hover = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
