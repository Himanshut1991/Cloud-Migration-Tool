#!/usr/bin/env python3

import sqlite3

def check_server_columns():
    try:
        conn = sqlite3.connect('migration_tool.db')
        cursor = conn.cursor()
        
        # Get servers table structure
        cursor.execute("PRAGMA table_info(servers)")
        columns = cursor.fetchall()
        
        print("Servers table columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Test the query
        cursor.execute('SELECT COUNT(*) FROM servers')
        count = cursor.fetchone()[0]
        print(f"\nTotal servers: {count}")
        
        # Check if problematic columns exist
        column_names = [col[1] for col in columns]
        if 'memory_gb' in column_names:
            print("memory_gb column exists")
        else:
            print("memory_gb column NOT found")
            
        if 'cpu_cores' in column_names:
            print("cpu_cores column exists")
        else:
            print("cpu_cores column NOT found")
            
        if 'storage_gb' in column_names:
            print("storage_gb column exists")
        else:
            print("storage_gb column NOT found")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_server_columns()
