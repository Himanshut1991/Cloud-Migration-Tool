#!/usr/bin/env python3
"""Simple test server for timeline API"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Mock timeline data
MOCK_TIMELINE_DATA = {
    "project_overview": {
        "total_duration_weeks": 16,
        "total_phases": 4,
        "critical_path_weeks": 14,
        "buffer_weeks": 2,
        "confidence_level": 85,
        "start_date": "2024-01-01",
        "estimated_end_date": "2024-04-15"
    },
    "phases": [
        {
            "phase": 1,
            "title": "Assessment & Planning",
            "description": "Initial assessment and detailed migration planning",
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
        },
        {
            "phase": 3,
            "title": "Data Migration",
            "description": "Migrate databases and file shares to cloud",
            "duration_weeks": 6,
            "start_week": 8,
            "end_week": 13,
            "dependencies": ["Phase 2"],
            "milestones": ["Database Migration Complete", "File Share Migration Complete"],
            "components": ["Database Replication", "File Transfer", "Data Validation"],
            "risks": ["Data corruption", "Extended downtime"],
            "resources_required": ["Database Administrator", "Storage Specialist"],
            "status": "pending"
        },
        {
            "phase": 4,
            "title": "Server Migration & Cutover",
            "description": "Migrate applications and perform final cutover",
            "duration_weeks": 3,
            "start_week": 14,
            "end_week": 16,
            "dependencies": ["Phase 3"],
            "milestones": ["Application Migration Complete", "Production Cutover"],
            "components": ["Application Deployment", "DNS Cutover", "Monitoring Setup"],
            "risks": ["Application compatibility", "User acceptance"],
            "resources_required": ["Application Developer", "System Administrator"],
            "status": "pending"
        }
    ],
    "critical_path": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
    "resource_allocation": {
        "Cloud Architect": {"weeks": [1, 2, 3, 4], "utilization": 80},
        "Database Expert": {"weeks": [1, 2, 8, 9, 10, 11, 12, 13], "utilization": 90},
        "DevOps Engineer": {"weeks": [5, 6, 7, 14, 15, 16], "utilization": 75}
    },
    "risk_mitigation": {
        "high_risk_items": [
            "Data corruption during migration",
            "Extended downtime during cutover"
        ],
        "mitigation_strategies": [
            "Implement comprehensive backup strategy",
            "Plan for rollback procedures",
            "Conduct thorough testing"
        ]
    },
    "ai_insights": {
        "confidence_level": 85,
        "optimization_suggestions": [
            "Consider parallel database migrations to reduce timeline",
            "Implement blue-green deployment for zero-downtime cutover"
        ],
        "timeline_risks": [
            "Database migration may take longer than estimated",
            "User acceptance testing might reveal compatibility issues"
        ],
        "resource_recommendations": [
            "Add additional database specialist for large databases",
            "Consider 24/7 support during cutover weekend"
        ]
    }
}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "timeline-test-server"})

@app.route('/api/timeline', methods=['POST'])
def timeline():
    return jsonify(MOCK_TIMELINE_DATA)

if __name__ == '__main__':
    print("Starting Timeline Test Server...")
    print("Timeline API available at: http://localhost:5000/api/timeline")
    app.run(debug=True, port=5000)
