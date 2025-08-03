from datetime import datetime

# Models will be initialized with db instance in app.py
def init_models(db):
    """Initialize models with database instance"""
    
    class Server(db.Model):
        """Server/VM inventory model"""
        __tablename__ = 'servers'
        
        id = db.Column(db.Integer, primary_key=True)
        server_id = db.Column(db.String(100), unique=True, nullable=False)
        os_type = db.Column(db.String(50), nullable=False)
        vcpu = db.Column(db.Integer, nullable=False)
        ram = db.Column(db.Integer, nullable=False)  # in GB
        disk_size = db.Column(db.Integer, nullable=False)  # in GB
        disk_type = db.Column(db.String(20), nullable=False)  # SSD/HDD
        uptime_pattern = db.Column(db.String(50), nullable=False)
        current_hosting = db.Column(db.String(100), nullable=False)
        technology = db.Column(db.String(500))  # Comma-separated technologies
        technology_version = db.Column(db.String(100))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Relationships
        databases = db.relationship('Database', backref='server', lazy=True)
        file_shares = db.relationship('FileShare', backref='server', lazy=True)

    class Database(db.Model):
        """Database inventory model"""
        __tablename__ = 'databases'
        
        id = db.Column(db.Integer, primary_key=True)
        db_name = db.Column(db.String(100), nullable=False)
        db_type = db.Column(db.String(50), nullable=False)
        size_gb = db.Column(db.Integer, nullable=False)
        ha_dr_required = db.Column(db.Boolean, default=False)
        backup_frequency = db.Column(db.String(50), nullable=False)
        licensing_model = db.Column(db.String(50), nullable=False)
        server_id = db.Column(db.String(100), db.ForeignKey('servers.server_id'))
        write_frequency = db.Column(db.String(20), nullable=False)  # Low/Medium/High
        downtime_tolerance = db.Column(db.String(50), nullable=False)
        real_time_sync = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class FileShare(db.Model):
        """File share/storage inventory model"""
        __tablename__ = 'file_shares'
        
        id = db.Column(db.Integer, primary_key=True)
        share_name = db.Column(db.String(100), nullable=False)
        total_size_gb = db.Column(db.Integer, nullable=False)
        access_pattern = db.Column(db.String(20), nullable=False)  # Cold/Warm/Hot
        snapshot_required = db.Column(db.Boolean, default=False)
        retention_days = db.Column(db.Integer, nullable=False)
        server_id = db.Column(db.String(100), db.ForeignKey('servers.server_id'))
        write_frequency = db.Column(db.String(20), nullable=False)  # Low/Medium/High
        downtime_tolerance = db.Column(db.String(50), nullable=False)
        real_time_sync = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class CloudPreference(db.Model):
        """Cloud target preferences model"""
        __tablename__ = 'cloud_preferences'
        
        id = db.Column(db.Integer, primary_key=True)
        cloud_provider = db.Column(db.String(50), nullable=False)  # AWS/Azure/GCP
        region = db.Column(db.String(50), nullable=False)
        preferred_services = db.Column(db.Text)  # JSON string
        network_config = db.Column(db.String(100), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class BusinessConstraint(db.Model):
        """Business constraints model"""
        __tablename__ = 'business_constraints'
        
        id = db.Column(db.Integer, primary_key=True)
        migration_window = db.Column(db.String(100), nullable=False)
        cutover_date = db.Column(db.Date, nullable=False)
        downtime_tolerance = db.Column(db.String(50), nullable=False)
        budget_cap = db.Column(db.Float)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class ResourceRate(db.Model):
        """Resource billing rates model"""
        __tablename__ = 'resource_rates'
        
        id = db.Column(db.Integer, primary_key=True)
        role = db.Column(db.String(100), nullable=False)
        duration_weeks = db.Column(db.Integer, nullable=False)
        hours_per_week = db.Column(db.Integer, nullable=False)
        rate_per_hour = db.Column(db.Float, nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class MigrationPlan(db.Model):
        """Migration plan results model"""
        __tablename__ = 'migration_plans'
        
        id = db.Column(db.Integer, primary_key=True)
        plan_name = db.Column(db.String(200), nullable=False)
        cloud_service_cost = db.Column(db.Float)
        migration_service_cost = db.Column(db.Float)
        total_timeline_weeks = db.Column(db.Integer)
        recommended_tools = db.Column(db.Text)  # JSON string
        migration_strategy = db.Column(db.Text)  # JSON string
        risk_assessment = db.Column(db.Text)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    return {
        'Server': Server,
        'Database': Database,
        'FileShare': FileShare,
        'CloudPreference': CloudPreference,
        'BusinessConstraint': BusinessConstraint,
        'ResourceRate': ResourceRate,
        'MigrationPlan': MigrationPlan
    }
