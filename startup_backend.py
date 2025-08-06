#!/usr/bin/env python3

import os
import sys
import subprocess
import sqlite3

def check_database():
    """Check if database exists and has data"""
    db_path = 'migration_tool.db'
    if not os.path.exists(db_path):
        print("Database doesn't exist. Creating...")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if tables exist and have data
    tables = ['servers', 'databases', 'file_shares', 'resource_rates']
    for table in tables:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"Table '{table}': {count} records")
            if count == 0:
                conn.close()
                return False
        except sqlite3.OperationalError:
            print(f"Table '{table}' doesn't exist")
            conn.close()
            return False
    
    conn.close()
    return True

def init_database():
    """Initialize database with real data"""
    print("Initializing database...")
    try:
        result = subprocess.run([sys.executable, 'init_real_database.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Database initialized successfully")
            return True
        else:
            print(f"Database initialization failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")
    try:
        subprocess.Popen([sys.executable, 'real_data_backend.py'])
        print("Backend server started")
        return True
    except Exception as e:
        print(f"Error starting backend: {e}")
        return False

if __name__ == "__main__":
    print("=== Backend Startup Script ===")
    
    # Change to backend directory
    os.chdir('backend')
    
    # Check if database exists and has data
    if not check_database():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            sys.exit(1)
    else:
        print("Database is ready")
    
    # Start backend
    if start_backend():
        print("Backend startup completed successfully")
    else:
        print("Failed to start backend")
        sys.exit(1)
