"""Premium Stat Card Component with Glass Morphism"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme


class ModernStatCard(QWidget):
    """Premium glass morphism stat card with smooth animations"""

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
        self._animation_value = 0.0

        self.setFixedHeight(160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"animation_value")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.init_ui()

    @pyqtProperty(float)
    def animation_value(self):
        return self._animation_value

    @animation_value.setter
    def animation_value(self, value):
        self._animation_value = value
        self.update()

    def init_ui(self):
        """Create premium UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        # Top - Icon and Title
        top_layout = QHBoxLayout()
        top_layout.setSpacing(14)

        # Icon container with gradient background
        icon_container = QWidget()
        icon_container.setFixedSize(48, 48)
        icon_container.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.color.name()},
                    stop:1 {self._adjust_color(self.color, 0.7).name()});
                border-radius: 12px;
            }}
        """)

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_label = QLabel(self.icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                color: white;
                background: transparent;
            }
        """)
        icon_layout.addWidget(self.icon_label)

        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                text-transform: uppercase;
                letter-spacing: 1px;
                background: transparent;
            }}
        """)

        top_layout.addWidget(icon_container)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()

        # Value with gradient text effect (simulated)
        self.value_label = QLabel(str(self.value))
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 44px;
                font-weight: 800;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -1px;
                background: transparent;
            }}
        """)

        # Subtitle with muted color
        self.subtitle_label = QLabel(self.subtitle)
        self.subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {MineTrackerTheme.TEXT_MUTED};
                background: transparent;
            }}
        """)
        self.subtitle_label.setWordWrap(True)

        layout.addLayout(top_layout)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()

    def _adjust_color(self, color, factor):
        """Adjust color brightness"""
        h, s, l, a = color.getHslF()
        new_l = min(1.0, l * factor)
        new_color = QColor()
        new_color.setHslF(h, s, new_l, a)
        return new_color

    def update_value(self, new_value):
        """Update value with animation effect"""
        self.value = new_value
        self.value_label.setText(str(new_value))

    def update_subtitle(self, new_subtitle):
        """Update subtitle"""
        self.subtitle = new_subtitle
        self.subtitle_label.setText(new_subtitle)

    def paintEvent(self, event):
        """Custom painting - premium glass effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        anim = self._animation_value

        # Background gradient
        if self.gradient:
            gradient = QLinearGradient(0, 0, rect.width(), rect.height())

            # Base colors
            base_start = QColor(MineTrackerTheme.SURFACE_LIGHT)
            base_end = QColor(MineTrackerTheme.SURFACE)

            # Accent overlay
            accent = QColor(self.color)
            accent.setAlpha(int(20 + anim * 30))

            gradient.setColorAt(0, base_start)
            gradient.setColorAt(0.5, base_end)
            gradient.setColorAt(1, base_start)

            painter.setBrush(QBrush(gradient))
        else:
            painter.setBrush(QBrush(QColor(MineTrackerTheme.SURFACE)))

        # Border with color transition
        border_color = QColor(MineTrackerTheme.BORDER)
        if anim > 0:
            border_color = QColor(self.color)
            border_color.setAlpha(int(100 + anim * 155))

        pen_width = 1 + anim
        painter.setPen(QPen(border_color, pen_width))

        # Draw rounded rect
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 16, 16)

        # Left accent bar
        accent_rect = QRectF(1, rect.height() * 0.2, 4, rect.height() * 0.6)
        accent_gradient = QLinearGradient(0, accent_rect.top(), 0, accent_rect.bottom())
        accent_gradient.setColorAt(0, self.color)
        accent_gradient.setColorAt(1, self._adjust_color(self.color, 0.6))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(accent_gradient))
        painter.drawRoundedRect(accent_rect, 2, 2)

        # Hover glow effect
        if anim > 0:
            glow_color = QColor(self.color)
            glow_color.setAlpha(int(anim * 30))
            painter.setBrush(QBrush(glow_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 14, 14)

        super().paintEvent(event)

    def enterEvent(self, event):
        """Mouse enter - smooth hover animation"""
        self.hover = True
        self.hover_animation.setStartValue(self._animation_value)
        self.hover_animation.setEndValue(1.0)
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse leave - smooth exit"""
        self.hover = False
        self.hover_animation.setStartValue(self._animation_value)
        self.hover_animation.setEndValue(0.0)
        self.hover_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Click handler"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
