#!/usr/bin/env python3
"""
Minimal working backend to debug issues
"""

import os
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({'message': 'Debug Backend Running', 'status': 'ok'})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "infrastructure_summary": {"servers": 5, "databases": 3, "file_shares": 2},
        "cost_estimation": {"monthly_cost": 1200, "annual_cost": 14400}
    })

@app.route('/api/servers')
def servers():
    return jsonify({
        "servers": [
            {"name": "web-server-01", "cpu_cores": 4, "ram_gb": 16, "storage_gb": 100, "os_type": "Linux"},
            {"name": "db-server-01", "cpu_cores": 8, "ram_gb": 32, "storage_gb": 500, "os_type": "Windows"}
        ],
        "total": 2
    })

@app.route('/api/databases')
def databases():
    return jsonify({
        "databases": [
            {"name": "production-db", "database_type": "MySQL", "size_gb": 50, "version": "8.0"},
            {"name": "analytics-db", "database_type": "PostgreSQL", "size_gb": 100, "version": "13"}
        ],
        "total": 2
    })

@app.route('/api/file-shares')
def file_shares():
    return jsonify({
        "file_shares": [
            {"name": "shared-docs", "share_type": "SMB", "size_gb": 200, "protocol": "SMB3"},
            {"name": "backup-share", "share_type": "NFS", "size_gb": 500, "protocol": "NFSv4"}
        ],
        "total": 2
    })

@app.route('/api/cost-estimation')
def cost_estimation():
    return jsonify({
        "summary": {"monthly_cost": 1200, "annual_cost": 14400, "currency": "USD"},
        "cost_breakdown": {
            "compute": {"monthly_total": 800},
            "storage": {"monthly_total": 300},
            "networking": {"monthly_total": 100}
        }
    })

@app.route('/api/migration-strategy', methods=['GET', 'POST'])
def migration_strategy():
    return jsonify({
        "strategy_overview": {
            "recommended_approach": "Lift and Shift",
            "complexity_level": "Medium", 
            "estimated_duration_weeks": 8,
            "confidence_score": 85
        },
        "phase_breakdown": [
            {"phase": 1, "name": "Planning", "duration_weeks": 2},
            {"phase": 2, "name": "Migration", "duration_weeks": 4},
            {"phase": 3, "name": "Testing", "duration_weeks": 2}
        ]
    })

@app.route('/api/ai-status')
def ai_status():
    return jsonify({
        "ai_service_available": False,
        "service_status": "unavailable",
        "fallback_mode": True,
        "message": "Using static responses for demo"
    })

if __name__ == '__main__':
    print("Starting debug backend on port 5000...")
    print("Available endpoints:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule.rule}")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
