#!/usr/bin/env python3

import sqlite3
import json

def check_database_data():
    try:
        conn = sqlite3.connect('migration_tool.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if databases table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='databases'")
        if not cursor.fetchone():
            print("❌ Databases table does not exist")
            return
        
        # Get database data
        cursor.execute('SELECT * FROM databases LIMIT 5')
        rows = cursor.fetchall()
        
        print(f"📊 Found {len(rows)} databases in database:")
        if len(rows) > 0:
            first_db = dict(rows[0])
            print(f"  - Available columns: {list(first_db.keys())}")
            print(f"  - Sample data: {first_db}")
        
        # Format as the API would return
        databases = [dict(row) for row in rows]
        api_response = {'databases': databases}
        
        print("\n🔄 API Response format:")
        print(json.dumps(api_response, indent=2, default=str))
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_database_data()
