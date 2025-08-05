#!/usr/bin/env python3
"""Minimal backend for timeline testing"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize models
try:
    from models_new import init_models
    models = init_models(db)
    Server = models['Server']
    Database = models['Database']
    FileShare = models['FileShare']
    print("✓ Models loaded successfully")
except Exception as e:
    print(f"✗ Model loading error: {e}")
    Server = Database = FileShare = None

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/timeline', methods=['POST'])
def generate_timeline():
    """Generate migration timeline based on inventory"""
    try:
        # Get request data for custom start date
        request_data = request.get_json() or {}
        custom_start_date = request_data.get('start_date')
        
        # Calculate start and end dates
        if custom_start_date:
            try:
                start_date = datetime.strptime(custom_start_date, '%Y-%m-%d')
            except ValueError:
                start_date = datetime(2024, 1, 1)  # fallback
        else:
            start_date = datetime(2024, 1, 1)
        
        # Get inventory counts
        servers_count = 0
        databases_count = 0
        file_shares_count = 0
        
        if Server and Database and FileShare:
            with app.app_context():
                servers_count = Server.query.count()
                databases_count = Database.query.count() 
                file_shares_count = FileShare.query.count()
        
        # Calculate dynamic timeline
        base_weeks = 8
        db_weeks = databases_count * 2 if databases_count > 0 else 3
        server_weeks = servers_count * 1 if servers_count > 0 else 2
        total_weeks = base_weeks + db_weeks + server_weeks
        
        # Calculate end date
        end_date = start_date + timedelta(weeks=total_weeks)
        
        timeline = {
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
                    "description": f"Assessment of {servers_count} servers, {databases_count} databases, {file_shares_count} file shares from your inventory",
                    "duration_weeks": 4,
                    "start_week": 1,
                    "end_week": 4,
                    "dependencies": [],
                    "milestones": ["Infrastructure Assessment Complete", "Migration Plan Approved", "Resource Planning Done"],
                    "components": ["Server Discovery", "Database Analysis", "File Share Mapping", "Network Assessment"],
                    "risks": ["Incomplete inventory discovery", "Resource availability constraints"],
                    "resources_required": ["Cloud Architect", "Database Expert", "Network Engineer"],
                    "status": "pending"
                },
                {
                    "phase": 2,
                    "title": "Environment Setup",
                    "description": "Cloud infrastructure setup and configuration",
                    "duration_weeks": 3,
                    "start_week": 5,
                    "end_week": 7,
                    "dependencies": ["Phase 1"],
                    "milestones": ["Cloud Environment Ready", "Security Configured", "Monitoring Setup"],
                    "components": ["VPC Setup", "Security Groups", "Load Balancers", "Monitoring"],
                    "risks": ["Configuration errors", "Security misconfigurations"],
                    "resources_required": ["DevOps Engineer", "Security Specialist", "Cloud Architect"],
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
                },
                {
                    "role": "Database Expert", 
                    "weeks_allocated": db_weeks,
                    "overlap_phases": [1],
                    "peak_utilization_week": max(1, db_weeks // 2)
                }
            ],
            "risk_mitigation": [
                {
                    "risk": "Data corruption during migration",
                    "probability": "Medium",
                    "impact": "High",
                    "mitigation_strategy": "Comprehensive backup and testing strategy",
                    "timeline_buffer_weeks": 2
                },
                {
                    "risk": "Extended downtime during cutover",
                    "probability": "High", 
                    "impact": "High",
                    "mitigation_strategy": "Blue-green deployment and rollback procedures",
                    "timeline_buffer_weeks": 1
                }
            ],
            "success_criteria": [
                f"All {servers_count} servers migrated successfully",
                f"All {databases_count} databases migrated with zero data loss",
                f"All {file_shares_count} file shares accessible",
                "Application performance maintained or improved",
                "Downtime within acceptable business limits"
            ],
            "ai_insights": {
                "optimization_suggestions": [
                    f"Timeline optimized for current inventory size ({servers_count} servers, {databases_count} databases)",
                    "Consider parallel migrations for databases to reduce timeline",
                    "Implement automated testing to catch issues early"
                ],
                "timeline_risks": [
                    "Complex databases may require additional migration time",
                    "Legacy applications might need refactoring",
                    "Network bandwidth may impact file share migration speed"
                ],
                "resource_recommendations": [
                    f"Current inventory size requires {total_weeks} weeks total duration",
                    "Add database specialists if you have more than 5 databases",
                    "Consider 24/7 support team for final cutover weekend"
                ]
            }
        }
        
        return jsonify(timeline)
        
    except Exception as e:
        print(f"Timeline generation error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Timeline Backend Server...")
    print("Health: http://localhost:5000/api/health")
    print("Timeline: http://localhost:5000/api/timeline")
    app.run(debug=True, port=5000)
