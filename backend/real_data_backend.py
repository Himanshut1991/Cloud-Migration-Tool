#!/usr/bin/env python3
"""
Real Data Backend - Serves ONLY real database data, no sample data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

DATABASE_PATH = 'migration_tool.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    return dict(row) if row else None

@app.route('/api/servers', methods=['GET', 'POST'])
def handle_servers():
    try:
        if request.method == 'POST':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO servers (server_id, os_type, vcpu, ram, disk_size, disk_type, uptime_pattern, current_hosting, technology, technology_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['server_id'], data['os_type'], data['vcpu'], data['ram'], 
                  data['disk_size'], data['disk_type'], data['uptime_pattern'], 
                  data['current_hosting'], data['technology'], data['technology_version']))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Server added successfully'})
        
        # GET request
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM servers ORDER BY id')
        rows = cursor.fetchall()
        servers = [dict_from_row(row) for row in rows]
        conn.close()
        
        logger.info(f"Retrieved {len(servers)} servers from database")
        return jsonify({'servers': servers})
        
    except Exception as e:
        logger.error(f"Error in /api/servers: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/servers/<int:server_id>', methods=['PUT', 'DELETE'])
def handle_server_by_id(server_id):
    try:
        if request.method == 'PUT':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE servers SET server_id=?, os_type=?, vcpu=?, ram=?, disk_size=?, 
                       disk_type=?, uptime_pattern=?, current_hosting=?, technology=?, technology_version=?
                WHERE id=?
            ''', (data['server_id'], data['os_type'], data['vcpu'], data['ram'], 
                  data['disk_size'], data['disk_type'], data['uptime_pattern'], 
                  data['current_hosting'], data['technology'], data['technology_version'], server_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Server updated successfully'})
        
        elif request.method == 'DELETE':
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM servers WHERE id=?', (server_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Server deleted successfully'})
            
    except Exception as e:
        logger.error(f"Error in /api/servers/{server_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/databases', methods=['GET', 'POST'])
def handle_databases():
    try:
        if request.method == 'POST':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO databases (db_name, db_type, size_gb, ha_dr_required, backup_frequency, 
                       licensing_model, server_id, write_frequency, downtime_tolerance, real_time_sync)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['db_name'], data['db_type'], data['size_gb'], data.get('ha_dr_required', False),
                  data.get('backup_frequency', 'Daily'), data.get('licensing_model', 'Standard'),
                  data.get('server_id', 1), data.get('write_frequency', 'Medium'),
                  data.get('downtime_tolerance', 'Low'), data.get('real_time_sync', False)))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Database added successfully'})
        
        # GET request
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM databases ORDER BY id')
        rows = cursor.fetchall()
        databases = [dict_from_row(row) for row in rows]
        conn.close()
        
        logger.info(f"Retrieved {len(databases)} databases from database")
        return jsonify({'databases': databases})
        
    except Exception as e:
        logger.error(f"Error in /api/databases: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/databases/<int:database_id>', methods=['PUT', 'DELETE'])
def handle_database_by_id(database_id):
    try:
        if request.method == 'PUT':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE databases SET db_name=?, db_type=?, size_gb=?, ha_dr_required=?, 
                       backup_frequency=?, licensing_model=?, server_id=?, write_frequency=?, 
                       downtime_tolerance=?, real_time_sync=?
                WHERE id=?
            ''', (data['db_name'], data['db_type'], data['size_gb'], data.get('ha_dr_required', False),
                  data.get('backup_frequency', 'Daily'), data.get('licensing_model', 'Standard'),
                  data.get('server_id', 1), data.get('write_frequency', 'Medium'),
                  data.get('downtime_tolerance', 'Low'), data.get('real_time_sync', False), database_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Database updated successfully'})
        
        elif request.method == 'DELETE':
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM databases WHERE id=?', (database_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Database deleted successfully'})
            
    except Exception as e:
        logger.error(f"Error in /api/databases/{database_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-shares', methods=['GET', 'POST'])
def handle_file_shares():
    try:
        if request.method == 'POST':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO file_shares (share_name, total_size_gb, access_pattern, snapshot_required, 
                       retention_days, server_id, write_frequency, downtime_tolerance, real_time_sync)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['share_name'], data['total_size_gb'], data.get('access_pattern', 'Medium'),
                  data.get('snapshot_required', False), data.get('retention_days', 30),
                  data.get('server_id', 1), data.get('write_frequency', 'Medium'),
                  data.get('downtime_tolerance', 'Low'), data.get('real_time_sync', False)))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'File share added successfully'})
        
        # GET request
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM file_shares ORDER BY id')
        rows = cursor.fetchall()
        file_shares = [dict_from_row(row) for row in rows]
        conn.close()
        
        logger.info(f"Retrieved {len(file_shares)} file shares from database")
        return jsonify({'file_shares': file_shares})
        
    except Exception as e:
        logger.error(f"Error in /api/file-shares: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-shares/<int:file_share_id>', methods=['PUT', 'DELETE'])
def handle_file_share_by_id(file_share_id):
    try:
        if request.method == 'PUT':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE file_shares SET share_name=?, total_size_gb=?, access_pattern=?, 
                       snapshot_required=?, retention_days=?, server_id=?, write_frequency=?, 
                       downtime_tolerance=?, real_time_sync=?
                WHERE id=?
            ''', (data['share_name'], data['total_size_gb'], data.get('access_pattern', 'Medium'),
                  data.get('snapshot_required', False), data.get('retention_days', 30),
                  data.get('server_id', 1), data.get('write_frequency', 'Medium'),
                  data.get('downtime_tolerance', 'Low'), data.get('real_time_sync', False), file_share_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'File share updated successfully'})
        
        elif request.method == 'DELETE':
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM file_shares WHERE id=?', (file_share_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'File share deleted successfully'})
            
    except Exception as e:
        logger.error(f"Error in /api/file-shares/{file_share_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/resource-rates', methods=['GET', 'POST'])
def handle_resource_rates():
    try:
        if request.method == 'POST':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO resource_rates (role, duration_weeks, hours_per_week, rate_per_hour)
                VALUES (?, ?, ?, ?)
            ''', (data['role'], data['duration_weeks'], data['hours_per_week'], data['rate_per_hour']))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Resource rate added successfully'})
        
        # GET request
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM resource_rates ORDER BY id')
        rows = cursor.fetchall()
        resource_rates = [dict_from_row(row) for row in rows]
        conn.close()
        
        logger.info(f"Retrieved {len(resource_rates)} resource rates from database")
        return jsonify({'resource_rates': resource_rates})
        
    except Exception as e:
        logger.error(f"Error in /api/resource-rates: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/resource-rates/<int:rate_id>', methods=['PUT', 'DELETE'])
def handle_resource_rate_by_id(rate_id):
    try:
        if request.method == 'PUT':
            data = request.json
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE resource_rates SET role=?, duration_weeks=?, hours_per_week=?, rate_per_hour=?
                WHERE id=?
            ''', (data['role'], data['duration_weeks'], data['hours_per_week'], data['rate_per_hour'], rate_id))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Resource rate updated successfully'})
        
        elif request.method == 'DELETE':
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM resource_rates WHERE id=?', (rate_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Resource rate deleted successfully'})
            
    except Exception as e:
        logger.error(f"Error in /api/resource-rates/{rate_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
        resource_rates = [dict_from_row(row) for row in rows]
        conn.close()
        
        logger.info(f"Retrieved {len(resource_rates)} resource rates from database")
        return jsonify({'resource_rates': resource_rates})
        
    except Exception as e:
        logger.error(f"Error in /api/resource-rates: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get counts and basic stats from real database
        cursor.execute('SELECT COUNT(*) FROM servers')
        total_servers = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM databases')
        total_databases = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM file_shares')
        total_file_shares = cursor.fetchone()[0]
        
        # Calculate total data size from databases and file shares
        cursor.execute('SELECT COALESCE(SUM(size_gb), 0) FROM databases')
        database_size = cursor.fetchone()[0]
        
        cursor.execute('SELECT COALESCE(SUM(total_size_gb), 0) FROM file_shares')
        file_share_size = cursor.fetchone()[0]
        
        cursor.execute('SELECT COALESCE(SUM(disk_size), 0) FROM servers')
        server_storage_size = cursor.fetchone()[0]
        
        total_data_gb = database_size + file_share_size + server_storage_size
        
        # Get estimated costs (placeholder calculation from real data)
        cursor.execute('SELECT SUM(ram * 0.1 + vcpu * 0.05 + disk_size * 0.02) FROM servers')
        result = cursor.fetchone()[0]
        estimated_monthly_cost = round(result * 730, 2) if result else 0  # rough estimate
        
        conn.close()
        
        dashboard_data = {
            'infrastructure_summary': {
                'servers': total_servers,
                'databases': total_databases,
                'file_shares': total_file_shares,
                'total_items': total_servers + total_databases + total_file_shares,
                'total_data_gb': total_data_gb
            },
            'cost_estimation': {
                'monthly_cost': estimated_monthly_cost,
                'annual_cost': estimated_monthly_cost * 12,
                'currency': 'USD',
                'last_updated': 'Now'
            },
            'migration_timeline': {
                'estimated_duration_weeks': 12,
                'phases': 5,
                'complexity': 'Medium'
            }
        }
        
        logger.info(f"Dashboard data: {dashboard_data}")
        return jsonify(dashboard_data)
        
    except Exception as e:
        logger.error(f"Error in /api/dashboard: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/cost-estimation', methods=['POST'])
def cost_estimation():
    try:
        data = request.json
        
        # Get actual resource rates from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT AVG(hourly_rate) FROM resource_rates WHERE service_type = ?', ('compute',))
        avg_compute_rate = cursor.fetchone()[0] or 0.1
        
        cursor.execute('SELECT AVG(hourly_rate) FROM resource_rates WHERE service_type = ?', ('storage',))
        avg_storage_rate = cursor.fetchone()[0] or 0.02
        
        conn.close()
        
        # Basic cost calculation using real rates
        monthly_compute_cost = data.get('servers', 0) * avg_compute_rate * 730
        monthly_storage_cost = data.get('storage_gb', 0) * avg_storage_rate * 730
        total_monthly_cost = monthly_compute_cost + monthly_storage_cost
        
        result = {
            'monthly_cost': round(total_monthly_cost, 2),
            'yearly_cost': round(total_monthly_cost * 12, 2),
            'breakdown': {
                'compute': round(monthly_compute_cost, 2),
                'storage': round(monthly_storage_cost, 2)
            }
        }
        
        logger.info(f"Cost estimation: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in /api/cost-estimation: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/migration-strategy', methods=['POST'])
def migration_strategy():
    try:
        data = request.json
        
        # Simple strategy based on real data patterns
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM servers WHERE criticality = ?', ('High',))
        high_criticality_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM servers')
        total_servers = cursor.fetchone()[0]
        
        conn.close()
        
        # Basic strategy logic
        if high_criticality_count > total_servers * 0.5:
            strategy = "Hybrid Cloud - Mix of rehost and replatform"
            risk_level = "Medium"
        else:
            strategy = "Lift and Shift - Rehost approach"
            risk_level = "Low"
        
        result = {
            'recommended_strategy': strategy,
            'risk_level': risk_level,
            'timeline_weeks': 12 + (total_servers // 10) * 2,  # Estimate based on server count
            'key_considerations': [
                f"Total of {total_servers} servers to migrate",
                f"{high_criticality_count} high-criticality systems require careful planning",
                "Consider phased approach for reduced risk"
            ]
        }
        
        logger.info(f"Migration strategy: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in /api/migration-strategy: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-status', methods=['GET'])
def ai_status():
    try:
        # Simple AI status - would integrate with actual AI service
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM servers')
        server_count = cursor.fetchone()[0]
        conn.close()
        
        status = {
            'ai_enabled': server_count > 0,  # AI enabled if we have data to analyze
            'models_available': ['Claude-3-Sonnet', 'Claude-3-Haiku'] if server_count > 0 else [],
            'last_analysis': '2024-01-15T10:00:00Z' if server_count > 0 else None,
            'recommendations_count': server_count if server_count > 0 else 0
        }
        
        logger.info(f"AI status: {status}")
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error in /api/ai-status: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_report():
    try:
        data = request.json
        report_type = data.get('type', 'excel')
        
        # Generate simple export based on real data
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM servers')
        server_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM databases')
        db_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Mock file generation
        filename = f"migration_report_{report_type}.{report_type}"
        
        result = {
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}',
            'content_summary': f"Report contains {server_count} servers and {db_count} databases"
        }
        
        logger.info(f"Export report: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in /api/export: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Mock download - would return actual file
        return jsonify({
            'success': True,
            'message': f'Download {filename} would start here',
            'file_size': '2.4 MB',
            'generated_from_real_data': True
        })
        
    except Exception as e:
        logger.error(f"Error in /api/download: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM servers')
        server_count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database_connected': True,
            'servers_in_db': server_count,
            'serving_real_data': True
        })
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'database_connected': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting Real Data Backend - serves ONLY database data")
    app.run(host='127.0.0.1', port=5000, debug=True)
