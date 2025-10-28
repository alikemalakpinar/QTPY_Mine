"""Enterprise Grade Theme - Aico Design System"""

class AicoTheme:
    """Aico Maden Takip - Professional design system"""
    
    # Core Colors - Professional Palette
    BACKGROUND = "#0a0b0d"          # Deep space
    SURFACE = "#111827"             # Elevated surface
    SURFACE_LIGHT = "#1f2937"       # Light surface
    SURFACE_HOVER = "#374151"       # Hover state
    
    # Brand Colors - Modern & Clean
    PRIMARY = "#3B82F6"             # Professional blue
    PRIMARY_DARK = "#2563EB"        # Darker blue
    PRIMARY_LIGHT = "#60A5FA"       # Light blue
    
    SUCCESS = "#10B981"             # Modern green
    WARNING = "#F59E0B"             # Amber
    DANGER = "#EF4444"              # Clean red
    INFO = "#8B5CF6"                # Purple
    
    # Text Colors - Accessible
    TEXT_PRIMARY = "#F9FAFB"        # Almost white
    TEXT_SECONDARY = "#9CA3AF"      # Gray 400
    TEXT_MUTED = "#6B7280"          # Gray 500
    
    # Borders - Subtle
    BORDER = "#1f2937"              # Match surface
    BORDER_LIGHT = "#374151"        # Subtle borders
    
    @staticmethod
    def get_app_style():
        """Ana uygulama stili"""
        return f"""
        QMainWindow {{
            background: {AicoTheme.BACKGROUND};
        }}
        
        QWidget {{
            background: {AicoTheme.BACKGROUND};
            color: {AicoTheme.TEXT_PRIMARY};
            font-family: -apple-system, 'Segoe UI', 'Inter', sans-serif;
            font-size: 14px;
        }}
        
        /* Buttons */
        QPushButton {{
            background: {AicoTheme.SURFACE_LIGHT};
            color: {AicoTheme.TEXT_PRIMARY};
            border: 1px solid {AicoTheme.BORDER};
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
        }}
        
        QPushButton:hover {{
            background: {AicoTheme.SURFACE_HOVER};
            border-color: {AicoTheme.PRIMARY};
        }}
        
        QPushButton:pressed {{
            background: {AicoTheme.PRIMARY_DARK};
        }}
        
        QPushButton:disabled {{
            background: {AicoTheme.SURFACE};
            color: {AicoTheme.TEXT_MUTED};
            border-color: {AicoTheme.BORDER};
        }}
        
        /* Input Fields */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background: {AicoTheme.SURFACE};
            color: {AicoTheme.TEXT_PRIMARY};
            border: 1px solid {AicoTheme.BORDER};
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }}
        
        QLineEdit:focus, QComboBox:focus {{
            border-color: {AicoTheme.PRIMARY};
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
            border-top: 5px solid {AicoTheme.TEXT_SECONDARY};
            width: 0;
            height: 0;
        }}
        
        QComboBox QAbstractItemView {{
            background: {AicoTheme.SURFACE_LIGHT};
            color: {AicoTheme.TEXT_PRIMARY};
            border: 1px solid {AicoTheme.BORDER};
            selection-background-color: {AicoTheme.PRIMARY};
            outline: none;
        }}
        
        /* Tables */
        QTableWidget {{
            background: {AicoTheme.SURFACE};
            border: none;
            border-radius: 12px;
            gridline-color: {AicoTheme.BORDER};
        }}
        
        QTableWidget::item {{
            padding: 12px;
            border-bottom: 1px solid {AicoTheme.BORDER};
            color: {AicoTheme.TEXT_PRIMARY};
        }}
        
        QTableWidget::item:selected {{
            background: {AicoTheme.PRIMARY_DARK};
        }}
        
        QHeaderView::section {{
            background: {AicoTheme.SURFACE_LIGHT};
            color: {AicoTheme.TEXT_SECONDARY};
            border: none;
            padding: 12px;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
        }}
        
        /* ScrollBars */
        QScrollBar:vertical {{
            background: {AicoTheme.SURFACE};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {AicoTheme.SURFACE_LIGHT};
            border-radius: 5px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {AicoTheme.PRIMARY_DARK};
        }}
        
        QScrollBar:horizontal {{
            background: {AicoTheme.SURFACE};
            height: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {AicoTheme.SURFACE_LIGHT};
            border-radius: 5px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {AicoTheme.PRIMARY_DARK};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            width: 0px;
            height: 0px;
        }}
        
        /* Labels */
        QLabel {{
            color: {AicoTheme.TEXT_PRIMARY};
            background: transparent;
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background: {AicoTheme.SURFACE};
            border: 1px solid {AicoTheme.BORDER};
            border-radius: 6px;
            text-align: center;
            color: {AicoTheme.TEXT_PRIMARY};
        }}
        
        QProgressBar::chunk {{
            background: {AicoTheme.PRIMARY};
            border-radius: 5px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background: {AicoTheme.SURFACE};
            color: {AicoTheme.TEXT_SECONDARY};
            border-top: 1px solid {AicoTheme.BORDER};
        }}
        
        /* ToolTip */
        QToolTip {{
            background: {AicoTheme.SURFACE_LIGHT};
            color: {AicoTheme.TEXT_PRIMARY};
            border: 1px solid {AicoTheme.PRIMARY};
            border-radius: 6px;
            padding: 5px;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {AicoTheme.BORDER};
            border-radius: 8px;
            background: {AicoTheme.SURFACE};
        }}
        
        QTabBar::tab {{
            background: {AicoTheme.SURFACE};
            color: {AicoTheme.TEXT_SECONDARY};
            border: 1px solid {AicoTheme.BORDER};
            padding: 10px 20px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background: {AicoTheme.PRIMARY};
            color: {AicoTheme.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:hover {{
            background: {AicoTheme.SURFACE_HOVER};
        }}
        """
    
    @staticmethod
    def get_card_style(hover=True):
        """Kart stili"""
        hover_style = f"""
            QWidget:hover {{
                border-color: {AicoTheme.PRIMARY};
                background: {AicoTheme.SURFACE_HOVER};
            }}
        """ if hover else ""
        
        return f"""
            QWidget {{
                background: {AicoTheme.SURFACE};
                border-radius: 12px;
                border: 1px solid {AicoTheme.BORDER};
            }}
            {hover_style}
        """
    
    @staticmethod
    def get_button_style(variant='primary'):
        """Buton stilleri"""
        styles = {
            'primary': {
                'bg': AicoTheme.PRIMARY,
                'hover': AicoTheme.PRIMARY_LIGHT,
                'pressed': AicoTheme.PRIMARY_DARK,
                'text': '#000000'
            },
            'success': {
                'bg': AicoTheme.SUCCESS,
                'hover': '#33FF99',
                'pressed': '#00DD77',
                'text': '#000000'
            },
            'danger': {
                'bg': AicoTheme.DANGER,
                'hover': '#FF5577',
                'pressed': '#DD2244',
                'text': '#FFFFFF'
            },
            'warning': {
                'bg': AicoTheme.WARNING,
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
