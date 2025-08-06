#!/usr/bin/env python3

import sqlite3
import json

def check_server_data():
    try:
        conn = sqlite3.connect('migration_tool.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if servers table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='servers'")
        if not cursor.fetchone():
            print("❌ Servers table does not exist")
            return
        
        # Get server data
        cursor.execute('SELECT * FROM servers LIMIT 5')
        rows = cursor.fetchall()
        
        print(f"📊 Found {len(rows)} servers in database:")
        for row in rows:
            server = dict(row)
            print(f"  - Available columns: {list(server.keys())}")
            print(f"  - Server data: {server}")
            break  # Just show first one
        
        # Format as the API would return
        servers = [dict(row) for row in rows]
        api_response = {'servers': servers}
        
        print("\n🔄 API Response format:")
        print(json.dumps(api_response, indent=2, default=str))
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_server_data()
