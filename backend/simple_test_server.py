#!/usr/bin/env python3
"""Simple test server to verify Flask works"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Test backend is running', 'status': 'ok'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Test server working"})

@app.route('/api/timeline', methods=['POST'])
def timeline():
    return jsonify({
        "project_overview": {
            "total_duration_weeks": 12,
            "total_duration_months": 3,
            "estimated_start_date": "2024-01-01",
            "estimated_end_date": "2024-03-31",
            "confidence_level": "95%",
            "complexity_score": 6.5
        },
        "phases": [
            {
                "phase": 1,
                "title": "Assessment & Planning (From Backend)",
                "description": "Real data from working backend API",
                "duration_weeks": 3,
                "start_week": 1,
                "end_week": 3,
                "dependencies": [],
                "milestones": ["Backend Connected", "API Working"],
                "components": ["Real API Response"],
                "risks": ["None - backend working"],
                "resources_required": ["Backend Developer"],
                "status": "completed"
            }
        ],
        "critical_path": ["Phase 1"],
        "resource_allocation": [
            {
                "role": "Backend Developer",
                "weeks_allocated": 3,
                "overlap_phases": [1],
                "peak_utilization_week": 2
            }
        ],
        "risk_mitigation": [
            {
                "risk": "API connectivity issues",
                "probability": "Low",
                "impact": "Medium", 
                "mitigation_strategy": "Backend is now working correctly",
                "timeline_buffer_weeks": 0
            }
        ],
        "success_criteria": [
            "Backend API responding",
            "Timeline data loading from server",
            "Real-time data generation working"
        ],
        "ai_insights": {
            "optimization_suggestions": [
                "Backend API is now functioning correctly",
                "Timeline will update based on your inventory"
            ],
            "timeline_risks": [
                "No current backend connectivity issues"
            ],
            "resource_recommendations": [
                "Backend server is operational"
            ]
        }
    })

if __name__ == '__main__':
    print("Starting simple test server on port 5000...")
    print("Health check: http://localhost:5000/api/health")
    print("Timeline API: http://localhost:5000/api/timeline")
    app.run(debug=True, port=5000, host='0.0.0.0')
