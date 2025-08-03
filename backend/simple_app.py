import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
from datetime import datetime, timedelta

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
            'name': d.name,
            'type': d.type,
            'version': d.version,
            'size_gb': d.size_gb,
            'server_id': d.server_id,
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
            name=data['name'],
            type=data['type'],
            version=data['version'],
            size_gb=data['size_gb'],
            server_id=data['server_id']
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
        
        database.name = data.get('name', database.name)
        database.type = data.get('type', database.type)
        database.version = data.get('version', database.version)
        database.size_gb = data.get('size_gb', database.size_gb)
        database.server_id = data.get('server_id', database.server_id)
        
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
            'share_type': f.share_type,
            'total_size_gb': f.total_size_gb,
            'file_count': f.file_count,
            'access_pattern': f.access_pattern,
            'backup_required': f.backup_required,
            'os_type': f.os_type,
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
            share_type=data['share_type'],
            total_size_gb=data['total_size_gb'],
            file_count=data['file_count'],
            access_pattern=data['access_pattern'],
            backup_required=data['backup_required'],
            os_type=data['os_type']
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
        file_share.share_type = data.get('share_type', file_share.share_type)
        file_share.total_size_gb = data.get('total_size_gb', file_share.total_size_gb)
        file_share.file_count = data.get('file_count', file_share.file_count)
        file_share.access_pattern = data.get('access_pattern', file_share.access_pattern)
        file_share.backup_required = data.get('backup_required', file_share.backup_required)
        file_share.os_type = data.get('os_type', file_share.os_type)
        
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting Cloud Migration Tool Backend...")
    print("Dashboard available at: http://127.0.0.1:5000/api/dashboard")
    print("Health check at: http://127.0.0.1:5000/api/health")
    app.run(host='127.0.0.1', port=5000, debug=True)
