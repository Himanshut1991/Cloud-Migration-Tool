#!/usr/bin/env python3

import sqlite3

def check_database_tables():
    try:
        conn = sqlite3.connect('migration_tool.db')
        cursor = conn.cursor()
        
        # Check all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📊 All tables in database:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} records")
            
            # Show columns for each table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"    Columns: {[col[1] for col in columns]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_database_tables()
