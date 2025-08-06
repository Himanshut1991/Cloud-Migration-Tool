#!/usr/bin/env python3

import sqlite3
import json

def check_file_share_data():
    try:
        conn = sqlite3.connect('migration_tool.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if file_shares table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_shares'")
        if not cursor.fetchone():
            print("❌ File_shares table does not exist")
            return
        
        # Get file share data
        cursor.execute('SELECT * FROM file_shares LIMIT 5')
        rows = cursor.fetchall()
        
        print(f"📊 Found {len(rows)} file shares in database:")
        if len(rows) > 0:
            first_fs = dict(rows[0])
            print(f"  - Available columns: {list(first_fs.keys())}")
            print(f"  - Sample data: {first_fs}")
        
        # Format as the API would return
        file_shares = [dict(row) for row in rows]
        api_response = {'file_shares': file_shares}
        
        print("\n🔄 API Response format:")
        print(json.dumps(api_response, indent=2, default=str))
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_file_share_data()
