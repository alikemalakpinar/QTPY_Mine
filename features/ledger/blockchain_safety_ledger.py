import hashlib
import json
import time
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class BlockchainSafetyLedger(QObject):
    """Enterprise blockchain ledger for mining safety compliance"""
    
    block_added = pyqtSignal(dict)
    compliance_alert = pyqtSignal(dict)
    audit_ready = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.chain = []
        self.pending_transactions = []
        self.mining_difficulty = 4
        self.mining_reward = 100
        
        # Create genesis block
        self.create_genesis_block()
        
        # Auto-mining timer
        self.mining_timer = QTimer()
        self.mining_timer.timeout.connect(self.auto_mine_pending_transactions)
        self.mining_timer.start(15000)  # Mine every 15 seconds
        
        # Compliance checker
        self.compliance_timer = QTimer()
        self.compliance_timer.timeout.connect(self.check_compliance)
        self.compliance_timer.start(60000)  # Check every minute
        
    def create_genesis_block(self):
        """Create the genesis block"""
        genesis_block = {
            'index': 0,
            'timestamp': datetime.now().isoformat(),
            'transactions': [{
                'type': 'genesis',
                'description': 'MineGuard Safety Ledger Genesis Block',
                'data': {
                    'system': 'MineGuard Safety Management',
                    'version': '1.0.0',
                    'initialized': datetime.now().isoformat(),
                    'compliance_standards': [
                        'ISO 45001', 'MSHA Standards', 'OSHA Regulations',
                        'ILO Mining Safety', 'ICMM Principles'
                    ]
                }
            }],
            'previous_hash': '0',
            'nonce': 0
        }
        
        genesis_block['hash'] = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)
        print("🔗 Genesis block created for MineGuard Safety Ledger")
    
    def calculate_hash(self, block):
        """Calculate SHA-256 hash of a block"""
        block_string = json.dumps(block, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def get_latest_block(self):
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_safety_incident(self, incident_data):
        """Add safety incident to the blockchain"""
        transaction = {
            'type': 'safety_incident',
            'timestamp': datetime.now().isoformat(),
            'incident_id': f"INC-{len(self.chain):05d}",
            'data': {
                'severity': incident_data.get('severity', 'medium'),
                'location': incident_data.get('location', 'Unknown'),
                'personnel_involved': incident_data.get('personnel', []),
                'equipment_involved': incident_data.get('equipment', []),
                'description': incident_data.get('description', ''),
                'immediate_actions': incident_data.get('actions', []),
                'investigation_status': 'pending',
                'reported_by': incident_data.get('reporter', 'System'),
                'compliance_impact': self.assess_compliance_impact(incident_data)
            },
            'immutable': True,
            'verified': True
        }
        
        self.pending_transactions.append(transaction)
        print(f"🚨 Safety incident added to ledger: {transaction['incident_id']}")
        return transaction['incident_id']
    
    def add_safety_training(self, training_data):
        """Add safety training record to blockchain"""
        transaction = {
            'type': 'safety_training',
            'timestamp': datetime.now().isoformat(),
            'training_id': f"TRN-{len(self.chain):05d}",
            'data': {
                'personnel_id': training_data.get('personnel_id'),
                'personnel_name': training_data.get('name'),
                'training_type': training_data.get('type', 'General Safety'),
                'certification': training_data.get('certification'),
                'trainer': training_data.get('trainer'),
                'duration_hours': training_data.get('duration', 0),
                'score': training_data.get('score', 0),
                'pass_status': training_data.get('passed', False),
                'expiry_date': training_data.get('expiry'),
                'compliance_standards': training_data.get('standards', [])
            },
            'immutable': True,
            'verified': True
        }
        
        self.pending_transactions.append(transaction)
        print(f"📚 Training record added to ledger: {transaction['training_id']}")
        return transaction['training_id']
    
    def add_equipment_maintenance(self, maintenance_data):
        """Add equipment maintenance record to blockchain"""
        transaction = {
            'type': 'equipment_maintenance',
            'timestamp': datetime.now().isoformat(),
            'maintenance_id': f"MNT-{len(self.chain):05d}",
            'data': {
                'equipment_id': maintenance_data.get('equipment_id'),
                'equipment_type': maintenance_data.get('type'),
                'maintenance_type': maintenance_data.get('maintenance_type', 'Routine'),
                'technician': maintenance_data.get('technician'),
                'work_performed': maintenance_data.get('work', []),
                'parts_replaced': maintenance_data.get('parts', []),
                'downtime_minutes': maintenance_data.get('downtime', 0),
                'cost': maintenance_data.get('cost', 0),
                'next_maintenance_date': maintenance_data.get('next_date'),
                'safety_checks': maintenance_data.get('safety_checks', []),
                'certification': maintenance_data.get('certification')
            },
            'immutable': True,
            'verified': True
        }
        
        self.pending_transactions.append(transaction)
        print(f"🔧 Maintenance record added to ledger: {transaction['maintenance_id']}")
        return transaction['maintenance_id']
    
    def add_inspection_record(self, inspection_data):
        """Add safety inspection record to blockchain"""
        transaction = {
            'type': 'safety_inspection',
            'timestamp': datetime.now().isoformat(),
            'inspection_id': f"INS-{len(self.chain):05d}",
            'data': {
                'inspector': inspection_data.get('inspector'),
                'inspector_certification': inspection_data.get('certification'),
                'area_inspected': inspection_data.get('area'),
                'inspection_type': inspection_data.get('type', 'Routine'),
                'findings': inspection_data.get('findings', []),
                'violations': inspection_data.get('violations', []),
                'corrective_actions': inspection_data.get('actions', []),
                'compliance_score': inspection_data.get('score', 100),
                'follow_up_required': inspection_data.get('follow_up', False),
                'regulatory_standards': inspection_data.get('standards', [])
            },
            'immutable': True,
            'verified': True
        }
        
        self.pending_transactions.append(transaction)
        print(f"🔍Inspection record added to ledger: {transaction['inspection_id']}")