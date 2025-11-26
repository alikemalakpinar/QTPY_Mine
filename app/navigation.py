"""Premium Modern Navigation Sidebar with Glass Morphism"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme


class NavigationBar(QWidget):
    """Premium glass morphism navigation sidebar"""

    page_changed = pyqtSignal(int)
    emergency_triggered = pyqtSignal()

    def __init__(self, i18n):
        super().__init__()
        self.i18n = i18n
        self.current_page = 0
        self.nav_buttons = []
        self.init_ui()

        # Language change listener
        self.i18n.language_changed.connect(self.update_texts)

    def init_ui(self):
        """Initialize premium UI"""
        self.setFixedWidth(280)
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MineTrackerTheme.SURFACE_LIGHT},
                    stop:1 {MineTrackerTheme.SURFACE});
                border-right: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Premium Logo Header
        header = self.create_header()
        layout.addWidget(header)

        # Navigation section label
        nav_label = QLabel("NAVIGATION")
        nav_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.5px;
                padding: 20px 28px 10px 28px;
            }}
        """)
        layout.addWidget(nav_label)

        # Navigation items with modern icons
        self.nav_items = [
            ('◉', 'dashboard', 0),        # Dashboard
            ('◎', 'live_map', 1),          # Live Map
            ('◈', 'personnel', 2),         # Personnel
            ('⬡', 'equipment', 3),         # Equipment
            ('⚠', 'emergency', 4),         # Emergency
            ('▤', 'reports', 5),           # Reports
            ('◇', 'zones', 6),             # Zones
            ('⚙', 'settings', 7)           # Settings
        ]

        for icon, key, index in self.nav_items:
            btn = self.create_nav_button(icon, key, index)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

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
        """Create premium header with logo"""
        header = QWidget()
        header.setFixedHeight(120)
        header.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MineTrackerTheme.SURFACE_HOVER},
                    stop:1 {MineTrackerTheme.SURFACE_LIGHT});
                border-bottom: 1px solid {MineTrackerTheme.BORDER};
                border-right: none;
            }}
        """)

        layout = QVBoxLayout(header)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        # Logo container
        logo_container = QHBoxLayout()
        logo_container.setSpacing(12)

        # Logo icon with gradient background
        logo_icon = QLabel("⛏")
        logo_icon.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                background: {MineTrackerTheme.GRADIENT_PRIMARY};
                border-radius: 12px;
                padding: 8px 12px;
            }}
        """)
        logo_icon.setFixedSize(56, 56)
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo text
        logo_text_layout = QVBoxLayout()
        logo_text_layout.setSpacing(2)

        logo_title = QLabel("MineTracker")
        logo_title.setStyleSheet(f"""
            QLabel {{
                font-size: 22px;
                font-weight: 800;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -0.5px;
            }}
        """)

        logo_version = QLabel("Pro v2.0")
        logo_version.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: 600;
                color: {MineTrackerTheme.PRIMARY};
                letter-spacing: 0.5px;
            }}
        """)

        logo_text_layout.addWidget(logo_title)
        logo_text_layout.addWidget(logo_version)

        logo_container.addWidget(logo_icon)
        logo_container.addLayout(logo_text_layout)
        logo_container.addStretch()

        layout.addLayout(logo_container)

        # Subtitle
        self.subtitle = QLabel(self.i18n.t('app_subtitle'))
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                margin-top: 4px;
            }}
        """)
        self.subtitle.setWordWrap(True)
        layout.addWidget(self.subtitle)

        return header

    def create_nav_button(self, icon, text_key, index):
        """Create premium navigation button"""
        btn = QPushButton(f"  {icon}    {self.i18n.t(text_key)}")
        btn.setCheckable(True)
        btn.setFixedHeight(52)
        btn.setProperty('text_key', text_key)
        btn.setProperty('icon', icon)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-left: 3px solid transparent;
                border-radius: 0px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                padding-left: 25px;
                margin: 2px 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {MineTrackerTheme.SURFACE_HOVER},
                    stop:1 transparent);
                color: {MineTrackerTheme.TEXT_PRIMARY};
                border-radius: 10px;
            }}
            QPushButton:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {MineTrackerTheme.PRIMARY}25,
                    stop:1 transparent);
                border-left: 3px solid {MineTrackerTheme.PRIMARY};
                border-radius: 0px;
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
                background: {MineTrackerTheme.SURFACE};
                border-radius: 12px;
                margin: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # Status header
        header_layout = QHBoxLayout()
        status_dot = QLabel("●")
        status_dot.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.SUCCESS};
                font-size: 10px;
            }}
        """)
        status_text = QLabel("System Online")
        status_text.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        header_layout.addWidget(status_dot)
        header_layout.addWidget(status_text)
        header_layout.addStretch()

        # Connection info
        connection_info = QLabel("TCP: 8888 • 6 Anchors")
        connection_info.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 11px;
            }}
        """)

        layout.addLayout(header_layout)
        layout.addWidget(connection_info)

        return section

    def create_emergency_button(self):
        """Create premium emergency button with gradient"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 8, 16, 20)

        self.emergency_btn = QPushButton("🚨  " + self.i18n.t('emergency_button'))
        self.emergency_btn.setFixedHeight(56)
        self.emergency_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.emergency_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MineTrackerTheme.DANGER},
                    stop:1 {MineTrackerTheme.PINK});
                border: none;
                color: white;
                font-size: 15px;
                font-weight: 700;
                border-radius: 14px;
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
        """Select navigation page"""
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

        self.current_page = index
        self.page_changed.emit(index)

    def update_texts(self):
        """Update texts on language change"""
        self.subtitle.setText(self.i18n.t('app_subtitle'))
        self.emergency_btn.setText("🚨  " + self.i18n.t('emergency_button'))

        for btn in self.nav_buttons:
            text_key = btn.property('text_key')
            icon = btn.property('icon')
            if text_key and icon:
                btn.setText(f"  {icon}    {self.i18n.t(text_key)}")
