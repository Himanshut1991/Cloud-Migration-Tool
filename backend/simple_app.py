import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Basic configuration
app.config['SECRET_KEY'] = 'dev-secret-key'

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard data"""
    # Mock data matching the frontend interface
    dashboard_data = {
        'servers_count': 25,
        'databases_count': 15,
        'file_shares_count': 8,
        'total_data_size_gb': 2500,
        'last_updated': datetime.utcnow().isoformat(),
        'metrics': {
            'total_servers': 25,
            'total_databases': 15,
            'total_file_shares': 8,
            'estimated_cost': 125000
        },
        'server_distribution': [
            {'os': 'Windows', 'count': 15},
            {'os': 'Linux', 'count': 8},
            {'os': 'Unix', 'count': 2}
        ],
        'cost_breakdown': [
            {'category': 'Compute', 'cost': 45000},
            {'category': 'Storage', 'cost': 25000},
            {'category': 'Network', 'cost': 15000},
            {'category': 'Services', 'cost': 40000}
        ]
    }
    return jsonify(dashboard_data)

# Mock servers data
servers_data = [
    {
        'id': 1,
        'server_id': 'SRV-001',
        'os_type': 'Windows Server 2019',
        'vcpu': 4,
        'ram': 16,
        'disk_size': 500,
        'disk_type': 'SSD',
        'uptime_pattern': '24/7',
        'current_hosting': 'On-Premises',
        'technology': 'IIS, .NET',
        'technology_version': '4.8'
    },
    {
        'id': 2,
        'server_id': 'SRV-002',
        'os_type': 'Ubuntu 20.04',
        'vcpu': 8,
        'ram': 32,
        'disk_size': 1000,
        'disk_type': 'SSD',
        'uptime_pattern': 'Business Hours',
        'current_hosting': 'On-Premises',
        'technology': 'Apache, PHP',
        'technology_version': '8.0'
    }
]

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Get all servers"""
    return jsonify(servers_data)

@app.route('/api/servers', methods=['POST'])
def create_server():
    """Create a new server"""
    data = request.get_json()
    new_server = {
        'id': len(servers_data) + 1,
        **data
    }
    servers_data.append(new_server)
    return jsonify(new_server), 201

@app.route('/api/servers/<int:server_id>', methods=['PUT'])
def update_server(server_id):
    """Update a server"""
    data = request.get_json()
    for server in servers_data:
        if server['id'] == server_id:
            server.update(data)
            return jsonify(server)
    return jsonify({'error': 'Server not found'}), 404

@app.route('/api/servers/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    """Delete a server"""
    global servers_data
    servers_data = [s for s in servers_data if s['id'] != server_id]
    return '', 204

if __name__ == '__main__':
    print("Starting Cloud Migration Tool Backend...")
    print("Dashboard available at: http://127.0.0.1:5000/api/dashboard")
    print("Health check at: http://127.0.0.1:5000/api/health")
    app.run(host='127.0.0.1', port=5000, debug=True)
