#!/usr/bin/env python3
"""Direct database verification without Flask context"""

import sqlite3
import os

def check_database_direct():
    """Check database directly with SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), 'migration_tool.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return False
    
    print(f"✅ Database file exists at: {db_path}")
    print(f"📁 File size: {os.path.getsize(db_path)} bytes")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {[table[0] for table in tables]}")
        
        # Check record counts
        if ('server',) in tables:
            cursor.execute("SELECT COUNT(*) FROM server")
            servers_count = cursor.fetchone()[0]
            print(f"🖥️  Servers: {servers_count}")
            
            if servers_count > 0:
                cursor.execute("SELECT name, operating_system FROM server LIMIT 3")
                servers = cursor.fetchall()
                print("   Sample servers:")
                for server in servers:
                    print(f"   - {server[0]} ({server[1]})")
        
        if ('database',) in tables:
            cursor.execute("SELECT COUNT(*) FROM database")
            databases_count = cursor.fetchone()[0]
            print(f"🗄️  Databases: {databases_count}")
        
        if ('file_share',) in tables:
            cursor.execute("SELECT COUNT(*) FROM file_share")
            fileshares_count = cursor.fetchone()[0]
            print(f"📁 File Shares: {fileshares_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == '__main__':
    print("Direct Database Check")
    print("=" * 30)
    check_database_direct()
