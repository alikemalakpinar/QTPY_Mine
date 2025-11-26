"""Premium Modern Theme - Glass Morphism & Gradient Design System"""

class MineTrackerTheme:
    """Premium design system with glass morphism and modern aesthetics"""

    # Core Colors - Deep Rich Palette
    BACKGROUND = "#05070a"           # Ultra deep dark
    BACKGROUND_GRADIENT = "#0a0e14"  # Gradient end
    SURFACE = "#0d1117"              # GitHub dark style
    SURFACE_LIGHT = "#161b22"        # Elevated cards
    SURFACE_HOVER = "#21262d"        # Interactive hover
    SURFACE_GLASS = "rgba(13, 17, 23, 0.8)"  # Glass effect

    # Brand Colors - Vibrant Modern Palette
    PRIMARY = "#58a6ff"              # Bright blue
    PRIMARY_DARK = "#1f6feb"         # Deep blue
    PRIMARY_LIGHT = "#79c0ff"        # Light blue
    PRIMARY_GLOW = "#58a6ff40"       # Glow effect

    # Accent Colors - Rich & Vibrant
    SUCCESS = "#3fb950"              # Vivid green
    SUCCESS_LIGHT = "#56d364"        # Bright green
    SUCCESS_GLOW = "#3fb95040"

    WARNING = "#d29922"              # Rich gold
    WARNING_LIGHT = "#e3b341"        # Bright gold
    WARNING_GLOW = "#d2992240"

    DANGER = "#f85149"               # Vibrant red
    DANGER_LIGHT = "#ff7b72"         # Soft coral
    DANGER_GLOW = "#f8514940"

    INFO = "#a371f7"                 # Rich purple
    INFO_LIGHT = "#bc8cff"           # Light purple
    INFO_GLOW = "#a371f740"

    CYAN = "#39d2c0"                 # Teal accent
    CYAN_LIGHT = "#56e2d0"
    CYAN_GLOW = "#39d2c040"

    PINK = "#f778ba"                 # Modern pink
    PINK_LIGHT = "#ff9bce"
    PINK_GLOW = "#f778ba40"

    # Text Colors - Crisp & Readable
    TEXT_PRIMARY = "#f0f6fc"         # Pure white-ish
    TEXT_SECONDARY = "#8b949e"       # Soft gray
    TEXT_MUTED = "#484f58"           # Subtle gray
    TEXT_LINK = "#58a6ff"            # Link color

    # Borders & Shadows
    BORDER = "#21262d"               # Subtle border
    BORDER_LIGHT = "#30363d"         # Lighter border
    BORDER_ACTIVE = "#58a6ff"        # Active state

    # Gradients
    GRADIENT_PRIMARY = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #58a6ff, stop:1 #a371f7)"
    GRADIENT_SUCCESS = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3fb950, stop:1 #39d2c0)"
    GRADIENT_DANGER = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f85149, stop:1 #f778ba)"
    GRADIENT_WARM = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #d29922, stop:1 #f85149)"

    @staticmethod
    def get_app_style():
        """Modern premium application style"""
        return f"""
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {MineTrackerTheme.BACKGROUND},
                stop:1 {MineTrackerTheme.BACKGROUND_GRADIENT});
        }}

        QWidget {{
            background: transparent;
            color: {MineTrackerTheme.TEXT_PRIMARY};
            font-family: 'SF Pro Display', 'Inter', -apple-system, 'Segoe UI', sans-serif;
            font-size: 14px;
        }}

        /* Premium Buttons */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MineTrackerTheme.SURFACE_LIGHT},
                stop:1 {MineTrackerTheme.SURFACE});
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
        }}

        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MineTrackerTheme.SURFACE_HOVER},
                stop:1 {MineTrackerTheme.SURFACE_LIGHT});
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        QPushButton:pressed {{
            background: {MineTrackerTheme.PRIMARY_DARK};
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        QPushButton:disabled {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_MUTED};
            border-color: {MineTrackerTheme.BORDER};
        }}

        /* Glass Input Fields */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 14px;
            selection-background-color: {MineTrackerTheme.PRIMARY};
        }}

        QLineEdit:focus, QComboBox:focus {{
            border-color: {MineTrackerTheme.PRIMARY};
            background: {MineTrackerTheme.SURFACE_LIGHT};
        }}

        QLineEdit::placeholder {{
            color: {MineTrackerTheme.TEXT_MUTED};
        }}

        /* Modern ComboBox */
        QComboBox::drop-down {{
            border: none;
            padding-right: 12px;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {MineTrackerTheme.TEXT_SECONDARY};
            width: 0;
            height: 0;
        }}

        QComboBox QAbstractItemView {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 10px;
            selection-background-color: {MineTrackerTheme.PRIMARY_DARK};
            outline: none;
            padding: 5px;
        }}

        QComboBox QAbstractItemView::item {{
            padding: 10px 15px;
            border-radius: 6px;
            margin: 2px 5px;
        }}

        QComboBox QAbstractItemView::item:hover {{
            background: {MineTrackerTheme.SURFACE_HOVER};
        }}

        /* Premium Tables */
        QTableWidget {{
            background: {MineTrackerTheme.SURFACE};
            border: none;
            border-radius: 16px;
            gridline-color: {MineTrackerTheme.BORDER};
            alternate-background-color: {MineTrackerTheme.SURFACE_LIGHT};
        }}

        QTableWidget::item {{
            padding: 14px 16px;
            border-bottom: 1px solid {MineTrackerTheme.BORDER};
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}

        QTableWidget::item:selected {{
            background: {MineTrackerTheme.PRIMARY_DARK};
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}

        QTableWidget::item:hover {{
            background: {MineTrackerTheme.SURFACE_HOVER};
        }}

        QHeaderView::section {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MineTrackerTheme.SURFACE_LIGHT},
                stop:1 {MineTrackerTheme.SURFACE});
            color: {MineTrackerTheme.TEXT_SECONDARY};
            border: none;
            border-bottom: 2px solid {MineTrackerTheme.BORDER};
            padding: 14px 16px;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
        }}

        /* Modern ScrollBars */
        QScrollBar:vertical {{
            background: transparent;
            width: 12px;
            border-radius: 6px;
            margin: 4px;
        }}

        QScrollBar::handle:vertical {{
            background: {MineTrackerTheme.SURFACE_HOVER};
            border-radius: 6px;
            min-height: 40px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}

        QScrollBar:horizontal {{
            background: transparent;
            height: 12px;
            border-radius: 6px;
            margin: 4px;
        }}

        QScrollBar::handle:horizontal {{
            background: {MineTrackerTheme.SURFACE_HOVER};
            border-radius: 6px;
            min-width: 40px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}

        QScrollBar::add-line, QScrollBar::sub-line {{
            width: 0px;
            height: 0px;
        }}

        QScrollBar::add-page, QScrollBar::sub-page {{
            background: transparent;
        }}

        /* Labels */
        QLabel {{
            color: {MineTrackerTheme.TEXT_PRIMARY};
            background: transparent;
        }}

        /* Modern Progress Bar */
        QProgressBar {{
            background: {MineTrackerTheme.SURFACE};
            border: none;
            border-radius: 8px;
            text-align: center;
            color: {MineTrackerTheme.TEXT_PRIMARY};
            height: 10px;
        }}

        QProgressBar::chunk {{
            background: {MineTrackerTheme.GRADIENT_PRIMARY};
            border-radius: 8px;
        }}

        /* Status Bar */
        QStatusBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MineTrackerTheme.SURFACE},
                stop:1 {MineTrackerTheme.BACKGROUND});
            color: {MineTrackerTheme.TEXT_SECONDARY};
            border-top: 1px solid {MineTrackerTheme.BORDER};
            padding: 8px 16px;
        }}

        /* Elegant ToolTip */
        QToolTip {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 13px;
        }}

        /* Premium Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 12px;
            background: {MineTrackerTheme.SURFACE};
            top: -1px;
        }}

        QTabBar::tab {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_SECONDARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-bottom: none;
            padding: 12px 24px;
            margin-right: 4px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            font-weight: 600;
        }}

        QTabBar::tab:selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {MineTrackerTheme.PRIMARY},
                stop:1 {MineTrackerTheme.PRIMARY_DARK});
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        QTabBar::tab:hover:!selected {{
            background: {MineTrackerTheme.SURFACE_HOVER};
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}

        /* List Widget */
        QListWidget {{
            background: {MineTrackerTheme.SURFACE};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 12px;
            outline: none;
        }}

        QListWidget::item {{
            padding: 12px 16px;
            border-radius: 8px;
            margin: 4px 8px;
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}

        QListWidget::item:selected {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}

        QListWidget::item:hover {{
            background: {MineTrackerTheme.SURFACE_HOVER};
        }}

        /* Text Edit / Plain Text Edit */
        QTextEdit, QPlainTextEdit {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 12px;
            padding: 12px;
            font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
        }}

        QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        /* Group Box */
        QGroupBox {{
            background: {MineTrackerTheme.SURFACE};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 12px;
            margin-top: 20px;
            padding-top: 15px;
            font-weight: 600;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 20px;
            padding: 0 10px;
            color: {MineTrackerTheme.TEXT_SECONDARY};
        }}

        /* Slider */
        QSlider::groove:horizontal {{
            background: {MineTrackerTheme.SURFACE};
            height: 8px;
            border-radius: 4px;
        }}

        QSlider::handle:horizontal {{
            background: {MineTrackerTheme.PRIMARY};
            width: 20px;
            height: 20px;
            margin: -6px 0;
            border-radius: 10px;
        }}

        QSlider::handle:horizontal:hover {{
            background: {MineTrackerTheme.PRIMARY_LIGHT};
        }}

        QSlider::sub-page:horizontal {{
            background: {MineTrackerTheme.GRADIENT_PRIMARY};
            border-radius: 4px;
        }}

        /* CheckBox */
        QCheckBox {{
            color: {MineTrackerTheme.TEXT_PRIMARY};
            spacing: 10px;
        }}

        QCheckBox::indicator {{
            width: 22px;
            height: 22px;
            border-radius: 6px;
            border: 2px solid {MineTrackerTheme.BORDER};
            background: {MineTrackerTheme.SURFACE};
        }}

        QCheckBox::indicator:checked {{
            background: {MineTrackerTheme.PRIMARY};
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        QCheckBox::indicator:hover {{
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        /* Radio Button */
        QRadioButton {{
            color: {MineTrackerTheme.TEXT_PRIMARY};
            spacing: 10px;
        }}

        QRadioButton::indicator {{
            width: 22px;
            height: 22px;
            border-radius: 11px;
            border: 2px solid {MineTrackerTheme.BORDER};
            background: {MineTrackerTheme.SURFACE};
        }}

        QRadioButton::indicator:checked {{
            background: {MineTrackerTheme.PRIMARY};
            border-color: {MineTrackerTheme.PRIMARY};
        }}

        QRadioButton::indicator:hover {{
            border-color: {MineTrackerTheme.PRIMARY};
        }}
        """

    @staticmethod
    def get_card_style(hover=True):
        """Glass morphism card style"""
        hover_style = f"""
            QWidget:hover {{
                border-color: {MineTrackerTheme.PRIMARY};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MineTrackerTheme.SURFACE_HOVER},
                    stop:1 {MineTrackerTheme.SURFACE_LIGHT});
            }}
        """ if hover else ""

        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MineTrackerTheme.SURFACE_LIGHT},
                    stop:1 {MineTrackerTheme.SURFACE});
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
            {hover_style}
        """

    @staticmethod
    def get_glass_card_style():
        """Premium glass card with glow effect"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(22, 27, 34, 0.95),
                    stop:1 rgba(13, 17, 23, 0.95));
                border-radius: 20px;
                border: 1px solid {MineTrackerTheme.BORDER_LIGHT};
            }}
        """

    @staticmethod
    def get_button_style(variant='primary'):
        """Premium gradient button styles"""
        styles = {
            'primary': {
                'bg': MineTrackerTheme.GRADIENT_PRIMARY,
                'hover': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #79c0ff, stop:1 #bc8cff)',
                'pressed': MineTrackerTheme.PRIMARY_DARK,
                'text': '#ffffff',
                'glow': MineTrackerTheme.PRIMARY_GLOW
            },
            'success': {
                'bg': MineTrackerTheme.GRADIENT_SUCCESS,
                'hover': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #56d364, stop:1 #56e2d0)',
                'pressed': MineTrackerTheme.SUCCESS,
                'text': '#ffffff',
                'glow': MineTrackerTheme.SUCCESS_GLOW
            },
            'danger': {
                'bg': MineTrackerTheme.GRADIENT_DANGER,
                'hover': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff7b72, stop:1 #ff9bce)',
                'pressed': MineTrackerTheme.DANGER,
                'text': '#ffffff',
                'glow': MineTrackerTheme.DANGER_GLOW
            },
            'warning': {
                'bg': MineTrackerTheme.GRADIENT_WARM,
                'hover': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3b341, stop:1 #ff7b72)',
                'pressed': MineTrackerTheme.WARNING,
                'text': '#ffffff',
                'glow': MineTrackerTheme.WARNING_GLOW
            },
            'ghost': {
                'bg': 'transparent',
                'hover': MineTrackerTheme.SURFACE_HOVER,
                'pressed': MineTrackerTheme.SURFACE_LIGHT,
                'text': MineTrackerTheme.TEXT_PRIMARY,
                'glow': 'transparent'
            }
        }

        style = styles.get(variant, styles['primary'])

        return f"""
            QPushButton {{
                background: {style['bg']};
                color: {style['text']};
                border: none;
                border-radius: 12px;
                padding: 14px 28px;
                font-weight: 700;
                font-size: 14px;
                letter-spacing: 0.3px;
            }}
            QPushButton:hover {{
                background: {style['hover']};
            }}
            QPushButton:pressed {{
                background: {style['pressed']};
            }}
        """

    @staticmethod
    def get_stat_card_style(color):
        """Gradient stat card with glow"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MineTrackerTheme.SURFACE_LIGHT},
                    stop:0.5 {MineTrackerTheme.SURFACE},
                    stop:1 {MineTrackerTheme.SURFACE_LIGHT});
                border-radius: 20px;
                border: 1px solid {MineTrackerTheme.BORDER};
                border-left: 4px solid {color};
            }}
            QWidget:hover {{
                border-color: {color};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MineTrackerTheme.SURFACE_HOVER},
                    stop:1 {MineTrackerTheme.SURFACE_LIGHT});
            }}
        """
