from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime, timedelta
import random
from theme.theme import MineTrackerTheme

class PersonDetailScreen(QWidget):
    back_requested = pyqtSignal()
    
    def __init__(self, i18n, tracking, store, person_id):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store
        self.person_id = person_id
        self.person = self.tracking.get_person_by_id(person_id)
        
        if not self.person:
            return
            
        self.work_start_time = datetime.now() - timedelta(hours=random.randint(2, 6), minutes=random.randint(0, 59))
        self.total_break_time = timedelta(minutes=random.randint(15, 45))
        self.last_break = datetime.now() - timedelta(minutes=random.randint(30, 120))
        
        self.init_ui()
        
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_time_info)
        self.refresh_timer.start(1000)
        
        self.tracking.location_updated.connect(self.on_location_update)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        header = self.create_header()
        layout.addWidget(header)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)
        
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        left_column.addWidget(self.create_profile_card())
        left_column.addWidget(self.create_location_card())
        left_column.addWidget(self.create_health_card())
        
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        
        right_column.addWidget(self.create_time_tracking_card())
        right_column.addWidget(self.create_activity_card())
        
        content_layout.addLayout(left_column, 1)
        content_layout.addLayout(right_column, 1)
        
        layout.addLayout(content_layout)
    
    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        back_btn = QPushButton("← Geri")
        back_btn.setFixedSize(100, 40)
        back_btn.setStyleSheet(MineTrackerTheme.get_button_style('primary'))
        back_btn.clicked.connect(self.back_requested.emit)
        
        title_layout = QVBoxLayout()
        title = QLabel(f"👤 {self.person['full_name']}")
        title.setStyleSheet(f"font-size: 32px; font-weight: 700; color: {MineTrackerTheme.TEXT_PRIMARY};")
        
        subtitle = QLabel(self.person['position'])
        subtitle.setStyleSheet(f"font-size: 16px; color: {MineTrackerTheme.TEXT_SECONDARY}; margin-top: 5px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addWidget(back_btn)
        layout.addLayout(title_layout)
        layout.addStretch()
        
        status_badge = self.create_status_badge()
        layout.addWidget(status_badge)
        
        return header
    
    def create_status_badge(self):
        status = self.person['status']
        status_colors = {
            'active': (MineTrackerTheme.SUCCESS, '🟢 Aktif'),
            'break': (MineTrackerTheme.WARNING, '🟡 Molada'),
            'emergency': (MineTrackerTheme.DANGER, '🔴 Acil Durum')
        }
        
        color, text = status_colors.get(status, (MineTrackerTheme.TEXT_SECONDARY, 'Bilinmiyor'))
        
        badge = QLabel(text)
        badge.setStyleSheet(f"""
            background: {color};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
        """)
        return badge
    
    def create_profile_card(self):
        card = QWidget()
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        title = QLabel("📋 Profil Bilgileri")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {MineTrackerTheme.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        info_items = [
            ("Personel ID", self.person['id']),
            ("Pozisyon", self.person['position']),
            ("Vardiya", self.person.get('shift', 'N/A')),
            ("Giriş Saati", self.person.get('entry_time', 'N/A')),
            ("Telefon", self.person.get('phone', 'N/A')),
            ("E-posta", self.person.get('email', 'N/A')),
            ("Tag ID", self.person.get('tag_id', 'N/A'))
        ]
        
        for label, value in info_items:
            row = QHBoxLayout()
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-size: 13px;")
            
            value_widget = QLabel(str(value))
            value_widget.setStyleSheet(f"color: {MineTrackerTheme.TEXT_PRIMARY}; font-size: 14px; font-weight: 600;")
            value_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
            
            row.addWidget(label_widget)
            row.addStretch()
            row.addWidget(value_widget)
            layout.addLayout(row)
        
        return card
    
    def create_location_card(self):
        card = QWidget()
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        title = QLabel("📍 Konum Bilgisi")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {MineTrackerTheme.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        zone_label = QLabel(f"Bölge: {self.person['zone_name']}")
        zone_label.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {MineTrackerTheme.PRIMARY};")
        layout.addWidget(zone_label)
        
        loc = self.person['location']
        coords_layout = QHBoxLayout()
        
        for axis, value in [('X', loc['x']), ('Y', loc['y']), ('Z', loc['z'])]:
            coord_widget = QWidget()
            coord_layout = QVBoxLayout(coord_widget)
            coord_layout.setSpacing(5)
            
            axis_label = QLabel(axis)
            axis_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-size: 12px;")
            axis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            value_label = QLabel(f"{value:.1f}m")
            value_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_PRIMARY}; font-size: 18px; font-weight: 700;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            coord_layout.addWidget(axis_label)
            coord_layout.addWidget(value_label)
            coords_layout.addWidget(coord_widget)
        
        layout.addLayout(coords_layout)
        
        self.last_update_label = QLabel(f"Son Güncelleme: Az önce")
        self.last_update_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_MUTED}; font-size: 12px;")
        layout.addWidget(self.last_update_label)
        
        return card
    
    def create_health_card(self):
        card = QWidget()
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        title = QLabel("💓 Sağlık & Durum")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {MineTrackerTheme.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        metrics_layout = QHBoxLayout()
        
        heart_widget = self.create_metric_widget("💓", "Kalp Atışı", f"{self.person['heart_rate']}", "bpm")
        battery_widget = self.create_metric_widget("🔋", "Tag Bataryası", f"{self.person['battery']}", "%")
        signal_widget = self.create_metric_widget("📶", "Sinyal Gücü", f"{self.person['signal']}", "%")
        
        metrics_layout.addWidget(heart_widget)
        metrics_layout.addWidget(battery_widget)
        metrics_layout.addWidget(signal_widget)
        
        layout.addLayout(metrics_layout)
        
        return card
    
    def create_metric_widget(self, icon, label, value, unit):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-size: 12px;")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_widget = QLabel(f"{value}{unit}")
        value_widget.setStyleSheet(f"color: {MineTrackerTheme.TEXT_PRIMARY}; font-size: 20px; font-weight: 700;")
        value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(icon_label)
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        
        return widget
    
    def create_time_tracking_card(self):
        card = QWidget()
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        title = QLabel("⏱️ Zaman Takibi")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {MineTrackerTheme.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        self.work_duration_label = QLabel()
        self.work_duration_label.setStyleSheet(f"font-size: 32px; font-weight: 700; color: {MineTrackerTheme.PRIMARY};")
        self.work_duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.work_duration_label)
        
        work_label = QLabel("Toplam Çalışma Süresi")
        work_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-size: 13px;")
        work_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(work_label)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet(f"background: {MineTrackerTheme.BORDER};")
        layout.addWidget(divider)
        
        stats_layout = QHBoxLayout()
        
        break_col = QVBoxLayout()
        self.break_time_label = QLabel()
        self.break_time_label.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {MineTrackerTheme.WARNING};")
        self.break_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        break_label = QLabel("Mola Süresi")
        break_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-size: 12px;")
        break_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        break_col.addWidget(self.break_time_label)
        break_col.addWidget(break_label)
        
        active_col = QVBoxLayout()
        self.active_time_label = QLabel()
        self.active_time_label.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {MineTrackerTheme.SUCCESS};")
        self.active_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        active_label = QLabel("Aktif Çalışma")
        active_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_SECONDARY}; font-size: 12px;")
        active_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        active_col.addWidget(self.active_time_label)
        active_col.addWidget(active_label)
        
        stats_layout.addLayout(break_col)
        stats_layout.addLayout(active_col)
        
        layout.addLayout(stats_layout)
        
        self.update_time_info()
        
        return card
    
    def create_activity_card(self):
        card = QWidget()
        card.setStyleSheet(MineTrackerTheme.get_card_style(hover=False))
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        title = QLabel("📊 Son Aktiviteler")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {MineTrackerTheme.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
        """)
        
        activities_widget = QWidget()
        activities_layout = QVBoxLayout(activities_widget)
        activities_layout.setSpacing(10)
        
        activities = [
            {"time": "2 dakika önce", "action": "Sektör C'ye giriş yaptı", "icon": "📍"},
            {"time": "15 dakika önce", "action": "Molayı bitirdi", "icon": "☕"},
            {"time": "30 dakika önce", "action": "Mola başlattı", "icon": "⏸️"},
            {"time": "1 saat önce", "action": "Ana Galeri'de çalışmaya başladı", "icon": "⛏️"},
            {"time": "2 saat önce", "action": "Vardiyaya giriş yaptı", "icon": "🚪"}
        ]
        
        for activity in activities:
            activity_item = self.create_activity_item(activity['icon'], activity['action'], activity['time'])
            activities_layout.addWidget(activity_item)
        
        activities_layout.addStretch()
        scroll.setWidget(activities_widget)
        layout.addWidget(scroll)
        
        return card
    
    def create_activity_item(self, icon, action, time):
        item = QWidget()
        layout = QHBoxLayout(item)
        layout.setContentsMargins(10, 10, 10, 10)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px;")
        icon_label.setFixedSize(30, 30)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        
        action_label = QLabel(action)
        action_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_PRIMARY}; font-size: 13px; font-weight: 500;")
        
        time_label = QLabel(time)
        time_label.setStyleSheet(f"color: {MineTrackerTheme.TEXT_MUTED}; font-size: 11px;")
        
        text_layout.addWidget(action_label)
        text_layout.addWidget(time_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        item.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE_LIGHT};
                border-radius: 8px;
            }}
            QWidget:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
            }}
        """)
        
        return item
    
    def update_time_info(self):
        work_duration = datetime.now() - self.work_start_time
        active_duration = work_duration - self.total_break_time
        
        def format_duration(td):
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        
        self.work_duration_label.setText(format_duration(work_duration))
        self.break_time_label.setText(format_duration(self.total_break_time))
        self.active_time_label.setText(format_duration(active_duration))
    
    def on_location_update(self, data):
        if data.get('type') == 'personnel' and data.get('data', {}).get('id') == self.person_id:
            self.person = data['data']
            self.last_update_label.setText("Son Güncelleme: Az önce")
