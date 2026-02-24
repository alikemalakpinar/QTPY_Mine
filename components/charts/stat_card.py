"""Tesla-Grade Stat Card - Giant Numbers, Muted Labels, Pulse Alerts"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme


class ModernStatCard(QWidget):
    """
    Premium stat card with Tesla-style typography:
    - Giant, thin value numbers (48px, Light weight)
    - Small, uppercase, muted labels
    - Pulse animation when value is in alert state
    - Smooth hover glow
    """

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
        self._pulse_value = 0.0
        self._alert_active = False

        self.setFixedHeight(150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"animation_value")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Pulse animation for alerts
        self._pulse_forward = QPropertyAnimation(self, b"pulse_value")
        self._pulse_forward.setDuration(600)
        self._pulse_forward.setStartValue(0.0)
        self._pulse_forward.setEndValue(1.0)
        self._pulse_forward.setEasingCurve(QEasingCurve.Type.InOutSine)

        self._pulse_reverse = QPropertyAnimation(self, b"pulse_value")
        self._pulse_reverse.setDuration(600)
        self._pulse_reverse.setStartValue(1.0)
        self._pulse_reverse.setEndValue(0.0)
        self._pulse_reverse.setEasingCurve(QEasingCurve.Type.InOutSine)

        self._pulse_group = QSequentialAnimationGroup(self)
        self._pulse_group.addAnimation(self._pulse_forward)
        self._pulse_group.addAnimation(self._pulse_reverse)
        self._pulse_group.setLoopCount(-1)

        self.init_ui()

    @pyqtProperty(float)
    def animation_value(self):
        return self._animation_value

    @animation_value.setter
    def animation_value(self, value):
        self._animation_value = value
        self.update()

    @pyqtProperty(float)
    def pulse_value(self):
        return self._pulse_value

    @pulse_value.setter
    def pulse_value(self, value):
        self._pulse_value = value
        self.update()

    def init_ui(self):
        """Create Tesla-style premium UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(6)

        # Top row: small icon + UPPERCASE label
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)

        # Small icon with subtle background
        icon_container = QWidget()
        icon_container.setFixedSize(32, 32)
        icon_container.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.color.name()},
                    stop:1 {self._adjust_color(self.color, 0.7).name()});
                border-radius: 8px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_label = QLabel(self.icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                background: transparent;
            }
        """)
        icon_layout.addWidget(self.icon_label)

        # Title - SMALL, UPPERCASE, MUTED
        self.title_label = QLabel(self.title.upper())
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_MUTED};
                letter-spacing: 1.5px;
                background: transparent;
            }}
        """)

        top_layout.addWidget(icon_container)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()

        # Value - GIANT, THIN weight
        self.value_label = QLabel(str(self.value))
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 48px;
                font-weight: 300;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -2px;
                background: transparent;
                margin-top: -2px;
            }}
        """)

        # Subtitle - small, muted
        self.subtitle_label = QLabel(self.subtitle)
        self.subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
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
        """Update value"""
        self.value = new_value
        self.value_label.setText(str(new_value))

    def update_subtitle(self, new_subtitle):
        """Update subtitle"""
        self.subtitle = new_subtitle
        self.subtitle_label.setText(new_subtitle)

    def set_alert(self, active=True):
        """Toggle pulse alert animation"""
        if active and not self._alert_active:
            self._alert_active = True
            self._pulse_group.start()
        elif not active and self._alert_active:
            self._alert_active = False
            self._pulse_group.stop()
            self._pulse_value = 0.0
            self.update()

    def paintEvent(self, event):
        """Custom painting - OLED black background with subtle glow"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        anim = self._animation_value
        pulse = self._pulse_value

        # Background - deep OLED surface
        bg = QLinearGradient(0, 0, rect.width(), rect.height())
        bg.setColorAt(0, QColor(MineTrackerTheme.SURFACE))
        bg.setColorAt(1, QColor(MineTrackerTheme.BACKGROUND_ELEVATED))
        painter.setBrush(QBrush(bg))

        # Border color
        if self._alert_active:
            border_color = QColor(self.color)
            border_color.setAlpha(int(80 + pulse * 175))
            pen_width = 1.0 + pulse * 0.5
        elif anim > 0:
            border_color = QColor(self.color)
            border_color.setAlpha(int(40 + anim * 120))
            pen_width = 1.0
        else:
            border_color = QColor(MineTrackerTheme.BORDER)
            pen_width = 1.0

        painter.setPen(QPen(border_color, pen_width))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 20, 20)

        # Left accent bar (thin, elegant)
        accent_rect = QRectF(0, rect.height() * 0.25, 3, rect.height() * 0.5)
        accent_color = QColor(self.color)
        if self._alert_active:
            accent_color.setAlpha(int(150 + pulse * 105))
        else:
            accent_color.setAlpha(180)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(accent_color))
        painter.drawRoundedRect(accent_rect, 1.5, 1.5)

        # Hover / Pulse glow overlay
        glow_alpha = 0
        if self._alert_active:
            glow_alpha = int(pulse * 15)
        elif anim > 0:
            glow_alpha = int(anim * 12)

        if glow_alpha > 0:
            glow_color = QColor(self.color)
            glow_color.setAlpha(glow_alpha)
            painter.setBrush(QBrush(glow_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 18, 18)

        super().paintEvent(event)

    def enterEvent(self, event):
        self.hover = True
        self.hover_animation.setStartValue(self._animation_value)
        self.hover_animation.setEndValue(1.0)
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover = False
        self.hover_animation.setStartValue(self._animation_value)
        self.hover_animation.setEndValue(0.0)
        self.hover_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
