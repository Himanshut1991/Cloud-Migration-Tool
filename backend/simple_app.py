import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
from datetime import datetime, timedelta

# Import AI service (with error handling)
ai_service = None
try:
    from services.ai_recommendations import AIRecommendationService
    ai_service = AIRecommendationService()
    print("AI service initialized successfully")
except Exception as e:
    print(f"Warning: AI service initialization failed: {e}")
    ai_service = None

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

db = SQLAlchemy(app)

# Initialize models
from models_new import init_models
models = init_models(db)
Server = models['Server']
Database = models['Database']
FileShare = models['FileShare']
CloudPreference = models['CloudPreference']
BusinessConstraint = models['BusinessConstraint']
ResourceRate = models['ResourceRate']
MigrationPlan = models['MigrationPlan']

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard data"""
    try:
        # Get actual counts from database
        servers_count = Server.query.count()
        databases_count = Database.query.count()
        file_shares_count = FileShare.query.count()
        
        # Calculate total data size
        total_db_size = db.session.query(db.func.sum(Database.size_gb)).scalar() or 0
        total_fs_size = db.session.query(db.func.sum(FileShare.total_size_gb)).scalar() or 0
        total_data_size = total_db_size + total_fs_size
        
        # Get OS distribution from actual servers
        servers = Server.query.all()
        os_distribution = {}
        for server in servers:
            os_type = server.os_type.split()[0] if server.os_type else 'Unknown'  # Get first word of OS type
            if 'Windows' in os_type:
                os_type = 'Windows'
            elif any(x in os_type.lower() for x in ['linux', 'ubuntu', 'centos', 'rhel', 'debian']):
                os_type = 'Linux'
            elif any(x in os_type.lower() for x in ['unix', 'aix', 'solaris']):
                os_type = 'Unix/AIX'
            else:
                os_type = 'Other'
            os_distribution[os_type] = os_distribution.get(os_type, 0) + 1
        
        server_distribution = [{'os': k, 'count': v} for k, v in os_distribution.items()]
        
        dashboard_data = {
            'servers_count': servers_count,
            'databases_count': databases_count,
            'file_shares_count': file_shares_count,
            'total_data_size_gb': total_data_size,
            'last_updated': datetime.utcnow().isoformat(),
            'metrics': {
                'total_servers': servers_count,
                'total_databases': databases_count,
                'total_file_shares': file_shares_count,
                'estimated_cost': 285000  # This could be calculated based on actual data
            },
            'server_distribution': server_distribution,
            'cost_breakdown': [
                {'category': 'Compute', 'cost': 120000},
                {'category': 'Storage', 'cost': 85000},
                {'category': 'Network', 'cost': 35000},
                {'category': 'Services', 'cost': 45000}
            ]
        }
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Mock servers data
servers_data = [
    {
        'id': 1,
        'server_id': 'SRV-001',
        'os_type': 'Windows Server 2019',
        'vcpu': 4,
        'ram': 16,
        'disk_size': 500,
        'disk_type': 'SSD',
        'uptime_pattern': '24/7',
        'current_hosting': 'On-Premises',
        'technology': 'IIS, .NET Framework',
        'technology_version': '4.8'
    },
    {
        'id': 2,
        'server_id': 'SRV-002',
        'os_type': 'Ubuntu 20.04',
        'vcpu': 8,
        'ram': 32,
        'disk_size': 1000,
        'disk_type': 'SSD',
        'uptime_pattern': 'Business Hours',
        'current_hosting': 'On-Premises',
        'technology': 'Apache, PHP',
        'technology_version': '8.0'
    },
    {
        'id': 3,
        'server_id': 'SRV-003',
        'os_type': 'Windows Server 2022',
        'vcpu': 16,
        'ram': 64,
        'disk_size': 2000,
        'disk_type': 'NVMe',
        'uptime_pattern': '24/7',
        'current_hosting': 'Private Cloud',
        'technology': 'SQL Server, SSRS',
        'technology_version': '2019'
    },
    {
        'id': 4,
        'server_id': 'SRV-004',
        'os_type': 'CentOS 8',
        'vcpu': 12,
        'ram': 48,
        'disk_size': 1500,
        'disk_type': 'SSD',
        'uptime_pattern': '24/7',
        'current_hosting': 'On-Premises',
        'technology': 'Docker, Kubernetes',
        'technology_version': '1.24'
    },
    {
        'id': 5,
        'server_id': 'SRV-005',
        'os_type': 'Red Hat Enterprise Linux 8',
        'vcpu': 6,
        'ram': 24,
        'disk_size': 800,
        'disk_type': 'HDD',
        'uptime_pattern': 'Business Hours',
        'current_hosting': 'On-Premises',
        'technology': 'Oracle WebLogic',
        'technology_version': '14c'
    },
    {
        'id': 6,
        'server_id': 'SRV-006',
        'os_type': 'Windows Server 2016',
        'vcpu': 4,
        'ram': 8,
        'disk_size': 300,
        'disk_type': 'HDD',
        'uptime_pattern': 'Extended Hours',
        'current_hosting': 'On-Premises',
        'technology': 'SharePoint Server',
        'technology_version': '2019'
    },
    {
        'id': 7,
        'server_id': 'SRV-007',
        'os_type': 'Ubuntu 22.04',
        'vcpu': 20,
        'ram': 128,
        'disk_size': 4000,
        'disk_type': 'NVMe',
        'uptime_pattern': '24/7',
        'current_hosting': 'Hybrid Cloud',
        'technology': 'Node.js, MongoDB',
        'technology_version': '18.x'
    },
    {
        'id': 8,
        'server_id': 'SRV-008',
        'os_type': 'AIX 7.2',
        'vcpu': 8,
        'ram': 32,
        'disk_size': 1200,
        'disk_type': 'SSD',
        'uptime_pattern': '24/7',
        'current_hosting': 'On-Premises',
        'technology': 'WebSphere Application Server',
        'technology_version': '9.0'
    },
    {
        'id': 9,
        'server_id': 'SRV-009',
        'os_type': 'SUSE Linux Enterprise 15',
        'vcpu': 10,
        'ram': 40,
        'disk_size': 1800,
        'disk_type': 'SSD',
        'uptime_pattern': '24/7',
        'current_hosting': 'On-Premises',
        'technology': 'SAP HANA',
        'technology_version': '2.0'
    },
    {
        'id': 10,
        'server_id': 'SRV-010',
        'os_type': 'Windows Server 2019 Core',
        'vcpu': 2,
        'ram': 4,
        'disk_size': 120,
        'disk_type': 'SSD',
        'uptime_pattern': 'Business Hours',
        'current_hosting': 'On-Premises',
        'technology': 'File Server, DFS',
        'technology_version': '2019'
    }
]

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Get all servers"""
    try:
        servers = Server.query.all()
        return jsonify([{
            'id': s.id,
            'server_id': s.server_id,
            'os_type': s.os_type,
            'vcpu': s.vcpu,
            'ram': s.ram,
            'disk_size': s.disk_size,
            'disk_type': s.disk_type,
            'uptime_pattern': s.uptime_pattern,
            'current_hosting': s.current_hosting,
            'technology': s.technology,
            'technology_version': s.technology_version,
            'created_at': s.created_at.isoformat()
        } for s in servers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servers', methods=['POST'])
def create_server():
    """Create a new server"""
    try:
        data = request.get_json()
        server = Server(
            server_id=data['server_id'],
            os_type=data['os_type'],
            vcpu=data['vcpu'],
            ram=data['ram'],
            disk_size=data['disk_size'],
            disk_type=data['disk_type'],
            uptime_pattern=data['uptime_pattern'],
            current_hosting=data['current_hosting'],
            technology=data.get('technology', ''),
            technology_version=data.get('technology_version', '')
        )
        db.session.add(server)
        db.session.commit()
        return jsonify({'message': 'Server added successfully', 'id': server.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/servers/<int:server_id>', methods=['PUT'])
def update_server(server_id):
    """Update a server"""
    try:
        server = Server.query.get_or_404(server_id)
        data = request.get_json()
        
        server.server_id = data.get('server_id', server.server_id)
        server.os_type = data.get('os_type', server.os_type)
        server.vcpu = data.get('vcpu', server.vcpu)
        server.ram = data.get('ram', server.ram)
        server.disk_size = data.get('disk_size', server.disk_size)
        server.disk_type = data.get('disk_type', server.disk_type)
        server.uptime_pattern = data.get('uptime_pattern', server.uptime_pattern)
        server.current_hosting = data.get('current_hosting', server.current_hosting)
        server.technology = data.get('technology', server.technology)
        server.technology_version = data.get('technology_version', server.technology_version)
        
        db.session.commit()
        return jsonify({'message': 'Server updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/servers/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    """Delete a server"""
    try:
        server = Server.query.get_or_404(server_id)
        db.session.delete(server)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Mock databases data
databases_data = [
    {
        'id': 1,
        'db_name': 'CustomerDB_Prod',
        'db_type': 'SQL Server',
        'size_gb': 1200,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Enterprise',
        'server_id': 'SRV-003',
        'write_frequency': 'High',
        'downtime_tolerance': 'Low',
        'real_time_sync': True
    },
    {
        'id': 2,
        'db_name': 'InventoryDB',
        'db_type': 'MySQL',
        'size_gb': 350,
        'ha_dr_required': False,
        'backup_frequency': 'Weekly',
        'licensing_model': 'Community',
        'server_id': 'SRV-002',
        'write_frequency': 'Medium',
        'downtime_tolerance': 'Medium',
        'real_time_sync': False
    },
    {
        'id': 3,
        'db_name': 'OracleERP_Main',
        'db_type': 'Oracle Database',
        'size_gb': 2800,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Enterprise',
        'server_id': 'SRV-005',
        'write_frequency': 'High',
        'downtime_tolerance': 'None',
        'real_time_sync': True
    },
    {
        'id': 4,
        'db_name': 'UserProfilesDB',
        'db_type': 'PostgreSQL',
        'size_gb': 180,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Open Source',
        'server_id': 'SRV-004',
        'write_frequency': 'Medium',
        'downtime_tolerance': 'Low',
        'real_time_sync': False
    },
    {
        'id': 5,
        'db_name': 'DocumentStore',
        'db_type': 'MongoDB',
        'size_gb': 950,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Enterprise',
        'server_id': 'SRV-007',
        'write_frequency': 'High',
        'downtime_tolerance': 'Low',
        'real_time_sync': True
    },
    {
        'id': 6,
        'db_name': 'AnalyticsDB',
        'db_type': 'SAP HANA',
        'size_gb': 4500,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Enterprise',
        'server_id': 'SRV-009',
        'write_frequency': 'High',
        'downtime_tolerance': 'None',
        'real_time_sync': True
    },
    {
        'id': 7,
        'db_name': 'CacheDB',
        'db_type': 'Redis',
        'size_gb': 45,
        'ha_dr_required': False,
        'backup_frequency': 'Weekly',
        'licensing_model': 'Open Source',
        'server_id': 'SRV-004',
        'write_frequency': 'High',
        'downtime_tolerance': 'High',
        'real_time_sync': False
    },
    {
        'id': 8,
        'db_name': 'LegacyDB2_Finance',
        'db_type': 'IBM DB2',
        'size_gb': 800,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Enterprise',
        'server_id': 'SRV-008',
        'write_frequency': 'Medium',
        'downtime_tolerance': 'Low',
        'real_time_sync': False
    },
    {
        'id': 9,
        'db_name': 'ConfigDB',
        'db_type': 'SQLite',
        'size_gb': 5,
        'ha_dr_required': False,
        'backup_frequency': 'Monthly',
        'licensing_model': 'Public Domain',
        'server_id': 'SRV-010',
        'write_frequency': 'Low',
        'downtime_tolerance': 'High',
        'real_time_sync': False
    },
    {
        'id': 10,
        'db_name': 'ReportsDB',
        'db_type': 'SQL Server',
        'size_gb': 650,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Standard',
        'server_id': 'SRV-003',
        'write_frequency': 'Low',
        'downtime_tolerance': 'Medium',
        'real_time_sync': False
    },
    {
        'id': 11,
        'db_name': 'SessionStore',
        'db_type': 'Cassandra',
        'size_gb': 320,
        'ha_dr_required': True,
        'backup_frequency': 'Daily',
        'licensing_model': 'Apache License',
        'server_id': 'SRV-004',
        'write_frequency': 'High',
        'downtime_tolerance': 'Medium',
        'real_time_sync': True
    },
    {
        'id': 12,
        'db_name': 'SearchIndex',
        'db_type': 'Elasticsearch',
        'size_gb': 280,
        'ha_dr_required': False,
        'backup_frequency': 'Weekly',
        'licensing_model': 'Elastic License',
        'server_id': 'SRV-007',
        'write_frequency': 'Medium',
        'downtime_tolerance': 'Medium',
        'real_time_sync': False
    }
]

# Database API endpoints
@app.route('/api/databases', methods=['GET'])
def get_databases():
    """Get all databases"""
    try:
        databases = Database.query.all()
        return jsonify([{
            'id': d.id,
            'db_name': d.db_name,
            'db_type': d.db_type,
            'size_gb': d.size_gb,
            'ha_dr_required': d.ha_dr_required,
            'backup_frequency': d.backup_frequency,
            'licensing_model': d.licensing_model,
            'server_id': d.server_id,
            'write_frequency': d.write_frequency,
            'downtime_tolerance': d.downtime_tolerance,
            'real_time_sync': d.real_time_sync,
            'created_at': d.created_at.isoformat()
        } for d in databases])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/databases', methods=['POST'])
def create_database():
    """Create a new database"""
    try:
        data = request.get_json()
        database = Database(
            db_name=data['db_name'],
            db_type=data['db_type'],
            size_gb=data['size_gb'],
            ha_dr_required=data.get('ha_dr_required', False),
            backup_frequency=data['backup_frequency'],
            licensing_model=data['licensing_model'],
            server_id=data['server_id'],
            write_frequency=data['write_frequency'],
            downtime_tolerance=data['downtime_tolerance'],
            real_time_sync=data.get('real_time_sync', False)
        )
        db.session.add(database)
        db.session.commit()
        return jsonify({'message': 'Database added successfully', 'id': database.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/databases/<int:database_id>', methods=['PUT'])
def update_database(database_id):
    """Update a database"""
    try:
        database = Database.query.get_or_404(database_id)
        data = request.get_json()
        
        database.db_name = data.get('db_name', database.db_name)
        database.db_type = data.get('db_type', database.db_type)
        database.size_gb = data.get('size_gb', database.size_gb)
        database.ha_dr_required = data.get('ha_dr_required', database.ha_dr_required)
        database.backup_frequency = data.get('backup_frequency', database.backup_frequency)
        database.licensing_model = data.get('licensing_model', database.licensing_model)
        database.server_id = data.get('server_id', database.server_id)
        database.write_frequency = data.get('write_frequency', database.write_frequency)
        database.downtime_tolerance = data.get('downtime_tolerance', database.downtime_tolerance)
        database.real_time_sync = data.get('real_time_sync', database.real_time_sync)
        
        db.session.commit()
        return jsonify({'message': 'Database updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/databases/<int:database_id>', methods=['DELETE'])
def delete_database(database_id):
    """Delete a database"""
    try:
        database = Database.query.get_or_404(database_id)
        db.session.delete(database)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Mock file shares data
file_shares_data = [
    {
        'id': 1,
        'share_name': 'Corporate_Documents',
        'share_type': 'SMB',
        'size_gb': 2500,
        'file_count': 150000,
        'access_pattern': 'Frequent',
        'backup_required': True,
        'server_id': 'SRV-006',
        'location': '\\\\srv-006\\corporate',
        'security_model': 'NTFS'
    },
    {
        'id': 2,
        'share_name': 'Media_Archive',
        'share_type': 'NFS',
        'size_gb': 8000,
        'file_count': 75000,
        'access_pattern': 'Archive',
        'backup_required': True,
        'server_id': 'SRV-002',
        'location': '/mnt/media_archive',
        'security_model': 'POSIX'
    },
    {
        'id': 3,
        'share_name': 'User_Profiles',
        'share_type': 'CIFS',
        'size_gb': 1200,
        'file_count': 85000,
        'access_pattern': 'Frequent',
        'backup_required': True,
        'server_id': 'SRV-001',
        'location': '\\\\srv-001\\profiles$',
        'security_model': 'NTFS'
    },
    {
        'id': 4,
        'share_name': 'Application_Logs',
        'share_type': 'NFS',
        'size_gb': 450,
        'file_count': 250000,
        'access_pattern': 'Infrequent',
        'backup_required': False,
        'server_id': 'SRV-004',
        'location': '/var/log/applications',
        'security_model': 'POSIX'
    },
    {
        'id': 5,
        'share_name': 'Software_Repository',
        'share_type': 'FTP',
        'size_gb': 3200,
        'file_count': 12000,
        'access_pattern': 'Infrequent',
        'backup_required': True,
        'server_id': 'SRV-005',
        'location': 'ftp://srv-005/software',
        'security_model': 'ACL'
    },
    {
        'id': 6,
        'share_name': 'Database_Backups',
        'share_type': 'SMB',
        'size_gb': 5500,
        'file_count': 8500,
        'access_pattern': 'Archive',
        'backup_required': True,
        'server_id': 'SRV-010',
        'location': '\\\\srv-010\\backups',
        'security_model': 'NTFS'
    },
    {
        'id': 7,
        'share_name': 'Temp_Processing',
        'share_type': 'NFS',
        'size_gb': 800,
        'file_count': 45000,
        'access_pattern': 'Frequent',
        'backup_required': False,
        'server_id': 'SRV-007',
        'location': '/tmp/processing',
        'security_model': 'POSIX'
    }
]

# File Share API endpoints
@app.route('/api/file-shares', methods=['GET'])
def get_file_shares():
    """Get all file shares"""
    try:
        file_shares = FileShare.query.all()
        return jsonify([{
            'id': f.id,
            'share_name': f.share_name,
            'total_size_gb': f.total_size_gb,
            'access_pattern': f.access_pattern,
            'snapshot_required': f.snapshot_required,
            'retention_days': f.retention_days,
            'server_id': f.server_id,
            'write_frequency': f.write_frequency,
            'downtime_tolerance': f.downtime_tolerance,
            'real_time_sync': f.real_time_sync,
            'created_at': f.created_at.isoformat()
        } for f in file_shares])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-shares', methods=['POST'])
def create_file_share():
    """Create a new file share"""
    try:
        data = request.get_json()
        file_share = FileShare(
            share_name=data['share_name'],
            total_size_gb=data['total_size_gb'],
            access_pattern=data['access_pattern'],
            snapshot_required=data.get('snapshot_required', False),
            retention_days=data['retention_days'],
            server_id=data['server_id'],
            write_frequency=data['write_frequency'],
            downtime_tolerance=data['downtime_tolerance'],
            real_time_sync=data.get('real_time_sync', False)
        )
        db.session.add(file_share)
        db.session.commit()
        return jsonify({'message': 'File share added successfully', 'id': file_share.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/file-shares/<int:file_share_id>', methods=['PUT'])
def update_file_share(file_share_id):
    """Update a file share"""
    try:
        file_share = FileShare.query.get_or_404(file_share_id)
        data = request.get_json()
        
        file_share.share_name = data.get('share_name', file_share.share_name)
        file_share.total_size_gb = data.get('total_size_gb', file_share.total_size_gb)
        file_share.access_pattern = data.get('access_pattern', file_share.access_pattern)
        file_share.snapshot_required = data.get('snapshot_required', file_share.snapshot_required)
        file_share.retention_days = data.get('retention_days', file_share.retention_days)
        file_share.server_id = data.get('server_id', file_share.server_id)
        file_share.write_frequency = data.get('write_frequency', file_share.write_frequency)
        file_share.downtime_tolerance = data.get('downtime_tolerance', file_share.downtime_tolerance)
        file_share.real_time_sync = data.get('real_time_sync', file_share.real_time_sync)
        
        db.session.commit()
        return jsonify({'message': 'File share updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/file-shares/<int:file_share_id>', methods=['DELETE'])
def delete_file_share(file_share_id):
    """Delete a file share"""
    try:
        file_share = FileShare.query.get_or_404(file_share_id)
        db.session.delete(file_share)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Cloud Preferences API endpoints
@app.route('/api/cloud-preferences', methods=['GET'])
def get_cloud_preferences():
    """Get cloud preferences (returns the first/only record)"""
    try:
        preference = CloudPreference.query.first()
        if preference:
            return jsonify({
                'id': preference.id,
                'cloud_provider': preference.cloud_provider,
                'region': preference.region,
                'preferred_services': preference.preferred_services,
                'network_config': preference.network_config,
                'created_at': preference.created_at.isoformat(),
                'updated_at': preference.updated_at.isoformat()
            })
        else:
            return jsonify(None)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cloud-preferences', methods=['POST'])
def create_or_update_cloud_preferences():
    """Create or update cloud preferences"""
    try:
        data = request.get_json()
        preference = CloudPreference.query.first()
        
        if preference:
            # Update existing
            preference.cloud_provider = data['cloud_provider']
            preference.region = data['region']
            preference.preferred_services = data['preferred_services']
            preference.network_config = data['network_config']
        else:
            # Create new
            preference = CloudPreference(
                cloud_provider=data['cloud_provider'],
                region=data['region'],
                preferred_services=data['preferred_services'],
                network_config=data['network_config']
            )
            db.session.add(preference)
        
        db.session.commit()
        return jsonify({'message': 'Cloud preferences saved successfully', 'id': preference.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Business Constraints API endpoints
@app.route('/api/business-constraints', methods=['GET'])
def get_business_constraints():
    """Get business constraints (returns the first/only record)"""
    try:
        constraint = BusinessConstraint.query.first()
        if constraint:
            return jsonify({
                'id': constraint.id,
                'migration_window': constraint.migration_window,
                'cutover_date': constraint.cutover_date.isoformat(),
                'downtime_tolerance': constraint.downtime_tolerance,
                'budget_cap': constraint.budget_cap,
                'created_at': constraint.created_at.isoformat(),
                'updated_at': constraint.updated_at.isoformat()
            })
        else:
            return jsonify(None)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/business-constraints', methods=['POST'])
def create_or_update_business_constraints():
    """Create or update business constraints"""
    try:
        data = request.get_json()
        constraint = BusinessConstraint.query.first()
        
        if constraint:
            # Update existing
            constraint.migration_window = data['migration_window']
            constraint.cutover_date = datetime.strptime(data['cutover_date'], '%Y-%m-%d').date()
            constraint.downtime_tolerance = data['downtime_tolerance']
            constraint.budget_cap = data.get('budget_cap')
        else:
            # Create new
            constraint = BusinessConstraint(
                migration_window=data['migration_window'],
                cutover_date=datetime.strptime(data['cutover_date'], '%Y-%m-%d').date(),
                downtime_tolerance=data['downtime_tolerance'],
                budget_cap=data.get('budget_cap')
            )
            db.session.add(constraint)
        
        db.session.commit()
        return jsonify({'message': 'Business constraints saved successfully', 'id': constraint.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Resource Rates API endpoints
@app.route('/api/resource-rates', methods=['GET'])
def get_resource_rates():
    """Get all resource rates"""
    try:
        rates = ResourceRate.query.all()
        return jsonify([{
            'id': r.id,
            'role': r.role,
            'duration_weeks': r.duration_weeks,
            'hours_per_week': r.hours_per_week,
            'rate_per_hour': r.rate_per_hour,
            'created_at': r.created_at.isoformat(),
            'updated_at': r.updated_at.isoformat()
        } for r in rates])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resource-rates', methods=['POST'])
def create_resource_rate():
    """Create a new resource rate"""
    try:
        data = request.get_json()
        rate = ResourceRate(
            role=data['role'],
            duration_weeks=data['duration_weeks'],
            hours_per_week=data['hours_per_week'],
            rate_per_hour=data['rate_per_hour']
        )
        db.session.add(rate)
        db.session.commit()
        return jsonify({'message': 'Resource rate added successfully', 'id': rate.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/resource-rates/<int:rate_id>', methods=['PUT'])
def update_resource_rate(rate_id):
    """Update a resource rate"""
    try:
        rate = ResourceRate.query.get_or_404(rate_id)
        data = request.get_json()
        
        rate.role = data.get('role', rate.role)
        rate.duration_weeks = data.get('duration_weeks', rate.duration_weeks)
        rate.hours_per_week = data.get('hours_per_week', rate.hours_per_week)
        rate.rate_per_hour = data.get('rate_per_hour', rate.rate_per_hour)
        
        db.session.commit()
        return jsonify({'message': 'Resource rate updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/resource-rates/<int:rate_id>', methods=['DELETE'])
def delete_resource_rate(rate_id):
    """Delete a resource rate"""
    try:
        rate = ResourceRate.query.get_or_404(rate_id)
        db.session.delete(rate)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Analysis endpoints
@app.route('/api/cost-estimation', methods=['GET'])
def get_cost_estimation():
    """Get cost estimation analysis"""
    try:
        # Get data from database using SQLAlchemy
        servers_count = Server.query.count()
        databases_count = Database.query.count()
        file_shares_count = FileShare.query.count()
        
        # Get actual server and database data for AI analysis
        servers = Server.query.all()
        databases = Database.query.all()
        file_shares = FileShare.query.all()
        
        # Calculate base costs
        compute_cost = servers_count * 150  # $150 per server per month
        database_cost = databases_count * 200  # $200 per database per month
        storage_cost = file_shares_count * 100  # $100 per file share per month
        
        total_monthly = compute_cost + database_cost + storage_cost
        total_migration = total_monthly * 0.5  # Migration cost is 50% of monthly
        
        # Try to get AI-powered recommendations first
        ai_insights = None
        
        if ai_service:
            try:
                # Check if Bedrock client is available
                if hasattr(ai_service, 'bedrock_client') and ai_service.bedrock_client is not None:
                    print("🤖 AI service detected - generating recommendations...")
                    
                    # Prepare data for AI analysis
                    inventory_data = {
                        'servers': [{'id': s.server_id, 'os': s.os_type, 'environment': s.environment} for s in servers],
                        'databases': [{'name': d.db_name, 'type': d.db_type, 'size_gb': d.size_gb} for d in databases],
                        'file_shares': [{'name': f.share_name, 'size_gb': f.total_size_gb} for f in file_shares],
                        'total_monthly_cost': total_monthly,
                        'cost_breakdown': {
                            'compute': compute_cost,
                            'database': database_cost,
                            'storage': storage_cost
                        }
                    }
                    
                    # Get AI recommendations with better error handling
                    try:
                        print(f"🔍 Calling AI service with {len(inventory_data['servers'])} servers, {len(inventory_data['databases'])} databases, {len(inventory_data['file_shares'])} file shares")
                        ai_recommendations = ai_service.get_cost_optimization_recommendations(inventory_data)
                        
                        if ai_recommendations and isinstance(ai_recommendations, dict):
                            print(f"✅ AI service returned valid response with keys: {list(ai_recommendations.keys())}")
                            
                            # Check if this is actually AI-generated or fallback
                            is_ai_generated = not ai_recommendations.get('fallback_used', True)
                            
                            if is_ai_generated and ai_recommendations.get('recommendations'):
                                print("🎉 Using real AI-generated recommendations!")
                                ai_insights = {
                                    "confidence_level": ai_recommendations.get('confidence_level', 92),
                                    "recommendations": ai_recommendations.get('recommendations', []),
                                    "fallback_used": False,
                                    "ai_available": True,
                                    "ai_status": f"✅ AWS Bedrock Active - Claude 3.5 Sonnet",
                                    "cost_optimization_tips": ai_recommendations.get('cost_optimization_tips', [])
                                }
                            else:
                                print("📋 AI service returned fallback recommendations")
                                # Use the AI service fallback but mark it as such
                                ai_insights = ai_recommendations
                                ai_insights['ai_status'] = "AI service returned fallback - may indicate API limits or model issues"
                        else:
                            print("❌ AI service returned invalid response format")
                            raise ValueError("Invalid AI service response")
                            
                    except Exception as ai_error:
                        print(f"❌ Detailed AI service error: {str(ai_error)}")
                        raise ai_error
                    
                    if ai_recommendations and 'recommendations' in ai_recommendations:
                        ai_insights = {
                            "confidence_level": ai_recommendations.get('confidence_level', 92),
                            "recommendations": ai_recommendations.get('recommendations', []),
                            "fallback_used": False,
                            "ai_available": True,
                            "ai_status": f"✅ AWS Bedrock Active - Model: {getattr(ai_service, 'model_id', 'Unknown')}",
                            "cost_optimization_tips": ai_recommendations.get('cost_optimization_tips', [])
                        }
                        print("✅ AI recommendations generated successfully!")
                    else:
                        print("⚠️ AI service returned empty recommendations")
                        
                else:
                    print("ℹ️ AI service exists but Bedrock client not available")
                    
            except Exception as e:
                print(f"❌ AI service error: {str(e)}")
                # Don't let AI errors crash the endpoint
        
        # Use rule-based fallback if AI is not available or failed
        if ai_insights is None:
            print("📋 Using enhanced rule-based recommendations")
            ai_insights = {
                "confidence_level": 85,
                "recommendations": [
                    f"Based on {servers_count} servers, consider reserved instances for 20-30% cost savings",
                    f"Consolidate {databases_count} databases where possible to reduce licensing costs", 
                    f"Implement automated scaling for {file_shares_count} file shares to optimize storage costs",
                    "Consider spot instances for non-critical workloads",
                    "Use cloud-native services to reduce operational overhead"
                ],
                "fallback_used": True,
                "ai_available": ai_service is not None and hasattr(ai_service, 'bedrock_client') and ai_service.bedrock_client is not None,
                "ai_status": "AWS Bedrock not available - using intelligent rule-based analysis" if not ai_service else f"AI service error - using fallback (Bedrock available: {ai_service.bedrock_client is not None})",
                "cost_optimization_tips": [
                    "Reserved instances can save 20-72% compared to on-demand pricing",
                    "Use S3 storage classes for different access patterns", 
                    "Implement auto-scaling to match demand"
                ]
            }
        
        return jsonify({
            "total_monthly_cost": total_monthly,
            "total_migration_cost": total_migration,
            "cost_breakdown": {
                "compute": compute_cost,
                "storage": storage_cost,
                "database": database_cost
            },
            "resource_details": {
                "servers": servers_count,
                "databases": databases_count,
                "file_shares": file_shares_count
            },
            "ai_insights": ai_insights
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-status', methods=['GET'])
def get_ai_status():
    """Get AI service status"""
    ai_available = False
    status_message = "AI service not initialized"
    provider = "Rule-based fallback system"
    
    if ai_service:
        if hasattr(ai_service, 'bedrock_client') and ai_service.bedrock_client is not None:
            ai_available = True
            status_message = f"AWS Bedrock connected successfully with model: {getattr(ai_service, 'model_id', 'Unknown')}"
            provider = f"AWS Bedrock ({getattr(ai_service, 'region_name', 'Unknown region')})"
        else:
            status_message = "AI service initialized but Bedrock client not available (check AWS credentials and permissions)"
    
    return jsonify({
        "ai_available": ai_available,
        "fallback_active": not ai_available,
        "provider": provider,
        "last_check": datetime.utcnow().isoformat(),
        "status_message": status_message,
        "capabilities": [
            "Cost optimization recommendations",
            "Migration strategy planning", 
            "Timeline estimation",
            "Risk assessment"
        ],
        "setup_required": {
            "aws_credentials": ai_service is None,
            "bedrock_access": ai_service is not None and (not hasattr(ai_service, 'bedrock_client') or ai_service.bedrock_client is None),
            "model_permissions": ai_available
        }
    })

@app.route('/api/migration-strategy', methods=['POST'])
def get_migration_strategy():
    """Get migration strategy analysis"""
    try:
        # Get data from database using SQLAlchemy
        servers_count = Server.query.count()
        databases_count = Database.query.count()
        file_shares_count = FileShare.query.count()
        
        # Calculate timeline based on inventory
        base_weeks = 8
        server_weeks = servers_count * 2
        db_weeks = databases_count * 3
        total_weeks = base_weeks + server_weeks + db_weeks
        
        return jsonify({
            "strategy_overview": {
                "recommended_approach": "Hybrid Migration Strategy",
                "timeline_weeks": total_weeks,
                "confidence_level": 88,
                "complexity_score": min(10, max(1, (servers_count + databases_count) / 2))
            },
            "migration_phases": [
                {
                    "phase": 1,
                    "name": "Assessment & Planning",
                    "duration_weeks": 4,
                    "activities": [
                        f"Assess {servers_count} servers for migration readiness",
                        f"Analyze {databases_count} databases for cloud compatibility",
                        "Create detailed migration roadmap"
                    ]
                },
                {
                    "phase": 2,
                    "name": "Infrastructure Setup",
                    "duration_weeks": 3,
                    "activities": [
                        "Provision cloud infrastructure",
                        "Set up security and networking",
                        "Configure monitoring and backup"
                    ]
                },
                {
                    "phase": 3,
                    "name": "Data Migration",
                    "duration_weeks": max(4, databases_count * 2),
                    "activities": [
                        "Migrate database content",
                        "Validate data integrity",
                        "Set up replication"
                    ]
                },
                {
                    "phase": 4,
                    "name": "Application Migration",
                    "duration_weeks": max(3, servers_count * 1),
                    "activities": [
                        "Migrate applications and services",
                        "Update configurations",
                        "Test functionality"
                    ]
                }
            ],
            "recommendations": [
                {
                    "type": "Strategy",
                    "title": "Lift and Shift Approach",
                    "description": f"Recommended for {servers_count} servers to minimize complexity",
                    "priority": "High"
                },
                {
                    "type": "Optimization",
                    "title": "Database Modernization",
                    "description": f"Consider cloud-native services for {databases_count} databases",
                    "priority": "Medium"
                }
            ],
            "risk_assessment": [
                {
                    "risk": "Data Migration Complexity",
                    "probability": "Medium",
                    "impact": "High",
                    "mitigation": "Implement comprehensive testing and rollback procedures"
                }
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timeline', methods=['POST'])
def get_timeline():
    """Get migration timeline"""
    try:
        request_data = request.get_json() or {}
        custom_start_date = request_data.get('start_date')
        
        # Get data from database using SQLAlchemy
        servers_count = Server.query.count()
        databases_count = Database.query.count() 
        file_shares_count = FileShare.query.count()
        
        # Calculate timeline
        base_weeks = 8
        server_weeks = servers_count * 2
        db_weeks = databases_count * 3
        total_weeks = base_weeks + server_weeks + db_weeks
        
        # Handle custom start date
        if custom_start_date:
            try:
                start_date = datetime.strptime(custom_start_date, '%Y-%m-%d')
            except ValueError:
                start_date = datetime(2024, 3, 1)
        else:
            start_date = datetime(2024, 3, 1)
        
        end_date = start_date + timedelta(weeks=total_weeks)
        
        return jsonify({
            "project_overview": {
                "total_duration_weeks": total_weeks,
                "total_duration_months": round(total_weeks / 4, 1),
                "estimated_start_date": start_date.strftime('%Y-%m-%d'),
                "estimated_end_date": end_date.strftime('%Y-%m-%d'),
                "confidence_level": "90%",
                "complexity_score": min(10, max(1, (servers_count + databases_count + file_shares_count) / 3))
            },
            "phases": [
                {
                    "phase": 1,
                    "title": "Assessment & Planning",
                    "description": f"Assessment of {servers_count} servers, {databases_count} databases, {file_shares_count} file shares",
                    "duration_weeks": 4,
                    "start_week": 1,
                    "end_week": 4,
                    "dependencies": [],
                    "milestones": ["Infrastructure Assessment Complete", "Migration Plan Approved"],
                    "components": ["Server Assessment", "Database Analysis", "Network Planning"],
                    "risks": ["Incomplete inventory", "Resource availability"],
                    "resources_required": ["Cloud Architect", "Database Expert", "Network Engineer"],
                    "status": "pending"
                },
                {
                    "phase": 2,
                    "title": "Environment Setup",
                    "description": "Set up cloud infrastructure and prepare migration tools",
                    "duration_weeks": 3,
                    "start_week": 5,
                    "end_week": 7,
                    "dependencies": ["Phase 1"],
                    "milestones": ["Cloud Environment Ready", "Migration Tools Configured"],
                    "components": ["VPC Setup", "Security Groups", "Database Setup"],
                    "risks": ["Cloud service limitations", "Security compliance"],
                    "resources_required": ["DevOps Engineer", "Security Specialist"],
                    "status": "pending"
                }
            ],
            "critical_path": ["Phase 1", "Phase 2"],
            "resource_allocation": [
                {
                    "role": "Cloud Architect",
                    "weeks_allocated": total_weeks,
                    "overlap_phases": [1, 2],
                    "peak_utilization_week": 2
                }
            ],
            "risk_mitigation": [
                {
                    "risk": "Data corruption during migration",
                    "probability": "Low",
                    "impact": "High",
                    "mitigation_strategy": "Comprehensive backup and testing strategy",
                    "timeline_buffer_weeks": 2
                }
            ],
            "success_criteria": [
                "All servers migrated successfully",
                "Zero data loss during migration",
                "Application performance maintained"
            ],
            "ai_insights": {
                "optimization_suggestions": [
                    f"Timeline optimized for {servers_count} servers and {databases_count} databases",
                    "Consider parallel migrations to reduce timeline"
                ],
                "timeline_risks": [
                    "Database migration complexity varies by size",
                    "Server dependencies may extend timeline"
                ],
                "resource_recommendations": [
                    "Scale team based on inventory size",
                    "Add specialists for complex databases"
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/debug-ai', methods=['GET'])
def debug_ai():
    """Debug AI service for troubleshooting"""
    debug_info = {
        "ai_service_exists": ai_service is not None,
        "bedrock_client_exists": False,
        "model_id": None,
        "test_result": None,
        "error": None
    }
    
    if ai_service:
        debug_info["bedrock_client_exists"] = hasattr(ai_service, 'bedrock_client') and ai_service.bedrock_client is not None
        debug_info["model_id"] = getattr(ai_service, 'model_id', 'Unknown')
        
        if debug_info["bedrock_client_exists"]:
            try:
                # Test with minimal data
                test_data = {
                    'servers': [{'id': 'test', 'os': 'Windows', 'environment': 'Test'}],
                    'databases': [],
                    'file_shares': []
                }
                result = ai_service.get_cost_optimization_recommendations(test_data)
                debug_info["test_result"] = {
                    "success": True,
                    "type": str(type(result)),
                    "has_recommendations": isinstance(result, dict) and bool(result.get('recommendations')),
                    "fallback_used": result.get('fallback_used', True) if isinstance(result, dict) else True
                }
            except Exception as e:
                debug_info["test_result"] = {"success": False, "error": str(e)}
                debug_info["error"] = str(e)
    
    return jsonify(debug_info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting Cloud Migration Tool Backend...")
    print("Dashboard available at: http://127.0.0.1:5000/api/dashboard")
    print("Health check at: http://127.0.0.1:5000/api/health")
    app.run(host='127.0.0.1', port=5000, debug=True)
