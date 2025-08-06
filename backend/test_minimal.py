#!/usr/bin/env python3
"""
Minimal Flask app to test basic functionality
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({'message': 'Backend is working!', 'status': 'ok'})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "message": "Minimal backend working"})

@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "servers": 0,
        "databases": 0,
        "file_shares": 0,
        "estimated_cost": 0,
        "migration_timeline": "Not calculated"
    })

@app.route('/api/export', methods=['POST'])
def export():
    return jsonify({
        "status": "success",
        "message": "Export endpoint working",
        "filename": "test_export.pdf"
    })

if __name__ == '__main__':
    print("Starting minimal backend on port 5000...")
    print("Test endpoints:")
    print("  Root: http://localhost:5000/")
    print("  Health: http://localhost:5000/api/health")
    print("  Dashboard: http://localhost:5000/api/dashboard")
    print("  Export: http://localhost:5000/api/export")
    app.run(debug=True, port=5000, host='0.0.0.0')
