#!/usr/bin/env python3
"""
Minimal Backend for Export Testing - No AI dependencies
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import sqlite3
import logging
import traceback
import os
from datetime import datetime

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
    """Convert SQLite row to dictionary"""
    return dict(row) if row else {}

@app.route('/api/export', methods=['POST', 'OPTIONS'])
def export_report():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
        
    try:
        data = request.json
        export_format = data.get('format', 'excel')
        report_types = data.get('types', ['cost_estimation', 'migration_strategy', 'timeline'])
        
        logger.info(f"Export request - Format: {export_format}, Types: {report_types}")
        
        # Get all data from database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get servers
        cursor.execute('SELECT * FROM servers')
        servers_rows = cursor.fetchall()
        servers = [dict_from_row(row) for row in servers_rows]
        
        # Get databases
        cursor.execute('SELECT * FROM databases')
        databases_rows = cursor.fetchall()
        databases = [dict_from_row(row) for row in databases_rows]
        
        # Get file shares
        cursor.execute('SELECT * FROM file_shares')
        file_shares_rows = cursor.fetchall()
        file_shares = [dict_from_row(row) for row in file_shares_rows]
        
        conn.close()
        
        # Prepare mock export data
        export_data = {
            'infrastructure': {
                'servers': servers,
                'databases': databases,
                'file_shares': file_shares
            },
            'export_metadata': {
                'timestamp': datetime.now().isoformat(),
                'format': export_format,
                'types': report_types
            }
        }
        
        # Add mock data for each report type
        if 'cost_estimation' in report_types:
            export_data['cost_estimation'] = {
                'grand_total': {
                    'annual_cloud_cost': 50000,
                    'one_time_migration_cost': 25000,
                    'total_first_year_cost': 75000
                },
                'ai_insights': {
                    'confidence_level': 0.85,
                    'ai_model_used': 'Mock Model',
                    'fallback_used': True,
                    'cost_optimization_tips': [
                        'Consider reserved instances for long-term savings',
                        'Optimize storage tiers based on access patterns'
                    ]
                }
            }
        
        if 'migration_strategy' in report_types:
            export_data['migration_strategy'] = {
                'migration_approach': {
                    'overall_strategy': 'Hybrid Lift-and-Shift with Optimization',
                    'estimated_duration': '16 weeks',
                    'complexity_level': 'Medium'
                },
                'migration_phases': [
                    {
                        'phase': 1,
                        'name': 'Assessment & Planning',
                        'duration': '4 weeks',
                        'components': ['Infrastructure Assessment', 'Application Mapping']
                    }
                ]
            }
        
        if 'timeline' in report_types:
            export_data['timeline'] = {
                'project_overview': {
                    'total_duration_weeks': 16,
                    'estimated_start_date': '2025-09-01',
                    'estimated_end_date': '2025-12-23',
                    'confidence_level': '85%'
                },
                'phases': [
                    {
                        'id': 1,
                        'name': 'Assessment & Planning',
                        'start_week': 1,
                        'end_week': 4,
                        'duration_weeks': 4
                    }
                ]
            }
        
        # Generate mock file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'migration_report_{timestamp}.{export_format}'
        
        # Create exports directory
        exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        filepath = os.path.join(exports_dir, filename)
        
        # Create a simple mock file
        with open(filepath, 'w') as f:
            if export_format == 'excel':
                f.write('Mock Excel content')
            elif export_format == 'pdf':
                f.write('Mock PDF content')
            elif export_format == 'word':
                f.write('Mock Word content')
        
        file_size = os.path.getsize(filepath)
        
        result = {
            'message': f'{export_format.upper()} export completed successfully',
            'format': export_format,
            'filename': filename,
            'filepath': filepath,
            'file_size': file_size,
            'timestamp': datetime.now().isoformat(),
            'types_included': report_types,
            'download_url': f'/api/download/{filename}'
        }
        
        logger.info(f"Export completed: {filename} ({file_size} bytes)")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in /api/export: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
        filepath = os.path.join(exports_dir, filename)
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/octet-stream'
            )
        else:
            return jsonify({'error': 'File not found'}), 404
        
    except Exception as e:
        logger.error(f"Error in /api/download: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Minimal export backend running'
    })

if __name__ == '__main__':
    logger.info("Starting Minimal Export Backend")
    app.run(host='127.0.0.1', port=5000, debug=True)
