#!/usr/bin/env python3
"""Test database and summary data"""

import os
import sys
sys.path.append('.')

from models_new import init_models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def test_summary_data():
    """Test getting summary data without Word export"""
    try:
        print('🧪 Testing summary data collection...')
        
        app = Flask(__name__)
        basedir = os.path.dirname(os.path.abspath(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "migration_tool.db")}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            models = init_models(db)
            
            # Manually create the summary data logic to test each step
            Server = models.get('Server')
            Database = models.get('Database')
            FileShare = models.get('FileShare')
            
            print(f'Server model: {Server}')
            print(f'Database model: {Database}')
            print(f'FileShare model: {FileShare}')
            
            if Server:
                servers_count = Server.query.count()
                print(f'Servers count: {servers_count}')
                
                # Test getting first server
                if servers_count > 0:
                    first_server = Server.query.first()
                    print(f'First server: {first_server}')
                    print(f'First server vcpu: {getattr(first_server, "vcpu", "NO_VCPU")}')
                    print(f'First server ram: {getattr(first_server, "ram", "NO_RAM")}')
                    print(f'First server disk: {getattr(first_server, "disk_size", "NO_DISK")}')
            
            if Database:
                databases_count = Database.query.count()
                print(f'Databases count: {databases_count}')
                
                if databases_count > 0:
                    first_db = Database.query.first()
                    print(f'First database: {first_db}')
                    print(f'First db size: {getattr(first_db, "size_gb", "NO_SIZE")}')
            
            if FileShare:
                file_shares_count = FileShare.query.count()
                print(f'File shares count: {file_shares_count}')
                
                if file_shares_count > 0:
                    first_fs = FileShare.query.first()
                    print(f'First file share: {first_fs}')
                    print(f'First fs size: {getattr(first_fs, "total_size_gb", "NO_SIZE")}')
            
            print('✅ Summary data test completed')
            
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_summary_data()
