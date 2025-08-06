#!/usr/bin/env python3
"""
Minimal backend to serve resource rates data
"""
from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'migration_tool.db')
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/api/resource-rates', methods=['GET'])
def get_resource_rates():
    print(f"📡 Minimal Backend: Received request for /api/resource-rates")
    
    conn = get_db_connection()
    if not conn:
        # Return sample data if database is not available
        sample_rates = [
            {"id": 1, "role": "Cloud Architect", "duration_weeks": 12, "hours_per_week": 40, "rate_per_hour": 175.0},
            {"id": 2, "role": "Migration Engineer", "duration_weeks": 8, "hours_per_week": 40, "rate_per_hour": 145.0},
            {"id": 3, "role": "Database Specialist", "duration_weeks": 6, "hours_per_week": 35, "rate_per_hour": 155.0},
            {"id": 4, "role": "DevOps Engineer", "duration_weeks": 10, "hours_per_week": 40, "rate_per_hour": 135.0},
            {"id": 5, "role": "Security Engineer", "duration_weeks": 4, "hours_per_week": 30, "rate_per_hour": 165.0}
        ]
        print(f"📊 Minimal Backend: Returning {len(sample_rates)} sample resource rates")
        return jsonify({
            "resource_rates": sample_rates,
            "total": len(sample_rates),
            "timestamp": "2025-08-06T12:00:00"
        })
    
    try:
        cursor = conn.cursor()
        
        # Get resource rates count
        cursor.execute("SELECT COUNT(*) FROM resource_rates")
        count_result = cursor.fetchone()
        count = count_result[0] if count_result else 0
        
        # Get resource rates data
        cursor.execute("""
            SELECT id, role, duration_weeks, hours_per_week, rate_per_hour, 
                   created_at, updated_at 
            FROM resource_rates 
            ORDER BY role
        """)
        
        resource_rates = []
        for row in cursor.fetchall():
            rate_dict = {
                'id': row['id'],
                'role': row['role'],
                'duration_weeks': row['duration_weeks'],
                'hours_per_week': row['hours_per_week'],
                'rate_per_hour': row['rate_per_hour'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            resource_rates.append(rate_dict)
        
        conn.close()
        print(f"📊 Minimal Backend: Returning {len(resource_rates)} resource rates from database")
        
        return jsonify({
            "resource_rates": resource_rates,
            "total": count,
            "timestamp": "2025-08-06T12:00:00"
        })
        
    except Exception as e:
        print(f"❌ Minimal Backend: Error querying resource rates: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to fetch resource rates'}), 500

@app.route('/api/servers', methods=['GET'])
def get_servers():
    print(f"📡 Minimal Backend: Received request for /api/servers")
    
    conn = get_db_connection()
    if not conn:
        # Return sample data if database is not available
        sample_servers = [
            {"id": 1, "server_id": "web-server-01", "name": "web-server-01", "cpu_cores": 4, "vcpu": 4, "ram_gb": 16, "ram": 16, "storage_gb": 100, "disk_size": 100, "os_type": "Linux", "disk_type": "SSD", "uptime_pattern": "24/7", "current_hosting": "On-Premises", "technology": "Apache,PHP", "technology_version": "2.4,8.1"},
            {"id": 2, "server_id": "db-server-01", "name": "db-server-01", "cpu_cores": 8, "vcpu": 8, "ram_gb": 32, "ram": 32, "storage_gb": 500, "disk_size": 500, "os_type": "Windows", "disk_type": "SSD", "uptime_pattern": "24/7", "current_hosting": "On-Premises", "technology": "SQL Server", "technology_version": "2019"},
            {"id": 3, "server_id": "app-server-01", "name": "app-server-01", "cpu_cores": 6, "vcpu": 6, "ram_gb": 24, "ram": 24, "storage_gb": 200, "disk_size": 200, "os_type": "Linux", "disk_type": "HDD", "uptime_pattern": "Business Hours", "current_hosting": "On-Premises", "technology": "Node.js,Docker", "technology_version": "18,24"}
        ]
        print(f"📊 Minimal Backend: Returning {len(sample_servers)} sample servers")
        return jsonify({
            "servers": sample_servers,
            "total": len(sample_servers),
            "timestamp": "2025-08-06T12:00:00"
        })
    
    try:
        cursor = conn.cursor()
        
        # Get servers count
        cursor.execute("SELECT COUNT(*) FROM servers")
        count_result = cursor.fetchone()
        count = count_result[0] if count_result else 0
        
        # Get servers data
        cursor.execute("SELECT id, server_id, vcpu, ram, disk_size, os_type FROM servers LIMIT 20")
        servers = []
        for row in cursor.fetchall():
            server_dict = {
                'id': row['id'],
                'server_id': row['server_id'],
                'name': row['server_id'],  # Alias for name
                'cpu_cores': row['vcpu'],  # Alias for cpu_cores
                'vcpu': row['vcpu'],
                'ram_gb': row['ram'],  # Alias for ram_gb
                'ram': row['ram'],
                'storage_gb': row['disk_size'],  # Alias for storage_gb
                'disk_size': row['disk_size'],
                'os_type': row['os_type'],
                'disk_type': 'SSD',
                'uptime_pattern': '24/7',
                'current_hosting': 'On-Premises',
                'technology': 'Various',
                'technology_version': '1.0'
            }
            servers.append(server_dict)
        
        conn.close()
        print(f"📊 Minimal Backend: Returning {len(servers)} servers from database")
        
        return jsonify({
            "servers": servers,
            "total": count,
            "timestamp": "2025-08-06T12:00:00"
        })
        
    except Exception as e:
        print(f"❌ Minimal Backend: Error querying servers: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to fetch servers'}), 500

@app.route('/api/databases', methods=['GET'])
def get_databases():
    print(f"📡 Minimal Backend: Received request for /api/databases")
    
    conn = get_db_connection()
    if not conn:
        # Return sample data if database is not available
        sample_databases = [
            {"id": 1, "db_name": "production-db", "name": "production-db", "database_type": "MySQL", "db_type": "MySQL", "size_gb": 50, "version": "8.0", "ha_dr_required": True, "backup_frequency": "Daily", "licensing_model": "Open Source", "server_id": "db-server-01", "write_frequency": "High", "downtime_tolerance": "Low", "real_time_sync": True},
            {"id": 2, "db_name": "analytics-db", "name": "analytics-db", "database_type": "PostgreSQL", "db_type": "PostgreSQL", "size_gb": 100, "version": "13", "ha_dr_required": False, "backup_frequency": "Weekly", "licensing_model": "Open Source", "server_id": "db-server-01", "write_frequency": "Medium", "downtime_tolerance": "Medium", "real_time_sync": False},
            {"id": 3, "db_name": "cache-db", "name": "cache-db", "database_type": "Redis", "db_type": "Redis", "size_gb": 10, "version": "7.0", "ha_dr_required": False, "backup_frequency": "Daily", "licensing_model": "Open Source", "server_id": "app-server-01", "write_frequency": "High", "downtime_tolerance": "High", "real_time_sync": False}
        ]
        print(f"📊 Minimal Backend: Returning {len(sample_databases)} sample databases")
        return jsonify({
            "databases": sample_databases,
            "total": len(sample_databases),
            "timestamp": "2025-08-06T12:00:00"
        })
    
    try:
        cursor = conn.cursor()
        
        # Get databases count
        cursor.execute("SELECT COUNT(*) FROM databases")
        count_result = cursor.fetchone()
        count = count_result[0] if count_result else 0
        
        # Get databases data
        cursor.execute("SELECT id, db_name, db_type, size_gb FROM databases LIMIT 20")
        databases = []
        for row in cursor.fetchall():
            db_dict = {
                'id': row['id'],
                'db_name': row['db_name'],
                'name': row['db_name'],  # Alias for name
                'database_type': row['db_type'],  # Alias for type
                'db_type': row['db_type'],
                'size_gb': row['size_gb'],
                'version': '8.0',  # Default version
                'ha_dr_required': True,
                'backup_frequency': 'Daily',
                'licensing_model': 'Commercial',
                'server_id': f'server-{row["id"]}',
                'write_frequency': 'Medium',
                'downtime_tolerance': 'Low',
                'real_time_sync': False
            }
            databases.append(db_dict)
        
        conn.close()
        print(f"📊 Minimal Backend: Returning {len(databases)} databases from database")
        
        return jsonify({
            "databases": databases,
            "total": count,
            "timestamp": "2025-08-06T12:00:00"
        })
        
    except Exception as e:
        print(f"❌ Minimal Backend: Error querying databases: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to fetch databases'}), 500

@app.route('/api/file-shares', methods=['GET'])
def get_file_shares():
    print(f"📡 Minimal Backend: Received request for /api/file-shares")
    
    conn = get_db_connection()
    if not conn:
        # Return sample data if database is not available
        sample_file_shares = [
            {"id": 1, "share_name": "shared-docs", "share_type": "SMB", "total_size_gb": 200, "protocol": "SMB3", "access_pattern": "Hot", "snapshot_required": True, "retention_days": 30, "server_id": "web-server-01", "write_frequency": "High", "downtime_tolerance": "Low", "real_time_sync": False},
            {"id": 2, "share_name": "backup-share", "share_type": "NFS", "total_size_gb": 500, "protocol": "NFSv4", "access_pattern": "Cold", "snapshot_required": True, "retention_days": 365, "server_id": "db-server-01", "write_frequency": "Low", "downtime_tolerance": "High", "real_time_sync": False},
            {"id": 3, "share_name": "temp-storage", "share_type": "SMB", "total_size_gb": 50, "protocol": "SMB3", "access_pattern": "Warm", "snapshot_required": False, "retention_days": 7, "server_id": "app-server-01", "write_frequency": "Medium", "downtime_tolerance": "Medium", "real_time_sync": False}
        ]
        print(f"📊 Minimal Backend: Returning {len(sample_file_shares)} sample file shares")
        return jsonify({
            "file_shares": sample_file_shares,
            "total": len(sample_file_shares),
            "timestamp": "2025-08-06T12:00:00"
        })
    
    try:
        cursor = conn.cursor()
        
        # Get file shares count
        cursor.execute("SELECT COUNT(*) FROM file_shares") 
        count_result = cursor.fetchone()
        count = count_result[0] if count_result else 0
        
        # Get file shares data
        cursor.execute("SELECT id, share_name, total_size_gb FROM file_shares LIMIT 20")
        file_shares = []
        for row in cursor.fetchall():
            fs_dict = {
                'id': row['id'],
                'share_name': row['share_name'],
                'total_size_gb': row['total_size_gb'],
                'share_type': 'NFS',
                'protocol': 'NFSv4',
                'access_pattern': 'Hot',
                'snapshot_required': True,
                'retention_days': 30,
                'server_id': f'server-{row["id"]}',
                'write_frequency': 'Medium',
                'downtime_tolerance': 'Low',
                'real_time_sync': False
            }
            file_shares.append(fs_dict)
        
        conn.close()
        print(f"📊 Minimal Backend: Returning {len(file_shares)} file shares from database")
        
        return jsonify({
            "file_shares": file_shares,
            "total": count,
            "timestamp": "2025-08-06T12:00:00"
        })
        
    except Exception as e:
        print(f"❌ Minimal Backend: Error querying file_shares: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to fetch file shares'}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    print(f"📡 Minimal Backend: Received request for /api/dashboard")
    
    # Simple dashboard data
    return jsonify({
        "infrastructure_summary": {
            "servers": 3,
            "databases": 3,
            "file_shares": 3,
            "total_items": 9
        },
        "cost_estimation": {
            "monthly_cost": 675,
            "annual_cost": 8100,
            "currency": "USD",
            "last_updated": "2025-08-06T12:00:00"
        },
        "migration_timeline": {
            "estimated_duration_weeks": 8,
            "phases": 4,
            "complexity": "Medium"
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Minimal backend running'})

if __name__ == '__main__':
    print("🚀 Starting minimal backend on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
