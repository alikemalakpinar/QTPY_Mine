"""Predictive Analytics & Blockchain Visualization - Tesla-Grade Data Experience"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from theme.theme import MineTrackerTheme
from datetime import datetime
from components.charts import RealtimeChart
import random


class AnalyticsScreen(QWidget):
    """Cinematic visualization of ML predictions and blockchain safety ledger"""

    def __init__(self, i18n, tracking, store):
        super().__init__()
        self.i18n = i18n
        self.tracking = tracking
        self.store = store

        # Simulated prediction data
        self._predictions = []
        self._ledger_blocks = []
        self._risk_scores = []

        self.init_ui()

        # Periodic data refresh
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(10000)

        # Initial data
        QTimer.singleShot(500, self.refresh_data)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(32, 28, 32, 28)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Tab-like layout: Predictive | Blockchain
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {MineTrackerTheme.BORDER};
                border-radius: 16px;
                background: {MineTrackerTheme.SURFACE};
            }}
            QTabBar::tab {{
                background: transparent;
                color: {MineTrackerTheme.TEXT_MUTED};
                border: none;
                border-bottom: 2px solid transparent;
                padding: 12px 28px;
                font-weight: 600;
                font-size: 13px;
            }}
            QTabBar::tab:selected {{
                color: {MineTrackerTheme.PRIMARY};
                border-bottom: 2px solid {MineTrackerTheme.PRIMARY};
            }}
            QTabBar::tab:hover:!selected {{
                color: {MineTrackerTheme.TEXT_SECONDARY};
            }}
        """)

        # Predictive tab
        predictive_tab = self.create_predictive_tab()
        self.tab_widget.addTab(predictive_tab, "AI Predictions")

        # Blockchain tab
        blockchain_tab = self.create_blockchain_tab()
        self.tab_widget.addTab(blockchain_tab, "Safety Ledger")

        main_layout.addWidget(self.tab_widget, 1)

    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title_section = QVBoxLayout()
        title_section.setSpacing(2)

        title = QLabel("Analytics & Intelligence")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: 800;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                letter-spacing: -1px;
            }}
        """)

        subtitle = QLabel("ML Predictions  ·  Blockchain Safety Ledger  ·  Risk Assessment")
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {MineTrackerTheme.TEXT_MUTED};
            }}
        """)

        title_section.addWidget(title)
        title_section.addWidget(subtitle)
        layout.addLayout(title_section)
        layout.addStretch()

        # Model accuracy badge
        accuracy_badge = QLabel("MODEL ACCURACY: 94.2%")
        accuracy_badge.setStyleSheet(f"""
            QLabel {{
                background: {MineTrackerTheme.SUCCESS};
                color: white;
                font-size: 10px;
                font-weight: 700;
                padding: 6px 14px;
                border-radius: 8px;
                letter-spacing: 0.5px;
            }}
        """)
        layout.addWidget(accuracy_badge)

        return header

    def create_predictive_tab(self):
        """AI Predictions visualization"""
        tab = QWidget()
        tab.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Top: Risk chart + Summary cards
        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        # Risk trend chart
        risk_container = QWidget()
        risk_container.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND_ELEVATED};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)
        risk_layout = QVBoxLayout(risk_container)
        risk_layout.setContentsMargins(12, 12, 12, 12)

        self.risk_chart = RealtimeChart("Risk Score Trend", max_points=20, y_range=(0, 1))
        self.risk_chart.line_color = QColor(MineTrackerTheme.DANGER)
        self.risk_chart.fill_color = QColor(MineTrackerTheme.DANGER)
        self.risk_chart.fill_color.setAlpha(40)
        risk_layout.addWidget(self.risk_chart)

        top_row.addWidget(risk_container, 2)

        # Summary metrics
        metrics_layout = QVBoxLayout()
        metrics_layout.setSpacing(12)

        self.metric_cards = {}
        metrics = [
            ('equipment_risk', 'Equipment Risk', '12%', MineTrackerTheme.WARNING),
            ('safety_score', 'Safety Score', '96%', MineTrackerTheme.SUCCESS),
            ('production_opt', 'Production +', '8.5%', MineTrackerTheme.PRIMARY),
            ('days_incident', 'Days No Incident', '42', MineTrackerTheme.CYAN),
        ]

        for key, label, value, color in metrics:
            card = self._create_mini_metric(label, value, color)
            self.metric_cards[key] = card
            metrics_layout.addWidget(card)

        top_row.addLayout(metrics_layout, 1)
        layout.addLayout(top_row)

        # Equipment predictions table
        equipment_section = self.create_equipment_predictions_section()
        layout.addWidget(equipment_section, 1)

        return tab

    def _create_mini_metric(self, label, value, color):
        """Small metric card"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND_ELEVATED};
                border-radius: 12px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(10)

        # Color indicator
        indicator = QLabel("●")
        indicator.setStyleSheet(f"QLabel {{ color: {color}; font-size: 8px; }}")

        # Label
        label_widget = QLabel(label.upper())
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {MineTrackerTheme.TEXT_MUTED};
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
        """)

        # Value
        value_widget = QLabel(value)
        value_widget.setObjectName("metric_value")
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 20px;
                font-weight: 300;
            }}
        """)

        layout.addWidget(indicator)
        layout.addWidget(label_widget)
        layout.addStretch()
        layout.addWidget(value_widget)

        return card

    def create_equipment_predictions_section(self):
        section = QWidget()
        section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND_ELEVATED};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        title = QLabel("Equipment Failure Predictions")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)

        ai_badge = QLabel("AI-POWERED")
        ai_badge.setStyleSheet(f"""
            QLabel {{
                background: {MineTrackerTheme.INFO};
                color: white;
                font-size: 9px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 4px;
            }}
        """)
        ai_badge.setFixedHeight(18)

        header_layout.addWidget(title)
        header_layout.addWidget(ai_badge)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        self.predictions_list = QListWidget()
        self.predictions_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 10px;
                padding: 12px;
                margin-bottom: 4px;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 12px;
            }}
            QListWidget::item:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
            }}
        """)
        layout.addWidget(self.predictions_list)

        return section

    def create_blockchain_tab(self):
        """Blockchain Safety Ledger visualization"""
        tab = QWidget()
        tab.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Chain stats
        chain_stats = QHBoxLayout()
        chain_stats.setSpacing(16)

        stats_data = [
            ('Total Blocks', '0', MineTrackerTheme.PRIMARY),
            ('Transactions', '0', MineTrackerTheme.SUCCESS),
            ('Compliance', '100%', MineTrackerTheme.CYAN),
            ('Chain Integrity', 'Valid', MineTrackerTheme.SUCCESS),
        ]

        self.chain_stat_labels = {}
        for label, value, color in stats_data:
            card = self._create_mini_metric(label, value, color)
            self.chain_stat_labels[label] = card
            chain_stats.addWidget(card)

        layout.addLayout(chain_stats)

        # Blockchain visualization
        chain_section = QWidget()
        chain_section.setStyleSheet(f"""
            QWidget {{
                background: {MineTrackerTheme.BACKGROUND_ELEVATED};
                border-radius: 16px;
                border: 1px solid {MineTrackerTheme.BORDER};
            }}
        """)

        chain_layout = QVBoxLayout(chain_section)
        chain_layout.setContentsMargins(20, 16, 20, 16)
        chain_layout.setSpacing(10)

        chain_header = QHBoxLayout()
        chain_title = QLabel("Safety Ledger Chain")
        chain_title.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 700;
                color: {MineTrackerTheme.TEXT_PRIMARY};
            }}
        """)

        immutable_badge = QLabel("IMMUTABLE")
        immutable_badge.setStyleSheet(f"""
            QLabel {{
                background: {MineTrackerTheme.CYAN};
                color: white;
                font-size: 9px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 4px;
            }}
        """)
        immutable_badge.setFixedHeight(18)

        chain_header.addWidget(chain_title)
        chain_header.addWidget(immutable_badge)
        chain_header.addStretch()
        chain_layout.addLayout(chain_header)

        self.blocks_list = QListWidget()
        self.blocks_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background: {MineTrackerTheme.SURFACE};
                border-radius: 10px;
                padding: 14px;
                margin-bottom: 6px;
                color: {MineTrackerTheme.TEXT_PRIMARY};
                font-size: 11px;
                font-family: 'SF Mono', 'Consolas', monospace;
                border-left: 3px solid {MineTrackerTheme.CYAN};
            }}
            QListWidget::item:hover {{
                background: {MineTrackerTheme.SURFACE_HOVER};
            }}
        """)
        chain_layout.addWidget(self.blocks_list)

        layout.addWidget(chain_section, 1)

        return tab

    def refresh_data(self):
        """Refresh all analytics data"""
        self._refresh_predictions()
        self._refresh_blockchain()

    def _refresh_predictions(self):
        """Generate fresh prediction data"""
        equipment_names = [
            'Excavator #7', 'Loader #12', 'Truck #25', 'Drill #3',
            'Crusher #1', 'Conveyor #2', 'Pump Station A', 'Ventilation Fan #4'
        ]

        self.predictions_list.clear()

        for name in equipment_names:
            prob = random.uniform(0.05, 0.85)
            days = int(max(1, (1 - prob) * 180))
            cost = int(prob * random.randint(20000, 80000))

            if prob > 0.6:
                severity = "CRITICAL"
                sev_color = MineTrackerTheme.DANGER
            elif prob > 0.4:
                severity = "WARNING"
                sev_color = MineTrackerTheme.WARNING
            else:
                severity = "NORMAL"
                sev_color = MineTrackerTheme.SUCCESS

            item_text = f"[{severity}]  {name}  ·  Failure: {prob:.0%}  ·  ~{days}d  ·  ${cost:,} risk"
            self.predictions_list.addItem(item_text)

        # Update risk chart
        risk_score = random.uniform(0.1, 0.6)
        self.risk_chart.add_data_point(risk_score)

        # Update metric cards
        self._update_metric_value('equipment_risk', f"{random.randint(5, 30)}%")
        self._update_metric_value('safety_score', f"{random.randint(88, 100)}%")
        self._update_metric_value('production_opt', f"+{random.uniform(3, 15):.1f}%")

    def _refresh_blockchain(self):
        """Generate blockchain ledger data"""
        import hashlib
        import json

        block_types = [
            ('safety_inspection', 'Safety Inspection', MineTrackerTheme.SUCCESS),
            ('equipment_maintenance', 'Equipment Maintenance', MineTrackerTheme.WARNING),
            ('training_record', 'Training Completed', MineTrackerTheme.INFO),
            ('incident_report', 'Incident Report', MineTrackerTheme.DANGER),
            ('compliance_check', 'Compliance Check', MineTrackerTheme.CYAN),
        ]

        block_type, block_name, color = random.choice(block_types)

        # Generate block hash
        block_data = {
            'type': block_type,
            'timestamp': datetime.now().isoformat(),
            'data': block_name,
            'nonce': random.randint(1000, 9999)
        }
        block_hash = hashlib.sha256(json.dumps(block_data).encode()).hexdigest()[:16]

        block_count = self.blocks_list.count() + 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        block_text = f"Block #{block_count}  ·  {timestamp}  ·  {block_name}  ·  Hash: {block_hash}..."

        self.blocks_list.insertItem(0, block_text)

        while self.blocks_list.count() > 20:
            self.blocks_list.takeItem(self.blocks_list.count() - 1)

        # Update chain stats
        self._update_metric_value('Total Blocks', str(block_count), is_chain=True)
        self._update_metric_value('Transactions', str(block_count * 3), is_chain=True)

    def _update_metric_value(self, key, value, is_chain=False):
        """Update a metric card's value"""
        source = self.chain_stat_labels if is_chain else self.metric_cards
        card = source.get(key)
        if card:
            value_label = card.findChild(QLabel, "metric_value")
            if value_label:
                value_label.setText(value)
