"""Tesla-Grade Animation Manager - Smooth page transitions, fades, slides"""
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect, QStackedWidget
from PyQt6.QtCore import (
    QPropertyAnimation, QParallelAnimationGroup, QSequentialAnimationGroup,
    QEasingCurve, QPoint, QRect, pyqtProperty, QTimer, Qt, QObject, pyqtSignal
)
from PyQt6.QtGui import QColor


class AnimatedStackedWidget(QStackedWidget):
    """QStackedWidget with smooth fade + slide transitions between pages"""

    transition_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._transitioning = False
        self._duration = 300
        self._fade_opacity = 0.0

    def set_transition_duration(self, ms):
        self._duration = ms

    def slide_to(self, index):
        """Smooth fade transition to target index"""
        if self._transitioning or index == self.currentIndex():
            return
        if index < 0 or index >= self.count():
            return

        self._transitioning = True

        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        # Setup opacity effects
        current_effect = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(current_effect)
        current_effect.setOpacity(1.0)

        next_effect = QGraphicsOpacityEffect(next_widget)
        next_widget.setGraphicsEffect(next_effect)
        next_effect.setOpacity(0.0)

        # Show next widget on top
        next_widget.show()
        next_widget.raise_()

        # Fade out current
        fade_out = QPropertyAnimation(current_effect, b"opacity")
        fade_out.setDuration(self._duration // 2)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Fade in next
        fade_in = QPropertyAnimation(next_effect, b"opacity")
        fade_in.setDuration(self._duration // 2)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.InCubic)

        # Sequential: fade out then fade in
        group = QSequentialAnimationGroup(self)
        group.addAnimation(fade_out)
        group.addAnimation(fade_in)

        def on_finished():
            self.setCurrentIndex(index)
            # Clean up effects
            current_widget.setGraphicsEffect(None)
            next_widget.setGraphicsEffect(None)
            self._transitioning = False
            self.transition_finished.emit()

        group.finished.connect(on_finished)
        group.start()


class PulseAnimation(QObject):
    """Creates a pulsing glow effect for widgets - used for alert states"""

    value_changed = pyqtSignal(float)

    def __init__(self, parent=None, min_val=0.3, max_val=1.0, duration=1200):
        super().__init__(parent)
        self._value = min_val
        self._min = min_val
        self._max = max_val
        self._running = False

        # Forward pulse
        self._anim_forward = QPropertyAnimation(self, b"pulse_value")
        self._anim_forward.setDuration(duration // 2)
        self._anim_forward.setStartValue(min_val)
        self._anim_forward.setEndValue(max_val)
        self._anim_forward.setEasingCurve(QEasingCurve.Type.InOutSine)

        # Reverse pulse
        self._anim_reverse = QPropertyAnimation(self, b"pulse_value")
        self._anim_reverse.setDuration(duration // 2)
        self._anim_reverse.setStartValue(max_val)
        self._anim_reverse.setEndValue(min_val)
        self._anim_reverse.setEasingCurve(QEasingCurve.Type.InOutSine)

        # Loop
        self._group = QSequentialAnimationGroup(self)
        self._group.addAnimation(self._anim_forward)
        self._group.addAnimation(self._anim_reverse)
        self._group.setLoopCount(-1)  # Infinite

    @pyqtProperty(float)
    def pulse_value(self):
        return self._value

    @pulse_value.setter
    def pulse_value(self, val):
        self._value = val
        self.value_changed.emit(val)

    def start(self):
        if not self._running:
            self._running = True
            self._group.start()

    def stop(self):
        self._running = False
        self._group.stop()
        self._value = self._min


class SlideInAnimation:
    """Helper to create slide-in animations for widgets"""

    @staticmethod
    def from_bottom(widget, duration=300, offset=30):
        """Slide widget up from below with fade"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(0.0)

        # Fade in
        fade = QPropertyAnimation(effect, b"opacity")
        fade.setDuration(duration)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Slide up
        start_pos = widget.pos()
        slide = QPropertyAnimation(widget, b"pos")
        slide.setDuration(duration)
        slide.setStartValue(QPoint(start_pos.x(), start_pos.y() + offset))
        slide.setEndValue(start_pos)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        group = QParallelAnimationGroup(widget)
        group.addAnimation(fade)
        group.addAnimation(slide)

        def cleanup():
            widget.setGraphicsEffect(None)

        group.finished.connect(cleanup)
        return group

    @staticmethod
    def from_right(widget, duration=300, offset=40):
        """Slide widget in from the right with fade"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(0.0)

        fade = QPropertyAnimation(effect, b"opacity")
        fade.setDuration(duration)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(QEasingCurve.Type.OutCubic)

        start_pos = widget.pos()
        slide = QPropertyAnimation(widget, b"pos")
        slide.setDuration(duration)
        slide.setStartValue(QPoint(start_pos.x() + offset, start_pos.y()))
        slide.setEndValue(start_pos)
        slide.setEasingCurve(QEasingCurve.Type.OutCubic)

        group = QParallelAnimationGroup(widget)
        group.addAnimation(fade)
        group.addAnimation(slide)

        def cleanup():
            widget.setGraphicsEffect(None)

        group.finished.connect(cleanup)
        return group
