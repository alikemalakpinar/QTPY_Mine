"""Tesla-Grade Navigation Sidebar - Frosted Glass with Animated Indicator"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme


class NavigationBar(QWidget):
    """Premium frosted-glass navigation sidebar with animated active indicator"""

    page_changed = pyqtSignal(int)
    emergency_triggered = pyqtSignal()

    def __init__(self, i18n):
        super().__init__()
        self.i18n = i18n
        self.current_page = 0
        self.nav_buttons = []
        self._indicator_y = 0.0
        self.init_ui()

        self.i18n.language_changed.connect(self.update_texts)

        # Animated indicator
        self._indicator_anim = QPropertyAnimation(self, b"indicator_y")
        self._indicator_anim.setDuration(MineTrackerTheme.ANIM_NORMAL)
        self._indicator_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(float)
    def indicator_y(self):
        return self._indicator_y

    @indicator_y.setter
    def indicator_y(self, val):
        self._indicator_y = val
        self.update()

    def init_ui(self):
        """Initialize premium UI"""
        self.setFixedWidth(260)
        self.setStyleSheet(f"""
            NavigationBar {{
                background: {MineTrackerTheme.SURFACE};
                border-right: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Premium Logo Header
        header = self.create_header()
        layout.addWidget(header)

        # Spacer
        layout.addSpacing(8)

        # Navigation section label
        nav_label = QLabel("NAVIGATION")
        nav_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
                padding: 16px 24px 8px 24px;
            }}
        """)
        layout.addWidget(nav_label)

        # Navigation items
        self.nav_items = [
            ('◉', 'dashboard', 0),
            ('◎', 'live_map', 1),
            ('◈', 'personnel', 2),
            ('⬡', 'equipment', 3),
            ('⚠', 'emergency', 4),
            ('▤', 'reports', 5),
            ('◇', 'zones', 6),
            ('⚙', 'settings', 7)
        ]

        self._nav_container = QWidget()
        self._nav_layout = QVBoxLayout(self._nav_container)
        self._nav_layout.setContentsMargins(8, 0, 8, 0)
        self._nav_layout.setSpacing(2)

        for icon, key, index in self.nav_items:
            btn = self.create_nav_button(icon, key, index)
            self.nav_buttons.append(btn)
            self._nav_layout.addWidget(btn)

        layout.addWidget(self._nav_container)
        layout.addStretch()

        # Status section
        status_section = self.create_status_section()
        layout.addWidget(status_section)

        # Premium Emergency button
        emergency_btn = self.create_emergency_button()
        layout.addWidget(emergency_btn)

        # Select first page
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

    def create_header(self):
        """Create minimal premium header"""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QWidget {{
                background: transparent;
                border-bottom: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)

        # Logo icon
        logo_icon = QLabel("⛏")
        logo_icon.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                background: {MineTrackerTheme.GRADIENT_PRIMARY};
                border-radius: 10px;
                padding: 6px 10px;
            }}
        """)
        logo_icon.setFixedSize(44, 44)
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        logo_title = QLabel("MineTracker")
        logo_title.setStyleSheet(f"""
            QLabel {{
                font-size: 17px;
                font-weight: 800;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -0.5px;
            }}
        """)

        logo_version = QLabel("Pro v2.0")
        logo_version.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                font-weight: 600;
                color: {MineTrackerTheme.TEXT_MUTED};
                letter-spacing: 1px;
            }}
        """)

        text_layout.addWidget(logo_title)
        text_layout.addWidget(logo_version)

        layout.addWidget(logo_icon)
        layout.addLayout(text_layout)
        layout.addStretch()

        return header

    def create_nav_button(self, icon, text_key, index):
        """Create premium navigation button"""
        btn = QPushButton(f"  {icon}    {self.i18n.t(text_key)}")
        btn.setCheckable(True)
        btn.setFixedHeight(44)
        btn.setProperty('text_key', text_key)
        btn.setProperty('icon', icon)
        btn.setProperty('nav_index', index)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 10px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 500;
                text-align: left;
                padding-left: 16px;
            }}
            QPushButton:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
            QPushButton:checked {{
                background: {MineTrackerTheme.PRIMARY_SUBTLE};
                color: {MineTrackerTheme.PRIMARY};
                font-weight: 700;
            }}
        """)

        btn.clicked.connect(lambda: self.select_page(index))
        return btn

    def create_status_section(self):
        """Create system status indicator"""
        section = QWidget()
        section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND_ELEVATED};
                border-radius: 14px;
                margin: 12px 12px 0 12px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Status header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        status_dot = QLabel("●")
        status_dot.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.SUCCESS};
                font-size: 8px;
            }}
        """)
        status_text = QLabel("System Online")
        status_text.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 11px;
                font-weight: 600;
            }}
        """)
        header_layout.addWidget(status_dot)
        header_layout.addWidget(status_text)
        header_layout.addStretch()

        # Connection info
        connection_info = QLabel("TCP: 8888 · 6 Anchors")
        connection_info.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 10px;
            }}
        """)

        layout.addLayout(header_layout)
        layout.addWidget(connection_info)

        return section

    def create_emergency_button(self):
        """Create premium emergency button"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(12, 10, 12, 16)

        self.emergency_btn = QPushButton("🚨  " + self.i18n.t('emergency_button'))
        self.emergency_btn.setFixedHeight(48)
        self.emergency_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.emergency_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MineTrackerTheme.DANGER},
                    stop:1 {MineTrackerTheme.PINK});
                border: none;
                color: white;
                font-size: 13px;
                font-weight: 700;
                border-radius: 12px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MineTrackerTheme.DANGER_LIGHT},
                    stop:1 {MineTrackerTheme.PINK_LIGHT});
            }}
            QPushButton:pressed {{
                background: {MineTrackerTheme.DANGER};
            }}
        """)
        self.emergency_btn.clicked.connect(self.emergency_triggered.emit)

        container_layout.addWidget(self.emergency_btn)
        return container

    def select_page(self, index):
        """Select navigation page with animated indicator"""
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

        self.current_page = index
        self.page_changed.emit(index)

    def update_texts(self):
        """Update texts on language change"""
        self.emergency_btn.setText("🚨  " + self.i18n.t('emergency_button'))

        for btn in self.nav_buttons:
            text_key = btn.property('text_key')
            icon = btn.property('icon')
            if text_key and icon:
                btn.setText(f"  {icon}    {self.i18n.t(text_key)}")
