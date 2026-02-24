"""Tesla-Grade Real-time Chart - Smooth Bezier Curves, Gradient Fill, Glow"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from collections import deque
import math


class RealtimeChart(QWidget):
    """Premium real-time line chart with smooth bezier curves and cinematic gradient fill"""

    def __init__(self, title="Chart", max_points=50, y_range=(0, 100)):
        super().__init__()
        self.title = title
        self.max_points = max_points
        self.y_range = y_range
        self.data_series = deque(maxlen=max_points)
        self.setMinimumHeight(180)

        # Colors
        self.line_color = QColor(MineTrackerTheme.PRIMARY)
        self.fill_color = QColor(MineTrackerTheme.PRIMARY)
        self.fill_color.setAlpha(40)
        self.grid_color = QColor(MineTrackerTheme.BORDER)

        # Animation
        self._animation_progress = 0.0
        self.animation = QPropertyAnimation(self, b"animation_progress")
        self.animation.setDuration(350)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(float)
    def animation_progress(self):
        return self._animation_progress

    @animation_progress.setter
    def animation_progress(self, value):
        self._animation_progress = value
        self.update()

    def add_data_point(self, value):
        """Add new data point with animation"""
        self.data_series.append(value)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def clear_data(self):
        """Clear all data"""
        self.data_series.clear()
        self.update()

    def paintEvent(self, event):
        """Draw premium chart with OLED black background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        # OLED black background with very subtle gradient
        bg_gradient = QLinearGradient(0, 0, 0, rect.height())
        bg_gradient.setColorAt(0, QColor(MineTrackerTheme.SURFACE))
        bg_gradient.setColorAt(1, QColor(MineTrackerTheme.BACKGROUND_ELEVATED))
        painter.fillRect(rect, bg_gradient)

        # Subtle border
        painter.setPen(QPen(QColor(MineTrackerTheme.BORDER), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 16, 16)

        if len(self.data_series) < 2:
            painter.setPen(QColor(MineTrackerTheme.TEXT_MUTED))
            font = painter.font()
            font.setPointSize(10)
            font.setWeight(QFont.Weight.DemiBold)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Waiting for data...")
            return

        # Chart area
        margin_left = 45
        margin_right = 16
        margin_top = 42
        margin_bottom = 24
        chart_width = rect.width() - margin_left - margin_right
        chart_height = rect.height() - margin_top - margin_bottom

        # Horizontal grid lines - very subtle
        num_grid_lines = 3
        for i in range(num_grid_lines + 1):
            y = margin_top + (chart_height * i / num_grid_lines)
            painter.setPen(QPen(QColor(MineTrackerTheme.BORDER), 0.5, Qt.PenStyle.DotLine))
            painter.drawLine(int(margin_left), int(y), int(rect.width() - margin_right), int(y))

            value = self.y_range[1] - (self.y_range[1] - self.y_range[0]) * i / num_grid_lines
            painter.setPen(QColor(MineTrackerTheme.TEXT_MUTED))
            font = painter.font()
            font.setPointSize(8)
            font.setWeight(QFont.Weight.Normal)
            painter.setFont(font)
            painter.drawText(4, int(y + 3), f"{value:.0f}")

        # Calculate points
        points = []
        num_points = len(self.data_series)
        for i, value in enumerate(self.data_series):
            x = margin_left + (chart_width * i / max(1, num_points - 1))
            normalized = (value - self.y_range[0]) / max(0.001, self.y_range[1] - self.y_range[0])
            normalized = max(0, min(1, normalized))
            y = margin_top + chart_height - (chart_height * normalized)
            points.append(QPointF(x, y))

        if len(points) < 2:
            return

        # Build smooth bezier path
        line_path = QPainterPath()
        line_path.moveTo(points[0])

        for i in range(1, len(points)):
            prev = points[i - 1]
            curr = points[i]
            cp_x = (prev.x() + curr.x()) / 2
            line_path.cubicTo(cp_x, prev.y(), cp_x, curr.y(), curr.x(), curr.y())

        # Fill path
        fill_path = QPainterPath(line_path)
        fill_path.lineTo(points[-1].x(), margin_top + chart_height)
        fill_path.lineTo(points[0].x(), margin_top + chart_height)
        fill_path.closeSubpath()

        # Gradient fill
        fill_gradient = QLinearGradient(0, margin_top, 0, margin_top + chart_height)
        fill_start = QColor(self.line_color)
        fill_start.setAlpha(45)
        fill_mid = QColor(self.line_color)
        fill_mid.setAlpha(15)
        fill_end = QColor(self.line_color)
        fill_end.setAlpha(0)
        fill_gradient.setColorAt(0, fill_start)
        fill_gradient.setColorAt(0.4, fill_mid)
        fill_gradient.setColorAt(1, fill_end)
        painter.fillPath(fill_path, QBrush(fill_gradient))

        # Line glow
        glow_pen = QPen(self.line_color, 10)
        glow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        glow_color = QColor(self.line_color)
        glow_color.setAlpha(18)
        glow_pen.setColor(glow_color)
        painter.setPen(glow_pen)
        painter.drawPath(line_path)

        # Main line
        line_pen = QPen(self.line_color, 2.5)
        line_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        line_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(line_pen)
        painter.drawPath(line_path)

        # Last point highlight
        if len(points) > 0:
            last_point = points[-1]

            painter.setPen(Qt.PenStyle.NoPen)
            glow = QColor(self.line_color)
            glow.setAlpha(30)
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(last_point, 12, 12)

            glow.setAlpha(50)
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(last_point, 7, 7)

            painter.setBrush(QBrush(self.line_color))
            painter.drawEllipse(last_point, 4, 4)

            painter.setBrush(QBrush(QColor("#ffffff")))
            painter.drawEllipse(last_point, 1.5, 1.5)

        # Title
        painter.setPen(QColor(MineTrackerTheme.TEXT_SECONDARY))
        font = painter.font()
        font.setPointSize(10)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.drawText(margin_left, 22, self.title)

        # Current value badge
        if self.data_series:
            current_value = self.data_series[-1]
            value_text = f"{current_value:.1f}"
            font_metrics = painter.fontMetrics()
            text_width = font_metrics.horizontalAdvance(value_text)
            badge_rect = QRectF(
                rect.width() - margin_right - text_width - 20,
                8,
                text_width + 16,
                22
            )

            badge_color = QColor(self.line_color)
            badge_color.setAlpha(30)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(badge_color))
            painter.drawRoundedRect(badge_rect, 6, 6)

            painter.setPen(self.line_color)
            font.setPointSize(10)
            font.setWeight(QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, value_text)
