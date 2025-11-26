"""Premium Real-time Chart Widget with Smooth Animations"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from collections import deque
import math


class RealtimeChart(QWidget):
    """Premium real-time line chart with gradient fill and smooth animations"""

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
        self.animation.setDuration(300)
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
        """Draw premium chart"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        # Background with subtle gradient
        bg_gradient = QLinearGradient(0, 0, 0, rect.height())
        bg_gradient.setColorAt(0, QColor(MineTrackerTheme.SURFACE))
        bg_gradient.setColorAt(1, QColor(MineTrackerTheme.SURFACE_LIGHT))
        painter.fillRect(rect, bg_gradient)

        # Draw border
        painter.setPen(QPen(QColor(MineTrackerTheme.BORDER), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 12, 12)

        if len(self.data_series) < 2:
            # No data message
            painter.setPen(QColor(MineTrackerTheme.TEXT_MUTED))
            font = painter.font()
            font.setPointSize(11)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Waiting for data...")
            return

        # Chart area with padding
        margin_left = 50
        margin_right = 20
        margin_top = 45
        margin_bottom = 30
        chart_width = rect.width() - margin_left - margin_right
        chart_height = rect.height() - margin_top - margin_bottom

        # Draw horizontal grid lines
        painter.setPen(QPen(QColor(MineTrackerTheme.BORDER), 1, Qt.PenStyle.DotLine))
        num_grid_lines = 4
        for i in range(num_grid_lines + 1):
            y = margin_top + (chart_height * i / num_grid_lines)
            painter.drawLine(int(margin_left), int(y), int(rect.width() - margin_right), int(y))

            # Y-axis labels
            value = self.y_range[1] - (self.y_range[1] - self.y_range[0]) * i / num_grid_lines
            painter.setPen(QColor(MineTrackerTheme.TEXT_MUTED))
            font = painter.font()
            font.setPointSize(9)
            painter.setFont(font)
            painter.drawText(5, int(y + 4), f"{value:.0f}")
            painter.setPen(QPen(QColor(MineTrackerTheme.BORDER), 1, Qt.PenStyle.DotLine))

        # Calculate points
        points = []
        num_points = len(self.data_series)
        for i, value in enumerate(self.data_series):
            x = margin_left + (chart_width * i / max(1, num_points - 1))

            # Normalize value to chart range
            normalized = (value - self.y_range[0]) / max(0.001, self.y_range[1] - self.y_range[0])
            normalized = max(0, min(1, normalized))
            y = margin_top + chart_height - (chart_height * normalized)

            points.append(QPointF(x, y))

        # Draw fill gradient
        if len(points) >= 2:
            fill_path = QPainterPath()
            fill_path.moveTo(points[0].x(), margin_top + chart_height)
            fill_path.lineTo(points[0])

            # Smooth curve through points
            for i in range(1, len(points)):
                fill_path.lineTo(points[i])

            fill_path.lineTo(points[-1].x(), margin_top + chart_height)
            fill_path.closeSubpath()

            # Gradient fill
            fill_gradient = QLinearGradient(0, margin_top, 0, margin_top + chart_height)
            fill_start = QColor(self.line_color)
            fill_start.setAlpha(60)
            fill_end = QColor(self.line_color)
            fill_end.setAlpha(5)
            fill_gradient.setColorAt(0, fill_start)
            fill_gradient.setColorAt(1, fill_end)

            painter.fillPath(fill_path, QBrush(fill_gradient))

        # Draw smooth line
        if len(points) >= 2:
            line_path = QPainterPath()
            line_path.moveTo(points[0])

            for i in range(1, len(points)):
                line_path.lineTo(points[i])

            # Glow effect
            glow_pen = QPen(self.line_color, 8)
            glow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            glow_color = QColor(self.line_color)
            glow_color.setAlpha(30)
            glow_pen.setColor(glow_color)
            painter.setPen(glow_pen)
            painter.drawPath(line_path)

            # Main line
            line_pen = QPen(self.line_color, 3)
            line_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            line_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(line_pen)
            painter.drawPath(line_path)

        # Draw data points (only last few for clarity)
        if len(points) > 0:
            # Last point highlight
            last_point = points[-1]

            # Outer glow
            painter.setPen(Qt.PenStyle.NoPen)
            glow = QColor(self.line_color)
            glow.setAlpha(50)
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(last_point, 10, 10)

            # Inner dot
            painter.setBrush(QBrush(self.line_color))
            painter.drawEllipse(last_point, 5, 5)

            # White center
            painter.setBrush(QBrush(QColor("#ffffff")))
            painter.drawEllipse(last_point, 2, 2)

        # Draw title
        painter.setPen(QColor(MineTrackerTheme.TEXT_PRIMARY))
        font = painter.font()
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(margin_left, 25, self.title)

        # Draw current value badge
        if self.data_series:
            current_value = self.data_series[-1]

            # Badge background
            value_text = f"{current_value:.1f}"
            font_metrics = painter.fontMetrics()
            text_width = font_metrics.horizontalAdvance(value_text)
            badge_rect = QRectF(
                rect.width() - margin_right - text_width - 24,
                8,
                text_width + 20,
                26
            )

            badge_gradient = QLinearGradient(badge_rect.topLeft(), badge_rect.bottomRight())
            badge_gradient.setColorAt(0, self.line_color)
            badge_gradient.setColorAt(1, QColor(self.line_color).darker(120))

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(badge_gradient))
            painter.drawRoundedRect(badge_rect, 8, 8)

            # Value text
            painter.setPen(QColor("#ffffff"))
            font.setPointSize(11)
            font.setWeight(QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, value_text)
