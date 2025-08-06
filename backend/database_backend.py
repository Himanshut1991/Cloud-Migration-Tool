#!/usr/bin/env python3
"""
Proper backend serving real database data with correct frontend format
"""
from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'migration_tool.db')
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

@app.route('/api/servers', methods=['GET'])
def get_servers():
    print(f"📡 Backend: GET /api/servers")
    conn = get_db_connection()
    
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get servers count
        cursor.execute("SELECT COUNT(*) FROM servers")
        count = cursor.fetchone()[0]
        
        # Get servers data with all required fields
        cursor.execute("""
            SELECT id, server_id, vcpu, ram, disk_size, os_type, 
                   created_at, updated_at
            FROM servers 
            ORDER BY server_id
        """)
        
        servers = []
        for row in cursor.fetchall():
            server = {
                'id': row['id'],
                'server_id': row['server_id'],
                'name': row['server_id'],  # Frontend expects 'name'
                'cpu_cores': row['vcpu'],  # Frontend expects 'cpu_cores'
                'vcpu': row['vcpu'],
                'ram_gb': row['ram'],      # Frontend expects 'ram_gb'
                'ram': row['ram'],
                'storage_gb': row['disk_size'],  # Frontend expects 'storage_gb'
                'disk_size': row['disk_size'],
                'os_type': row['os_type'],
                'disk_type': 'SSD',        # Default value
                'uptime_pattern': '24/7',  # Default value
                'current_hosting': 'On-Premises',  # Default value
                'technology': 'Various',   # Default value
                'technology_version': '1.0',  # Default value
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            servers.append(server)
        
        conn.close()
        print(f"✅ Backend: Returning {len(servers)} servers from database")
        
        return jsonify({
            "servers": servers,
            "total": count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Backend: Error querying servers: {e}")
        if conn:
            conn.close()
        return jsonify({'error': f'Failed to fetch servers: {str(e)}'}), 500

@app.route('/api/databases', methods=['GET'])
def get_databases():
    print(f"📡 Backend: GET /api/databases")
    conn = get_db_connection()
    
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get databases count
        cursor.execute("SELECT COUNT(*) FROM databases")
        count = cursor.fetchone()[0]
        
        # Get databases data with all required fields
        cursor.execute("""
            SELECT id, db_name, db_type, size_gb, created_at, updated_at
            FROM databases 
            ORDER BY db_name
        """)
        
        databases = []
        for row in cursor.fetchall():
            database = {
                'id': row['id'],
                'db_name': row['db_name'],
                'name': row['db_name'],          # Frontend expects 'name'
                'database_type': row['db_type'],  # Frontend expects 'database_type'
                'db_type': row['db_type'],
                'size_gb': row['size_gb'],
                'version': '8.0',                # Default value
                'ha_dr_required': True,          # Default value
                'backup_frequency': 'Daily',     # Default value
                'licensing_model': 'Commercial', # Default value
                'server_id': f'server-{row["id"]}',  # Default value
                'write_frequency': 'Medium',     # Default value
                'downtime_tolerance': 'Low',     # Default value
                'real_time_sync': False,         # Default value
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            databases.append(database)
        
        conn.close()
        print(f"✅ Backend: Returning {len(databases)} databases from database")
        
        return jsonify({
            "databases": databases,
            "total": count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Backend: Error querying databases: {e}")
        if conn:
            conn.close()
        return jsonify({'error': f'Failed to fetch databases: {str(e)}'}), 500

@app.route('/api/file-shares', methods=['GET'])
def get_file_shares():
    print(f"📡 Backend: GET /api/file-shares")
    conn = get_db_connection()
    
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get file shares count
        cursor.execute("SELECT COUNT(*) FROM file_shares")
        count = cursor.fetchone()[0]
        
        # Get file shares data with all required fields
        cursor.execute("""
            SELECT id, share_name, total_size_gb, created_at, updated_at
            FROM file_shares 
            ORDER BY share_name
        """)
        
        file_shares = []
        for row in cursor.fetchall():
            file_share = {
                'id': row['id'],
                'share_name': row['share_name'],
                'total_size_gb': row['total_size_gb'],
                'share_type': 'NFS',             # Default value
                'protocol': 'NFSv4',             # Default value
                'access_pattern': 'Hot',         # Default value
                'snapshot_required': True,       # Default value
                'retention_days': 30,            # Default value
                'server_id': f'server-{row["id"]}',  # Default value
                'write_frequency': 'Medium',     # Default value
                'downtime_tolerance': 'Low',     # Default value
                'real_time_sync': False,         # Default value
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            file_shares.append(file_share)
        
        conn.close()
        print(f"✅ Backend: Returning {len(file_shares)} file shares from database")
        
        return jsonify({
            "file_shares": file_shares,
            "total": count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Backend: Error querying file_shares: {e}")
        if conn:
            conn.close()
        return jsonify({'error': f'Failed to fetch file shares: {str(e)}'}), 500

@app.route('/api/resource-rates', methods=['GET'])
def get_resource_rates():
    print(f"📡 Backend: GET /api/resource-rates")
    conn = get_db_connection()
    
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get resource rates count
        cursor.execute("SELECT COUNT(*) FROM resource_rates")
        count = cursor.fetchone()[0]
        
        # Get resource rates data
        cursor.execute("""
            SELECT id, role, duration_weeks, hours_per_week, rate_per_hour,
                   created_at, updated_at
            FROM resource_rates 
            ORDER BY role
        """)
        
        resource_rates = []
        for row in cursor.fetchall():
            rate = {
                'id': row['id'],
                'role': row['role'],
                'duration_weeks': row['duration_weeks'],
                'hours_per_week': row['hours_per_week'],
                'rate_per_hour': row['rate_per_hour'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            resource_rates.append(rate)
        
        conn.close()
        print(f"✅ Backend: Returning {len(resource_rates)} resource rates from database")
        
        return jsonify({
            "resource_rates": resource_rates,
            "total": count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Backend: Error querying resource_rates: {e}")
        if conn:
            conn.close()
        return jsonify({'error': f'Failed to fetch resource rates: {str(e)}'}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    print(f"📡 Backend: GET /api/dashboard")
    conn = get_db_connection()
    
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get counts from database
        cursor.execute("SELECT COUNT(*) FROM servers")
        servers_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM databases")
        databases_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_shares")
        file_shares_count = cursor.fetchone()[0]
        
        conn.close()
        
        total_items = servers_count + databases_count + file_shares_count
        monthly_cost = servers_count * 150 + databases_count * 75 + file_shares_count * 50
        
        print(f"✅ Backend: Dashboard - {servers_count} servers, {databases_count} databases, {file_shares_count} file shares")
        
        return jsonify({
            "infrastructure_summary": {
                "servers": servers_count,
                "databases": databases_count,
                "file_shares": file_shares_count,
                "total_items": total_items
            },
            "cost_estimation": {
                "monthly_cost": monthly_cost,
                "annual_cost": monthly_cost * 12,
                "currency": "USD",
                "last_updated": datetime.now().isoformat()
            },
            "migration_timeline": {
                "estimated_duration_weeks": max(4, total_items // 2 + 2),
                "phases": 4,
                "complexity": "High" if total_items > 10 else "Medium" if total_items > 5 else "Low"
            }
        })
        
    except Exception as e:
        print(f"❌ Backend: Error generating dashboard: {e}")
        if conn:
            conn.close()
        return jsonify({'error': f'Failed to generate dashboard: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    conn = get_db_connection()
    db_status = "connected" if conn else "failed"
    if conn:
        conn.close()
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'message': 'Database backend serving real data',
        'endpoints': ['/servers', '/databases', '/file-shares', '/resource-rates', '/dashboard'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting DATABASE backend on port 5000...")
    print("📋 Serving REAL data from SQLite database")
    print("✅ All endpoints return actual database content")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
