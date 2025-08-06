#!/usr/bin/env python3
"""
Ultra-simple backend for inventory data - guaranteed to work
"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"])

# Sample data that matches exactly what the frontend expects
SAMPLE_SERVERS = [
    {
        "id": 1,
        "server_id": "WEB-SERVER-01",
        "name": "WEB-SERVER-01",
        "cpu_cores": 4,
        "vcpu": 4,
        "ram_gb": 16,
        "ram": 16,
        "storage_gb": 100,
        "disk_size": 100,
        "os_type": "Windows Server 2019",
        "disk_type": "SSD",
        "uptime_pattern": "24/7",
        "current_hosting": "On-Premises",
        "technology": "IIS, .NET",
        "technology_version": "10.0, 4.8"
    },
    {
        "id": 2,
        "server_id": "DB-SERVER-01",
        "name": "DB-SERVER-01",
        "cpu_cores": 8,
        "vcpu": 8,
        "ram_gb": 32,
        "ram": 32,
        "storage_gb": 500,
        "disk_size": 500,
        "os_type": "Windows Server 2019",
        "disk_type": "SSD",
        "uptime_pattern": "24/7",
        "current_hosting": "On-Premises",
        "technology": "SQL Server",
        "technology_version": "2019"
    },
    {
        "id": 3,
        "server_id": "APP-SERVER-01",
        "name": "APP-SERVER-01",
        "cpu_cores": 6,
        "vcpu": 6,
        "ram_gb": 24,
        "ram": 24,
        "storage_gb": 200,
        "disk_size": 200,
        "os_type": "Linux Ubuntu 20.04",
        "disk_type": "HDD",
        "uptime_pattern": "Business Hours",
        "current_hosting": "On-Premises",
        "technology": "Node.js, Docker",
        "technology_version": "18.x, 24.x"
    }
]

SAMPLE_DATABASES = [
    {
        "id": 1,
        "db_name": "production-db",
        "name": "production-db",
        "database_type": "SQL Server",
        "db_type": "SQL Server",
        "size_gb": 150,
        "version": "2019",
        "ha_dr_required": True,
        "backup_frequency": "Daily",
        "licensing_model": "Commercial",
        "server_id": "DB-SERVER-01",
        "write_frequency": "High",
        "downtime_tolerance": "Low",
        "real_time_sync": True
    },
    {
        "id": 2,
        "db_name": "analytics-db",
        "name": "analytics-db",
        "database_type": "PostgreSQL",
        "db_type": "PostgreSQL",
        "size_gb": 75,
        "version": "13",
        "ha_dr_required": False,
        "backup_frequency": "Weekly",
        "licensing_model": "Open Source",
        "server_id": "APP-SERVER-01",
        "write_frequency": "Medium",
        "downtime_tolerance": "Medium",
        "real_time_sync": False
    },
    {
        "id": 3,
        "db_name": "cache-db",
        "name": "cache-db",
        "database_type": "Redis",
        "db_type": "Redis",
        "size_gb": 25,
        "version": "7.0",
        "ha_dr_required": False,
        "backup_frequency": "Daily",
        "licensing_model": "Open Source",
        "server_id": "WEB-SERVER-01",
        "write_frequency": "High",
        "downtime_tolerance": "High",
        "real_time_sync": False
    }
]

SAMPLE_FILE_SHARES = [
    {
        "id": 1,
        "share_name": "shared-documents",
        "total_size_gb": 500,
        "share_type": "SMB",
        "protocol": "SMB3",
        "access_pattern": "Hot",
        "snapshot_required": True,
        "retention_days": 30,
        "server_id": "WEB-SERVER-01",
        "write_frequency": "High",
        "downtime_tolerance": "Low",
        "real_time_sync": False
    },
    {
        "id": 2,
        "share_name": "backup-storage",
        "total_size_gb": 1000,
        "share_type": "NFS",
        "protocol": "NFSv4",
        "access_pattern": "Cold",
        "snapshot_required": True,
        "retention_days": 365,
        "server_id": "DB-SERVER-01",
        "write_frequency": "Low",
        "downtime_tolerance": "High",
        "real_time_sync": False
    },
    {
        "id": 3,
        "share_name": "temp-files",
        "total_size_gb": 100,
        "share_type": "SMB",
        "protocol": "SMB3",
        "access_pattern": "Warm",
        "snapshot_required": False,
        "retention_days": 7,
        "server_id": "APP-SERVER-01",
        "write_frequency": "Medium",
        "downtime_tolerance": "Medium",
        "real_time_sync": False
    }
]

SAMPLE_RESOURCE_RATES = [
    {"id": 1, "role": "Cloud Architect", "duration_weeks": 12, "hours_per_week": 40, "rate_per_hour": 175.0},
    {"id": 2, "role": "Migration Engineer", "duration_weeks": 8, "hours_per_week": 40, "rate_per_hour": 145.0},
    {"id": 3, "role": "Database Specialist", "duration_weeks": 6, "hours_per_week": 35, "rate_per_hour": 155.0},
    {"id": 4, "role": "DevOps Engineer", "duration_weeks": 10, "hours_per_week": 40, "rate_per_hour": 135.0},
    {"id": 5, "role": "Security Engineer", "duration_weeks": 4, "hours_per_week": 30, "rate_per_hour": 165.0}
]

@app.route('/api/servers', methods=['GET'])
def get_servers():
    print(f"📡 Simple Backend: GET /api/servers - returning {len(SAMPLE_SERVERS)} servers")
    return jsonify({
        "servers": SAMPLE_SERVERS,
        "total": len(SAMPLE_SERVERS),
        "timestamp": "2025-08-06T12:00:00Z"
    })

@app.route('/api/databases', methods=['GET'])
def get_databases():
    print(f"📡 Simple Backend: GET /api/databases - returning {len(SAMPLE_DATABASES)} databases")
    return jsonify({
        "databases": SAMPLE_DATABASES,
        "total": len(SAMPLE_DATABASES),
        "timestamp": "2025-08-06T12:00:00Z"
    })

@app.route('/api/file-shares', methods=['GET'])
def get_file_shares():
    print(f"📡 Simple Backend: GET /api/file-shares - returning {len(SAMPLE_FILE_SHARES)} file shares")
    return jsonify({
        "file_shares": SAMPLE_FILE_SHARES,
        "total": len(SAMPLE_FILE_SHARES),
        "timestamp": "2025-08-06T12:00:00Z"
    })

@app.route('/api/resource-rates', methods=['GET'])
def get_resource_rates():
    print(f"📡 Simple Backend: GET /api/resource-rates - returning {len(SAMPLE_RESOURCE_RATES)} resource rates")
    return jsonify({
        "resource_rates": SAMPLE_RESOURCE_RATES,
        "total": len(SAMPLE_RESOURCE_RATES),
        "timestamp": "2025-08-06T12:00:00Z"
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    print(f"📡 Simple Backend: GET /api/dashboard")
    return jsonify({
        "infrastructure_summary": {
            "servers": len(SAMPLE_SERVERS),
            "databases": len(SAMPLE_DATABASES),
            "file_shares": len(SAMPLE_FILE_SHARES),
            "total_items": len(SAMPLE_SERVERS) + len(SAMPLE_DATABASES) + len(SAMPLE_FILE_SHARES)
        },
        "cost_estimation": {
            "monthly_cost": 2250,
            "annual_cost": 27000,
            "currency": "USD",
            "last_updated": "2025-08-06T12:00:00Z"
        },
        "migration_timeline": {
            "estimated_duration_weeks": 12,
            "phases": 4,
            "complexity": "Medium"
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Simple backend running with sample data',
        'endpoints': ['/servers', '/databases', '/file-shares', '/resource-rates', '/dashboard'],
        'timestamp': '2025-08-06T12:00:00Z'
    })

if __name__ == '__main__':
    print("🚀 Starting SIMPLE backend on port 5000...")
    print("📋 Endpoints available:")
    print("   - GET /api/health")
    print("   - GET /api/servers")
    print("   - GET /api/databases")
    print("   - GET /api/file-shares")
    print("   - GET /api/resource-rates")
    print("   - GET /api/dashboard")
    print("✅ All endpoints return sample data in correct format")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
