# theme/theme.py - Improved theme with PyQt6 compatible CSS
class MineGuardTheme:
    def __init__(self):
        self.colors = {
            'primary': '#007bff',
            'secondary': '#6c757d',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'background': '#ffffff',
            'surface': '#f5f5f5',
        }
        
    def get_main_style(self):
        """Get main application stylesheet - PyQt6 compatible"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QWidget {
                font-family: "Segoe UI", "San Francisco", "Helvetica Neue", Arial, sans-serif;
            }
            
            QScrollBar:vertical {
                background-color: #f1f1f1;
                width: 12px;
                border-radius: 6px;
                border: none;
            }
            
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 6px;
                min-height: 20px;
                border: none;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8a8;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                border: none;
            }
            
            QScrollBar:horizontal {
                background-color: #f1f1f1;
                height: 12px;
                border-radius: 6px;
                border: none;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #c1c1c1;
                border-radius: 6px;
                min-width: 20px;
                border: none;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #a8a8a8;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                border: none;
            }
            
            /* Remove unsupported properties */
            QPushButton {
                border-style: solid;
                border-width: 1px;
            }
            
            QPushButton:hover {
                /* Hover effects without unsupported properties */
            }
        """