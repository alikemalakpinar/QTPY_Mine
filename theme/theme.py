"""Modern koyu tema - Professional Dark Theme"""

class MineTrackerTheme:
    """Modern, profesyonel koyu tema"""
    
    # Renk paleti
    BACKGROUND = "#0F0F0F"
    SURFACE = "#1A1A1A"
    SURFACE_LIGHT = "#252525"
    SURFACE_HOVER = "#2A2A2A"
    PRIMARY = "#00D4FF"
    PRIMARY_DARK = "#0099CC"
    PRIMARY_LIGHT = "#33DDFF"
    SUCCESS = "#00FF88"
    WARNING = "#FFB800"
    DANGER = "#FF3366"
    INFO = "#6C5CE7"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    TEXT_MUTED = "#707070"
    BORDER = "#2A2A2A"
    BORDER_LIGHT = "#3A3A3A"
    
    @staticmethod
    def get_app_style():
        """Ana uygulama stili"""
        return f"""
        QMainWindow {{
            background: {MineTrackerTheme.BACKGROUND};
        }}
        
        QWidget {{
            background: {MineTrackerTheme.BACKGROUND};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            font-family: -apple-system, 'Segoe UI', 'Inter', sans-serif;
            font-size: 14px;
        }}
        
        /* Buttons */
        QPushButton {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
        }}
        
        QPushButton:hover {{
            background: {MineTrackerTheme.SURFACE_HOVER};
            border-color: {MineTrackerTheme.PRIMARY};
        }}
        
        QPushButton:pressed {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}
        
        QPushButton:disabled {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_MUTED};
            border-color: {MineTrackerTheme.BORDER};
        }}
        
        /* Input Fields */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }}
        
        QLineEdit:focus, QComboBox:focus {{
            border-color: {MineTrackerTheme.PRIMARY};
            outline: none;
        }}
        
        /* ComboBox */
        QComboBox::drop-down {{
            border: none;
            padding-right: 10px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {MineTrackerTheme.TEXT_SECONDARY};
            width: 0;
            height: 0;
        }}
        
        QComboBox QAbstractItemView {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            selection-background-color: {MineTrackerTheme.PRIMARY};
            outline: none;
        }}
        
        /* Tables */
        QTableWidget {{
            background: {MineTrackerTheme.SURFACE};
            border: none;
            border-radius: 12px;
            gridline-color: {MineTrackerTheme.BORDER};
        }}
        
        QTableWidget::item {{
            padding: 12px;
            border-bottom: 1px solid {MineTrackerTheme.BORDER};
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}
        
        QTableWidget::item:selected {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}
        
        QHeaderView::section {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            color: {MineTrackerTheme.TEXT_SECONDARY};
            border: none;
            padding: 12px;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
        }}
        
        /* ScrollBars */
        QScrollBar:vertical {{
            background: {MineTrackerTheme.SURFACE};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            border-radius: 5px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}
        
        QScrollBar:horizontal {{
            background: {MineTrackerTheme.SURFACE};
            height: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            border-radius: 5px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {MineTrackerTheme.PRIMARY_DARK};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            width: 0px;
            height: 0px;
        }}
        
        /* Labels */
        QLabel {{
            color: {MineTrackerTheme.TEXT_PRIMARY};
            background: transparent;
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background: {MineTrackerTheme.SURFACE};
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 6px;
            text-align: center;
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}
        
        QProgressBar::chunk {{
            background: {MineTrackerTheme.PRIMARY};
            border-radius: 5px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_SECONDARY};
            border-top: 1px solid {MineTrackerTheme.BORDER};
        }}
        
        /* ToolTip */
        QToolTip {{
            background: {MineTrackerTheme.SURFACE_LIGHT};
            color: {MineTrackerTheme.TEXT_PRIMARY};
            border: 1px solid {MineTrackerTheme.PRIMARY};
            border-radius: 6px;
            padding: 5px;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {MineTrackerTheme.BORDER};
            border-radius: 8px;
            background: {MineTrackerTheme.SURFACE};
        }}
        
        QTabBar::tab {{
            background: {MineTrackerTheme.SURFACE};
            color: {MineTrackerTheme.TEXT_SECONDARY};
            border: 1px solid {MineTrackerTheme.BORDER};
            padding: 10px 20px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background: {MineTrackerTheme.PRIMARY};
            color: {MineTrackerTheme.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:hover {{
            background: {MineTrackerTheme.SURFACE_HOVER};
        }}
        """
    
    @staticmethod
    def get_card_style(hover=True):
        """Kart stili"""
        hover_style = f"""
            QWidget:hover {{
                border-color: {MineTrackerTheme.PRIMARY};
                background: {MineTrackerTheme.SURFACE_HOVER};
            }}
        """ if hover else ""
        
        return f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
            {hover_style}
        """
    
    @staticmethod
    def get_button_style(variant='primary'):
        """Buton stilleri"""
        styles = {
            'primary': {
                'bg': MineTrackerTheme.PRIMARY,
                'hover': MineTrackerTheme.PRIMARY_LIGHT,
                'pressed': MineTrackerTheme.PRIMARY_DARK,
                'text': '#000000'
            },
            'success': {
                'bg': MineTrackerTheme.SUCCESS,
                'hover': '#33FF99',
                'pressed': '#00DD77',
                'text': '#000000'
            },
            'danger': {
                'bg': MineTrackerTheme.DANGER,
                'hover': '#FF5577',
                'pressed': '#DD2244',
                'text': '#FFFFFF'
            },
            'warning': {
                'bg': MineTrackerTheme.WARNING,
                'hover': '#FFCC33',
                'pressed': '#DD9900',
                'text': '#000000'
            }
        }
        
        style = styles.get(variant, styles['primary'])
        
        return f"""
            QPushButton {{
                background: {style['bg']};
                color: {style['text']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {style['hover']};
            }}
            QPushButton:pressed {{
                background: {style['pressed']};
            }}
        """
