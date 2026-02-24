"""Tesla-Grade Dashboard - Real-time Analytics with OLED Aesthetic"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime
from components.charts import RealtimeChart, ModernStatCard
import random


class DashboardScreen(QWidget):
    """Tesla-caliber dashboard with giant metrics, minimal chrome, maximum data"""

    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store

        self.avg_accuracy_history = []
        self.active_personnel_history = []
        self.avg_battery_history = []

        self.init_ui()

        self.tracking.location_updated.connect(self.on_location_updated)
        self.tracking.position_calculated.connect(self.on_position_calculated)
        self.i18n.language_changed.connect(self.update_texts)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_all)
        self.update_timer.start(3000)

    def init_ui(self):
        """Initialize Tesla-grade UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(32, 28, 32, 28)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Stat cards
        stats_layout = self.create_modern_stats_cards()
        main_layout.addLayout(stats_layout)

        # Charts
        charts_layout = self.create_charts_section()
        main_layout.addLayout(charts_layout)

        # Bottom
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        left_section = self.create_recent_calculations_section()
        bottom_layout.addWidget(left_section, 3)

        right_section = self.create_anchor_metrics_section()
        bottom_layout.addWidget(right_section, 2)

        main_layout.addLayout(bottom_layout, 1)

    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        title_section = QVBoxLayout()
        title_section.setSpacing(2)

        self.title = QLabel(self.i18n.t('safety_dashboard'))
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 800;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -1px;
            }}
        """)

        self.subtitle = QLabel(f"{self.i18n.t('realtime_monitoring')}  ·  {datetime.now().strftime('%d %B %Y, %H:%M')}")
        self.subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {MineTrackerTheme.TEXT_MUTED};
                letter-spacing: 0.3px;
            }}
        """)

        title_section.addWidget(self.title)
        title_section.addWidget(self.subtitle)
        layout.addLayout(title_section)
        layout.addStretch()

        # Mode selector pill
        mode_group = QWidget()
        mode_group.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND_ELEVATED};
                border-radius: 10px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setSpacing(6)
        mode_layout.setContentsMargins(10, 6, 10, 6)

        mode_label = QLabel("MODE")
        mode_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1.5px;
            }}
        """)
        mode_layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Hybrid', 'Simulation', 'TCP Only'])
        self.mode_combo.setStyleSheet(f"""
            QComboBox {{
                background: transparent;
                border: none;
                padding: 4px 8px;
                font-weight: 600;
                font-size: 12px;
                min-width: 100px;
                color: {MineTrackerTheme.PRIMARY};
            }}
        """)
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)

        layout.addWidget(mode_group)
        return header

    def create_modern_stats_cards(self):
        layout = QHBoxLayout()
        layout.setSpacing(16)

        stats = self.tracking.get_statistics()

        self.card_active = ModernStatCard(
            icon='👷', title=self.i18n.t('active_personnel'),
            value=str(stats['personnel']['active']),
            subtitle=f"of {stats['personnel']['total']} underground",
            color=MineTrackerTheme.PRIMARY, gradient=True
        )
        self.card_active.clicked.connect(lambda: print("Navigate to Personnel"))

        self.card_anchors = ModernStatCard(
            icon='⚓', title='Anchors Online',
            value=f"{stats['anchors']['online']}/{stats['anchors']['total']}",
            subtitle='Coverage 100%',
            color=MineTrackerTheme.SUCCESS, gradient=True
        )

        self.card_tags = ModernStatCard(
            icon='🏷️', title='Active Tags',
            value=f"{stats['tags']['active']}/{stats['tags']['total']}",
            subtitle=f"Avg battery {stats['tags']['avg_battery']:.0f}%",
            color=MineTrackerTheme.INFO, gradient=True
        )

        avg_accuracy = self.calculate_avg_accuracy()
        self.card_accuracy = ModernStatCard(
            icon='🎯', title='Avg Accuracy',
            value=f"{avg_accuracy:.2f}m",
            subtitle='Trilateration + Kalman',
            color=MineTrackerTheme.WARNING if avg_accuracy > 1.0 else MineTrackerTheme.SUCCESS,
            gradient=True
        )

        layout.addWidget(self.card_active)
        layout.addWidget(self.card_anchors)
        layout.addWidget(self.card_tags)
        layout.addWidget(self.card_accuracy)
        return layout

    def create_charts_section(self):
        layout = QHBoxLayout()
        layout.setSpacing(16)

        # Accuracy
        ac = self.create_chart_container()
        al = QVBoxLayout()
        al.setContentsMargins(12, 12, 12, 12)
        self.accuracy_chart = RealtimeChart("Position Accuracy (m)", max_points=30, y_range=(0, 2))
        self.accuracy_chart.line_color = QColor(MineTrackerTheme.SUCCESS)
        self.accuracy_chart.fill_color = QColor(MineTrackerTheme.SUCCESS)
        self.accuracy_chart.fill_color.setAlpha(50)
        al.addWidget(self.accuracy_chart)
        ac.setLayout(al)

        # Battery
        bc = self.create_chart_container()
        bl = QVBoxLayout()
        bl.setContentsMargins(12, 12, 12, 12)
        self.battery_chart = RealtimeChart("Avg Battery (%)", max_points=30, y_range=(0, 100))
        self.battery_chart.line_color = QColor(MineTrackerTheme.WARNING)
        self.battery_chart.fill_color = QColor(MineTrackerTheme.WARNING)
        self.battery_chart.fill_color.setAlpha(50)
        bl.addWidget(self.battery_chart)
        bc.setLayout(bl)

        # Personnel
        pc = self.create_chart_container()
        pl = QVBoxLayout()
        pl.setContentsMargins(12, 12, 12, 12)
        self.personnel_chart = RealtimeChart("Active Personnel", max_points=30, y_range=(0, 20))
        self.personnel_chart.line_color = QColor(MineTrackerTheme.PRIMARY)
        self.personnel_chart.fill_color = QColor(MineTrackerTheme.PRIMARY)
        self.personnel_chart.fill_color.setAlpha(50)
        pl.addWidget(self.personnel_chart)
        pc.setLayout(pl)

        layout.addWidget(ac)
        layout.addWidget(bc)
        layout.addWidget(pc)
        return layout

    def create_chart_container(self):
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        return container

    def create_recent_calculations_section(self):
        section = QWidget()
        section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()
        title = QLabel("Recent Calculations")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)

        badge = QLabel("LIVE")
        badge.setStyleSheet(f"""
            QLabel {{
                background: {MineTrackerTheme.SUCCESS};
                color: white;
                font-size: 9px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 4px;
                letter-spacing: 0.5px;
            }}
        """)
        badge.setFixedHeight(18)

        header_layout.addWidget(title)
        header_layout.addWidget(badge)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        self.calculations_list = QListWidget()
        self.calculations_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 10px;
                padding: 10px 12px;
                margin-bottom: 4px;
                color: {MineTrackerTheme.TEXT_SECONDARY};
                font-size: 11px;
                font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
            }}
            QListWidget::item:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(self.calculations_list)
        return section

    def create_anchor_metrics_section(self):
        section = QWidget()
        section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        title = QLabel("Anchor Status")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)

        anchors = self.tracking.get_anchors()
        for anchor in anchors:
            anchor_widget = self.create_anchor_status_widget(anchor)
            layout.addWidget(anchor_widget)

        layout.addStretch()
        return section

    def create_anchor_status_widget(self, anchor):
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND};
                border-radius: 10px;
            }}
        """)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        status_dot = QLabel("●")
        dot_color = MineTrackerTheme.SUCCESS if anchor['status'] == 'online' else MineTrackerTheme.DANGER
        status_dot.setStyleSheet(f"QLabel {{ color: {dot_color}; font-size: 8px; }}")

        name_label = QLabel(anchor['name'])
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 12px;
                font-weight: 600;
            }}
        """)

        battery = anchor['battery']
        if battery < 70:
            color = MineTrackerTheme.DANGER
        elif battery < 85:
            color = MineTrackerTheme.WARNING
        else:
            color = MineTrackerTheme.TEXT_MUTED

        battery_label = QLabel(f"{battery}%")
        battery_label.setStyleSheet(f"QLabel {{ color: {color}; font-size: 11px; font-weight: 600; }}")

        layout.addWidget(status_dot)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(battery_label)
        return widget

    def calculate_avg_accuracy(self):
        personnel = self.tracking.get_personnel()
        accuracies = [p.get('position_accuracy', 0) for p in personnel if p.get('position_accuracy', 0) > 0]
        if not accuracies:
            return 0.5
        return sum(accuracies) / len(accuracies)

    def on_mode_changed(self, mode_text):
        mode_map = {'Hybrid': 'hybrid', 'Simulation': 'simulation', 'TCP Only': 'tcp'}
        self.tracking.set_mode(mode_map.get(mode_text, 'hybrid'))

    def on_location_updated(self, data):
        self.refresh_stats_quick()

    def on_position_calculated(self, data):
        tag_id = data.get('tag_id')
        accuracy = data.get('accuracy', 0)
        final_pos = data.get('final')
        anchors_used = data.get('anchors_used', [])
        timestamp = datetime.now().strftime('%H:%M:%S')
        item_text = f"[{timestamp}] {tag_id} → ({final_pos[0]:.1f}, {final_pos[1]:.1f}) ±{accuracy:.2f}m [{', '.join(anchors_used)}]"
        self.calculations_list.insertItem(0, item_text)
        while self.calculations_list.count() > 15:
            self.calculations_list.takeItem(self.calculations_list.count() - 1)

    def refresh_all(self):
        stats = self.tracking.get_statistics()
        self.card_active.update_value(str(stats['personnel']['active']))
        self.card_active.update_subtitle(f"of {stats['personnel']['total']} underground")
        self.card_anchors.update_value(f"{stats['anchors']['online']}/{stats['anchors']['total']}")
        self.card_tags.update_value(f"{stats['tags']['active']}/{stats['tags']['total']}")
        self.card_tags.update_subtitle(f"Avg battery {stats['tags']['avg_battery']:.0f}%")

        avg_accuracy = self.calculate_avg_accuracy()
        self.card_accuracy.update_value(f"{avg_accuracy:.2f}m")
        self.card_accuracy.color = QColor(MineTrackerTheme.WARNING if avg_accuracy > 1.0 else MineTrackerTheme.SUCCESS)
        self.card_accuracy.set_alert(avg_accuracy > 1.5)

        self.accuracy_chart.add_data_point(avg_accuracy)
        self.battery_chart.add_data_point(stats['tags']['avg_battery'])
        self.personnel_chart.add_data_point(stats['personnel']['active'])
        self.subtitle.setText(f"{self.i18n.t('realtime_monitoring')}  ·  {datetime.now().strftime('%d %B %Y, %H:%M:%S')}")

    def refresh_stats_quick(self):
        stats = self.tracking.get_statistics()
        self.card_active.update_value(str(stats['personnel']['active']))
        self.card_anchors.update_value(f"{stats['anchors']['online']}/{stats['anchors']['total']}")
        self.card_tags.update_value(f"{stats['tags']['active']}/{stats['tags']['total']}")

    def update_texts(self):
        self.title.setText(self.i18n.t('safety_dashboard'))
        self.subtitle.setText(f"{self.i18n.t('realtime_monitoring')}  ·  {datetime.now().strftime('%d %B %Y, %H:%M')}")
        self.refresh_all()
