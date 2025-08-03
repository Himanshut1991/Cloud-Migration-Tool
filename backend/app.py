import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest
import pandas as pd
import json
from datetime import datetime, timedelta
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

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
# Import services - these will be updated to work with the models
# from services.cost_calculator import CostCalculator
# from services.migration_advisor import MigrationAdvisor
# from services.timeline_generator import TimelineGenerator
# from services.export_service import ExportService

# AWS Bedrock configuration
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/servers', methods=['GET', 'POST'])
def handle_servers():
    """Handle server inventory operations"""
    if request.method == 'POST':
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
    
    # GET request
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

@app.route('/api/databases', methods=['GET', 'POST'])
def handle_databases():
    """Handle database inventory operations"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            database = Database(
                db_name=data['db_name'],
                db_type=data['db_type'],
                size_gb=data['size_gb'],
                ha_dr_required=data['ha_dr_required'],
                backup_frequency=data['backup_frequency'],
                licensing_model=data['licensing_model'],
                server_id=data.get('server_id'),
                write_frequency=data['write_frequency'],
                downtime_tolerance=data['downtime_tolerance'],
                real_time_sync=data['real_time_sync']
            )
            db.session.add(database)
            db.session.commit()
            return jsonify({'message': 'Database added successfully', 'id': database.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # GET request
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

@app.route('/api/file-shares', methods=['GET', 'POST'])
def handle_file_shares():
    """Handle file share inventory operations"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            file_share = FileShare(
                share_name=data['share_name'],
                total_size_gb=data['total_size_gb'],
                access_pattern=data['access_pattern'],
                snapshot_required=data['snapshot_required'],
                retention_days=data['retention_days'],
                server_id=data.get('server_id'),
                write_frequency=data['write_frequency'],
                downtime_tolerance=data['downtime_tolerance'],
                real_time_sync=data['real_time_sync']
            )
            db.session.add(file_share)
            db.session.commit()
            return jsonify({'message': 'File share added successfully', 'id': file_share.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # GET request
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

@app.route('/api/cloud-preferences', methods=['GET', 'POST'])
def handle_cloud_preferences():
    """Handle cloud target preferences"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            # Update or create cloud preferences
            preference = CloudPreference.query.first()
            if preference:
                preference.cloud_provider = data['cloud_provider']
                preference.region = data['region']
                preference.preferred_services = data['preferred_services']
                preference.network_config = data['network_config']
            else:
                preference = CloudPreference(
                    cloud_provider=data['cloud_provider'],
                    region=data['region'],
                    preferred_services=data['preferred_services'],
                    network_config=data['network_config']
                )
                db.session.add(preference)
            
            db.session.commit()
            return jsonify({'message': 'Cloud preferences saved successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # GET request
    preference = CloudPreference.query.first()
    if preference:
        return jsonify({
            'cloud_provider': preference.cloud_provider,
            'region': preference.region,
            'preferred_services': preference.preferred_services,
            'network_config': preference.network_config,
            'updated_at': preference.updated_at.isoformat()
        })
    return jsonify({})

@app.route('/api/business-constraints', methods=['GET', 'POST'])
def handle_business_constraints():
    """Handle business constraints"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            # Update or create business constraints
            constraint = BusinessConstraint.query.first()
            if constraint:
                constraint.migration_window = data['migration_window']
                constraint.cutover_date = datetime.fromisoformat(data['cutover_date'])
                constraint.downtime_tolerance = data['downtime_tolerance']
                constraint.budget_cap = data.get('budget_cap')
            else:
                constraint = BusinessConstraint(
                    migration_window=data['migration_window'],
                    cutover_date=datetime.fromisoformat(data['cutover_date']),
                    downtime_tolerance=data['downtime_tolerance'],
                    budget_cap=data.get('budget_cap')
                )
                db.session.add(constraint)
            
            db.session.commit()
            return jsonify({'message': 'Business constraints saved successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # GET request
    constraint = BusinessConstraint.query.first()
    if constraint:
        return jsonify({
            'migration_window': constraint.migration_window,
            'cutover_date': constraint.cutover_date.isoformat(),
            'downtime_tolerance': constraint.downtime_tolerance,
            'budget_cap': constraint.budget_cap,
            'updated_at': constraint.updated_at.isoformat()
        })
    return jsonify({})

@app.route('/api/resource-rates', methods=['GET', 'POST'])
def handle_resource_rates():
    """Handle resource billing rates"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            resource_rate = ResourceRate(
                role=data['role'],
                duration_weeks=data['duration_weeks'],
                hours_per_week=data['hours_per_week'],
                rate_per_hour=data['rate_per_hour']
            )
            db.session.add(resource_rate)
            db.session.commit()
            return jsonify({'message': 'Resource rate added successfully', 'id': resource_rate.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # GET request
    rates = ResourceRate.query.all()
    return jsonify([{
        'id': r.id,
        'role': r.role,
        'duration_weeks': r.duration_weeks,
        'hours_per_week': r.hours_per_week,
        'rate_per_hour': r.rate_per_hour,
        'created_at': r.created_at.isoformat()
    } for r in rates])

@app.route('/api/cost-estimation', methods=['POST'])
def calculate_costs():
    """Generate comprehensive cost estimation"""
    try:
        # TODO: Implement after fixing imports
        # calculator = CostCalculator(db, bedrock_client)
        # result = calculator.calculate_total_costs()
        result = {"message": "Cost estimation endpoint - implementation pending"}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/migration-strategy', methods=['POST'])
def generate_migration_strategy():
    """Generate AI-powered migration strategy"""
    try:
        data = request.get_json()
        # TODO: Implement after fixing imports
        # advisor = MigrationAdvisor(db, bedrock_client)
        result = {"message": "Migration strategy endpoint - implementation pending"}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timeline', methods=['POST'])
def generate_timeline():
    """Generate migration timeline"""
    try:
        # TODO: Implement after fixing imports
        # generator = TimelineGenerator(db)
        # timeline = generator.generate_migration_timeline()
        timeline = {"message": "Timeline generation endpoint - implementation pending"}
        return jsonify(timeline)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_data():
    """Export migration plan to various formats"""
    try:
        data = request.get_json()
        export_format = data.get('format', 'excel')  # excel, pdf, word
        
        # TODO: Implement after fixing imports
        # exporter = ExportService(db)
        result = {"message": f"Export endpoint - {export_format} format implementation pending"}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """Get dashboard overview data"""
    try:
        servers_count = Server.query.count()
        databases_count = Database.query.count()
        file_shares_count = FileShare.query.count()
        
        # Calculate total data size
        total_db_size = db.session.query(db.func.sum(Database.size_gb)).scalar() or 0
        total_fs_size = db.session.query(db.func.sum(FileShare.total_size_gb)).scalar() or 0
        
        return jsonify({
            'servers_count': servers_count,
            'databases_count': databases_count,
            'file_shares_count': file_shares_count,
            'total_data_size_gb': total_db_size + total_fs_size,
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
