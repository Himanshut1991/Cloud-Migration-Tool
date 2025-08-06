#!/usr/bin/env python3

import sqlite3
import json
from datetime import datetime

DATABASE_PATH = 'backend/migration_tool.db'

def check_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    print("=== DATABASE STATE CHECK ===")
    print(f"Time: {datetime.now()}")
    print()
    
    # Check servers
    cursor.execute("SELECT COUNT(*) FROM servers")
    server_count = cursor.fetchone()[0]
    print(f"📊 Servers: {server_count} records")
    
    cursor.execute("SELECT server_id, os_type, vcpu, ram FROM servers ORDER BY id DESC LIMIT 3")
    recent_servers = cursor.fetchall()
    print("   Recent servers:")
    for server in recent_servers:
        print(f"   - {server[0]} ({server[1]}, {server[2]} vCPU, {server[3]} GB RAM)")
    
    # Check databases  
    cursor.execute("SELECT COUNT(*) FROM databases")
    db_count = cursor.fetchone()[0]
    print(f"📊 Databases: {db_count} records")
    
    cursor.execute("SELECT db_name, db_type, size_gb FROM databases ORDER BY id DESC LIMIT 3")
    recent_dbs = cursor.fetchall()
    print("   Recent databases:")
    for db in recent_dbs:
        print(f"   - {db[0]} ({db[1]}, {db[2]} GB)")
    
    # Check file shares
    cursor.execute("SELECT COUNT(*) FROM file_shares")
    fs_count = cursor.fetchone()[0]
    print(f"📊 File Shares: {fs_count} records")
    
    cursor.execute("SELECT share_name, total_size_gb, access_pattern FROM file_shares ORDER BY id DESC LIMIT 3")
    recent_fs = cursor.fetchall()
    print("   Recent file shares:")
    for fs in recent_fs:
        print(f"   - {fs[0]} ({fs[1]} GB, {fs[2]})")
    
    # Check resource rates
    cursor.execute("SELECT COUNT(*) FROM resource_rates")
    rr_count = cursor.fetchone()[0]
    print(f"📊 Resource Rates: {rr_count} records")
    
    cursor.execute("SELECT resource_type, hourly_rate, region FROM resource_rates ORDER BY id DESC LIMIT 3")
    recent_rr = cursor.fetchall()
    print("   Recent resource rates:")
    for rr in recent_rr:
        print(f"   - {rr[0]} (${rr[1]}/hr, {rr[2]})")
    
    conn.close()
    print()
    print("=== END DATABASE CHECK ===")

if __name__ == "__main__":
    check_database()
