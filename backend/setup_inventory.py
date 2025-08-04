#!/usr/bin/env python3
"""Complete inventory setup and server test"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from models_new import init_models
import requests
import time

def setup_database():
    """Setup database with sample data"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migration_tool.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    with app.app_context():
        models = init_models(db)
        Server = models['Server']
        Database = models['Database']
        FileShare = models['FileShare']
        
        # Create tables
        db.create_all()
        
        print("=== Setting up sample inventory data ===")
        
        # Add servers
        servers_data = [
            {
                'server_id': 'WEB-SERVER-01',
                'os_type': 'Windows Server 2019',
                'vcpu': 4,
                'ram': 16,
                'disk_size': 500,
                'disk_type': 'SSD',
                'uptime_pattern': '24/7',
                'current_hosting': 'On-premises',
                'technology': 'IIS, .NET Framework',
                'technology_version': '4.8'
            },
            {
                'server_id': 'DB-SERVER-01',
                'os_type': 'Linux Ubuntu 20.04',
                'vcpu': 8,
                'ram': 32,
                'disk_size': 1000,
                'disk_type': 'SSD',
                'uptime_pattern': '24/7',
                'current_hosting': 'On-premises',
                'technology': 'MySQL, Apache',
                'technology_version': '8.0'
            },
            {
                'server_id': 'APP-SERVER-01',
                'os_type': 'Windows Server 2016',
                'vcpu': 2,
                'ram': 8,
                'disk_size': 250,
                'disk_type': 'HDD',
                'uptime_pattern': 'Business hours',
                'current_hosting': 'On-premises',
                'technology': 'Java, Tomcat',
                'technology_version': '9.0'
            }
        ]
        
        for server_data in servers_data:
            existing = Server.query.filter_by(server_id=server_data['server_id']).first()
            if not existing:
                server = Server(**server_data)
                db.session.add(server)
                print(f"✅ Added server: {server_data['server_id']}")
        
        # Add databases
        databases_data = [
            {
                'db_name': 'ProductionDB',
                'db_type': 'MySQL',
                'size_gb': 500,
                'ha_dr_required': True,
                'backup_frequency': 'Daily',
                'licensing_model': 'Open Source',
                'server_id': 'DB-SERVER-01',
                'write_frequency': 'High',
                'downtime_tolerance': 'Low',
                'real_time_sync': True
            },
            {
                'db_name': 'UserDB',
                'db_type': 'SQL Server',
                'size_gb': 100,
                'ha_dr_required': True,
                'backup_frequency': 'Daily',
                'licensing_model': 'Licensed',
                'server_id': 'WEB-SERVER-01',
                'write_frequency': 'High',
                'downtime_tolerance': 'Low',
                'real_time_sync': True
            }
        ]
        
        for db_data in databases_data:
            existing = Database.query.filter_by(db_name=db_data['db_name']).first()
            if not existing:
                database = Database(**db_data)
                db.session.add(database)
                print(f"✅ Added database: {db_data['db_name']}")
        
        # Add file shares
        file_shares_data = [
            {
                'share_name': 'CompanyFiles',
                'share_type': 'SMB',
                'total_size_gb': 2000,
                'active_users': 150,
                'growth_rate_monthly': 5.0,
                'backup_enabled': True,
                'server_id': 'APP-SERVER-01',
                'access_frequency': 'Regular',
                'access_pattern': 'Hot'
            },
            {
                'share_name': 'ArchiveData',
                'share_type': 'NFS',
                'total_size_gb': 5000,
                'active_users': 20,
                'growth_rate_monthly': 2.0,
                'backup_enabled': True,
                'server_id': 'APP-SERVER-01',
                'access_frequency': 'Rare',
                'access_pattern': 'Cold'
            }
        ]
        
        for share_data in file_shares_data:
            existing = FileShare.query.filter_by(share_name=share_data['share_name']).first()
            if not existing:
                file_share = FileShare(**share_data)
                db.session.add(file_share)
                print(f"✅ Added file share: {share_data['share_name']}")
        
        # Commit changes
        db.session.commit()
        
        print(f"\n=== Final Count ===")
        print(f"Servers: {Server.query.count()}")
        print(f"Databases: {Database.query.count()}")
        print(f"File Shares: {FileShare.query.count()}")
        
        return True

def test_api():
    """Test if API is accessible"""
    try:
        response = requests.get('http://localhost:5000/api/servers', timeout=5)
        if response.status_code == 200:
            servers = response.json()
            print(f"\n✅ API Test: Found {len(servers)} servers via API")
            return True
        else:
            print(f"❌ API Test: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Cloud Migration Tool - Inventory Setup ===")
    
    # Setup database
    setup_success = setup_database()
    
    if setup_success:
        print("\n=== Testing API Connection ===")
        # Wait a moment for server to be ready
        time.sleep(2)
        api_success = test_api()
        
        if api_success:
            print("\n🎉 Setup Complete! Check the frontend inventory tabs.")
        else:
            print("\n⚠️  Database setup complete, but API not accessible.")
            print("   Make sure the backend server is running on port 5000.")
    else:
        print("\n❌ Database setup failed.")
