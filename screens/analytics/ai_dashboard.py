class AIDashboardScreen(QWidget):
    """Advanced AI Analytics Dashboard - Million Dollar Interface"""
    
    def __init__(self):
        super().__init__()
        self.predictive_engine = PredictiveAnalyticsEngine()
        self.current_predictions = {}
        self.init_ui()
        self.connect_ai_engine()
        
    def init_ui(self):
        """Initialize AI dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_ai_header()
        layout.addWidget(header)
        
        # AI Status Cards
        status_cards = self.create_ai_status_cards()
        layout.addWidget(status_cards)
        
        # Main AI Content
        main_content = self.create_ai_content()
        layout.addWidget(main_content, 1)
        
    def create_ai_header(self):
        """Create AI dashboard header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        
        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        
        title = QLabel("🤖 AI Predictive Analytics")
        title.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                font-size: 32px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel("Enterprise AI • Predictive Intelligence • $50M+ Value Generated")
        subtitle.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 16px;
                margin-top: 5px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # AI Status Indicator
        status_widget = self.create_ai_status_indicator()
        
        layout.addWidget(title_widget)
        layout.addStretch()
        layout.addWidget(status_widget)
        
        return header
    
    def create_ai_status_indicator(self):
        """Create AI system status indicator"""
        status_widget = QWidget()
        status_widget.setFixedSize(200, 80)
        status_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                border: 2px solid #4c6ef5;
            }
        """)
        
        layout = QVBoxLayout(status_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        status_label = QLabel("🧠 AI ACTIVE")
        status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        accuracy_label = QLabel("94.2% Accuracy")
        accuracy_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 11px;
            }
        """)
        
        layout.addWidget(status_label)
        layout.addWidget(accuracy_label)
        
        return status_widget
    
    def create_ai_status_cards(self):
        """Create AI performance status cards"""
        cards_widget = QWidget()
        layout = QHBoxLayout(cards_widget)
        layout.setSpacing(20)
        
        # AI Performance Cards
        cards_data = [
            ("Predictions Generated", "2,847", "🎯", "#4c6ef5", "Last 30 days", "↗️ +23%"),
            ("Money Saved", "$2.4M", "💰", "#51cf66", "This quarter", "↗️ +156%"),
            ("Failures Prevented", "17", "🛡️", "#ff6b6b", "This month", "↗️ +89%"),
            ("Efficiency Gain", "31.2%", "⚡", "#ffd43b", "Production boost", "↗️ +12%"),
            ("Risk Reduction", "67%", "📉", "#845ef7", "Safety incidents", "↗️ +34%")
        ]
        
        for title, value, icon, color, subtitle, trend in cards_data:
            card = self.create_ai_performance_card(title, value, icon, color, subtitle, trend)
            layout.addWidget(card)
        
        return cards_widget
    
    def create_ai_performance_card(self, title, value, icon, color, subtitle, trend):
        """Create individual AI performance card"""
        card = QWidget()
        card.setFixedHeight(140)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
            }}
            QWidget:hover {{
                border: 2px solid {color};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 {color}08);
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Header
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                font-weight: 600;
            }
        """)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 32px;
                font-weight: bold;
            }}
        """)
        
        # Footer
        footer_layout = QHBoxLayout()
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #999;
                font-size: 10px;
            }
        """)
        
        trend_label = QLabel(trend)
        trend_label.setStyleSheet("""
            QLabel {
                color: #28a745;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        
        footer_layout.addWidget(subtitle_label)
        footer_layout.addStretch()
        footer_layout.addWidget(trend_label)
        
        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        layout.addLayout(footer_layout)
        
        return card
    
    def create_ai_content(self):
        """Create main AI content area"""
        content_widget = QWidget()
        layout = QHBoxLayout(content_widget)
        layout.setSpacing(20)
        
        # Left: Predictions Panel
        predictions_panel = self.create_predictions_panel()
        
        # Right: AI Insights Panel  
        insights_panel = self.create_insights_panel()
        
        layout.addWidget(predictions_panel, 3)
        layout.addWidget(insights_panel, 2)
        
        return content_widget
    
    def create_predictions_panel(self):
        """Create AI predictions panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🎯 AI Predictions & Recommendations")
        title.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        
        refresh_btn = QPushButton("🔄 Refresh AI")
        refresh_btn.clicked.connect(self.refresh_predictions)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd8, stop:1 #6a42a0);
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Predictions scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.predictions_widget = QWidget()
        self.predictions_layout = QVBoxLayout(self.predictions_widget)
        self.predictions_layout.setSpacing(15)
        
        scroll_area.setWidget(self.predictions_widget)
        layout.addWidget(scroll_area, 1)
        
        return panel
    
    def create_insights_panel(self):
        """Create AI insights panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        
        # Financial Impact Card
        financial_card = self.create_financial_impact_card()
        layout.addWidget(financial_card)
        
        # Production Optimization Card
        optimization_card = self.create_optimization_card()
        layout.addWidget(optimization_card)
        
        # Risk Assessment Card
        risk_card = self.create_risk_assessment_card()
        layout.addWidget(risk_card)
        
        return panel
    
    def create_financial_impact_card(self):
        """Create financial impact visualization card"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #11998e, stop:1 #38ef7d);
                border-radius: 16px;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        title = QLabel("💰 Financial Impact")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        amount = QLabel("$47.2M")
        amount.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin: 10px 0;
            }
        """)
        
        description = QLabel("Total value generated by AI\nthis year through predictions\nand optimizations")
        description.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(amount)
        layout.addWidget(description)
        layout.addStretch()
        
        return card
    
    def create_optimization_card(self):
        """Create production optimization card"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("⚡ Production Optimization")
        title.setStyleSheet("""
            QLabel {
                color: #1a1a1a;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        metrics = [
            ("Current Output", "1,247 tons/day", "#ffd43b"),
            ("AI Optimized", "1,623 tons/day", "#51cf66"),
            ("Potential Gain", "+30.1%", "#4c6ef5") 
        ]