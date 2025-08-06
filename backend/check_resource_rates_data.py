#!/usr/bin/env python3

import sqlite3
import json

def check_resource_rates_data():
    try:
        conn = sqlite3.connect('migration_tool.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if resource_rates table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='resource_rates'")
        if not cursor.fetchone():
            print("❌ resource_rates table does not exist")
            return
        
        # Get resource rates data
        cursor.execute('SELECT * FROM resource_rates LIMIT 5')
        rows = cursor.fetchall()
        
        print(f"📊 Found {len(rows)} resource rates in database:")
        if len(rows) > 0:
            first_rate = dict(rows[0])
            print(f"  - Available columns: {list(first_rate.keys())}")
            print(f"  - Sample data: {first_rate}")
        
        # Format as the API would return
        resource_rates = [dict(row) for row in rows]
        api_response = {'resource_rates': resource_rates}
        
        print("\n🔄 API Response format:")
        print(json.dumps(api_response, indent=2, default=str))
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_resource_rates_data()
