#!/usr/bin/env python3
"""Simple test to add one server"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models_new import init_models

# Create app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migration_tool.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    # Initialize models
    models = init_models(db)
    Server = models['Server']
    
    # Create tables
    db.create_all()
    
    # Check existing servers
    existing_count = Server.query.count()
    print(f"Existing servers: {existing_count}")
    
    # Add a test server if none exist
    if existing_count == 0:
        test_server = Server(
            server_id='TEST-001',
            os_type='Windows Server 2019',
            vcpu=4,
            ram=16,
            disk_size=500,
            disk_type='SSD',
            uptime_pattern='24/7',
            current_hosting='On-premises',
            technology='IIS, .NET Framework',
            technology_version='4.8'
        )
        
        db.session.add(test_server)
        db.session.commit()
        print("✅ Added test server: TEST-001")
    
    # Verify
    final_count = Server.query.count()
    print(f"Final server count: {final_count}")
    
    if final_count > 0:
        servers = Server.query.all()
        print("\n=== All Servers ===")
        for server in servers:
            print(f"  {server.server_id}: {server.os_type} ({server.vcpu} vCPU, {server.ram}GB RAM)")
