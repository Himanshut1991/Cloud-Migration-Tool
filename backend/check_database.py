#!/usr/bin/env python3
"""Quick database check script"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models_new import init_models

def check_database():
    """Check database content"""
    print("Checking Database Content")
    print("=" * 40)
    
    with app.app_context():
        try:
            models = init_models(db)
            Server = models['Server']
            Database = models['Database']
            FileShare = models['FileShare']
            CloudPreference = models['CloudPreference']
            BusinessConstraint = models['BusinessConstraint']
            ResourceRate = models['ResourceRate']
            
            # Count records
            servers_count = Server.query.count()
            databases_count = Database.query.count()
            fileshares_count = FileShare.query.count()
            prefs_count = CloudPreference.query.count()
            constraints_count = BusinessConstraint.query.count()
            rates_count = ResourceRate.query.count()
            
            print(f"📊 Inventory:")
            print(f"   Servers: {servers_count}")
            print(f"   Databases: {databases_count}")
            print(f"   File Shares: {fileshares_count}")
            print()
            print(f"⚙️  Configuration:")
            print(f"   Cloud Preferences: {prefs_count}")
            print(f"   Business Constraints: {constraints_count}")
            print(f"   Resource Rates: {rates_count}")
            print()
            
            if servers_count > 0:
                print("✅ Sample data exists!")
                
                # Show sample server names
                servers = Server.query.limit(3).all()
                print(f"📋 Sample Servers:")
                for server in servers:
                    print(f"   - {server.name} ({server.operating_system})")
            else:
                print("❌ No sample data found!")
                print("   Run the 'Populate Database' task first")
                
        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_database()
