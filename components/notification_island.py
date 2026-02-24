"""Dynamic Island Style Notification System - Apple-inspired expanding alerts"""
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize,
    pyqtSignal, pyqtProperty, QParallelAnimationGroup, QRect
)
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPen, QFont, QBrush, QPainterPath
from theme.theme import MineTrackerTheme


class DynamicIsland(QWidget):
    """
    Apple Dynamic Island-style notification widget.
    Normally a compact pill showing system status.
    Expands smoothly on alerts to show full details.
    """

    dismissed = pyqtSignal()

    COMPACT_WIDTH = 220
    COMPACT_HEIGHT = 36
    EXPANDED_WIDTH = 480
    EXPANDED_HEIGHT = 140

    def __init__(self, parent=None):
        super().__init__(parent)
        self._expanded = False
        self._expand_progress = 0.0
        self._alert_type = 'normal'  # normal, warning, danger, success
        self._alert_title = ''
        self._alert_message = ''
        self._alert_detail = ''
        self._pulse_value = 0.0

        self.setFixedSize(self.COMPACT_WIDTH, self.COMPACT_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Expand animation
        self._expand_anim = QPropertyAnimation(self, b"expand_progress")
        self._expand_anim.setDuration(400)
        self._expand_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        # Size animation
        self._size_anim = QPropertyAnimation(self, b"fixedSize")
        self._size_anim.setDuration(400)
        self._size_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        # Pulse animation for danger
        self._pulse_anim = QPropertyAnimation(self, b"pulse_val")
        self._pulse_anim.setDuration(800)
        self._pulse_anim.setStartValue(0.0)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._pulse_anim.setLoopCount(-1)

        # Auto-dismiss timer
        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self.collapse)

        # Status labels (compact mode)
        self._status_text = "System Online"
        self._status_color = QColor(MineTrackerTheme.SUCCESS)

    # --- Properties ---

    @pyqtProperty(float)
    def expand_progress(self):
        return self._expand_progress

    @expand_progress.setter
    def expand_progress(self, val):
        self._expand_progress = val
        self.update()

    @pyqtProperty(QSize)
    def fixedSize(self):
        return self.size()

    @fixedSize.setter
    def fixedSize(self, size):
        self.setFixedSize(size)
        self.update()

    @pyqtProperty(float)
    def pulse_val(self):
        return self._pulse_value

    @pulse_val.setter
    def pulse_val(self, val):
        self._pulse_value = val
        self.update()

    # --- Public API ---

    def show_alert(self, alert_type, title, message, detail='', auto_dismiss_ms=8000):
        """Show an expanded alert notification"""
        self._alert_type = alert_type
        self._alert_title = title
        self._alert_message = message
        self._alert_detail = detail
        self._expanded = True

        # Animate expansion
        self._size_anim.setStartValue(self.size())
        self._size_anim.setEndValue(QSize(self.EXPANDED_WIDTH, self.EXPANDED_HEIGHT))
        self._size_anim.start()

        self._expand_anim.setStartValue(self._expand_progress)
        self._expand_anim.setEndValue(1.0)
        self._expand_anim.start()

        # Start pulse for danger alerts
        if alert_type == 'danger':
            self._pulse_anim.start()
        else:
            self._pulse_anim.stop()
            self._pulse_value = 0.0

        # Auto dismiss
        if auto_dismiss_ms > 0:
            self._dismiss_timer.start(auto_dismiss_ms)

        # Re-center in parent
        self._recenter()

    def collapse(self):
        """Collapse back to compact pill"""
        self._expanded = False
        self._pulse_anim.stop()
        self._pulse_value = 0.0

        self._size_anim.setStartValue(self.size())
        self._size_anim.setEndValue(QSize(self.COMPACT_WIDTH, self.COMPACT_HEIGHT))
        self._size_anim.start()

        self._expand_anim.setStartValue(self._expand_progress)
        self._expand_anim.setEndValue(0.0)
        self._expand_anim.start()

        self._dismiss_timer.stop()
        self.dismissed.emit()

        # Re-center
        self._recenter()

    def set_status(self, text, color=None):
        """Update compact status text"""
        self._status_text = text
        if color:
            self._status_color = QColor(color)
        self.update()

    # --- Internal ---

    def _recenter(self):
        """Center the island in parent widget"""
        if self.parent():
            parent_width = self.parent().width()
            target_w = self.EXPANDED_WIDTH if self._expanded else self.COMPACT_WIDTH
            x = (parent_width - target_w) // 2
            self.move(x, 12)

    def _get_alert_color(self):
        colors = {
            'normal': QColor(MineTrackerTheme.PRIMARY),
            'success': QColor(MineTrackerTheme.SUCCESS),
            'warning': QColor(MineTrackerTheme.WARNING),
            'danger': QColor(MineTrackerTheme.DANGER),
            'info': QColor(MineTrackerTheme.INFO)
        }
        return colors.get(self._alert_type, QColor(MineTrackerTheme.PRIMARY))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        progress = self._expand_progress

        # Dynamic border radius
        radius = 18 + progress * 8  # 18 compact -> 26 expanded

        # Background
        path = QPainterPath()
        path.addRoundedRect(rect.adjusted(1, 1, -1, -1).toRectF(), radius, radius)

        # Fill with deep black
        bg_color = QColor(0, 0, 0, 240)
        painter.fillPath(path, QBrush(bg_color))

        # Subtle border
        alert_color = self._get_alert_color()
        border_alpha = int(40 + progress * 80)
        border_color = QColor(alert_color)
        border_color.setAlpha(border_alpha)
        painter.setPen(QPen(border_color, 1.0))
        painter.drawPath(path)

        # Pulse glow for danger
        if self._pulse_value > 0 and self._alert_type == 'danger':
            glow_alpha = int(self._pulse_value * 40)
            glow_color = QColor(MineTrackerTheme.DANGER)
            glow_color.setAlpha(glow_alpha)
            painter.setPen(QPen(glow_color, 2.0))
            painter.drawPath(path)

        if progress < 0.3:
            # === COMPACT MODE ===
            self._paint_compact(painter, rect)
        else:
            # === EXPANDED MODE ===
            self._paint_expanded(painter, rect, progress)

    def _paint_compact(self, painter, rect):
        """Draw compact pill status"""
        # Status dot
        dot_color = QColor(self._status_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(dot_color))
        painter.drawEllipse(16, rect.height() // 2 - 4, 8, 8)

        # Dot glow
        glow = QColor(dot_color)
        glow.setAlpha(40)
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(13, rect.height() // 2 - 7, 14, 14)

        # Status text
        painter.setPen(QColor(MineTrackerTheme.TEXT_SECONDARY))
        font = painter.font()
        font.setPointSize(10)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.drawText(34, 0, rect.width() - 44, rect.height(),
                         Qt.AlignmentFlag.AlignVCenter, self._status_text)

    def _paint_expanded(self, painter, rect, progress):
        """Draw expanded alert"""
        alert_color = self._get_alert_color()
        opacity = min(1.0, (progress - 0.3) / 0.7)

        # Top bar with color accent
        accent_rect = QRect(16, 12, int(rect.width() * 0.15), 3)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(alert_color))
        painter.drawRoundedRect(accent_rect, 2, 2)

        # Alert icon area
        icon_map = {
            'danger': '!',
            'warning': '!',
            'success': '✓',
            'info': 'i',
            'normal': '●'
        }
        icon_char = icon_map.get(self._alert_type, '●')

        icon_bg = QColor(alert_color)
        icon_bg.setAlpha(int(opacity * 40))
        painter.setBrush(QBrush(icon_bg))
        painter.drawRoundedRect(16, 24, 40, 40, 12, 12)

        painter.setPen(alert_color)
        font = painter.font()
        font.setPointSize(16)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(16, 24, 40, 40, Qt.AlignmentFlag.AlignCenter, icon_char)

        # Title
        title_color = QColor(MineTrackerTheme.TEXT_PRIMARY)
        title_color.setAlpha(int(opacity * 255))
        painter.setPen(title_color)
        font.setPointSize(13)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(68, 24, rect.width() - 84, 22,
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         self._alert_title)

        # Message
        msg_color = QColor(MineTrackerTheme.TEXT_SECONDARY)
        msg_color.setAlpha(int(opacity * 255))
        painter.setPen(msg_color)
        font.setPointSize(11)
        font.setWeight(QFont.Weight.Normal)
        painter.setFont(font)
        painter.drawText(68, 48, rect.width() - 84, 20,
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         self._alert_message)

        # Detail
        if self._alert_detail:
            detail_color = QColor(MineTrackerTheme.TEXT_MUTED)
            detail_color.setAlpha(int(opacity * 255))
            painter.setPen(detail_color)
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(16, 76, rect.width() - 32, 20,
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             self._alert_detail)

        # Dismiss hint
        hint_color = QColor(MineTrackerTheme.TEXT_MUTED)
        hint_color.setAlpha(int(opacity * 150))
        painter.setPen(hint_color)
        font.setPointSize(9)
        painter.setFont(font)
        painter.drawText(16, rect.height() - 30, rect.width() - 32, 20,
                         Qt.AlignmentFlag.AlignCenter,
                         "Click to dismiss")

    def mousePressEvent(self, event):
        if self._expanded:
            self.collapse()
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recenter()
