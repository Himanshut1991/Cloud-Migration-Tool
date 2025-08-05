#!/usr/bin/env python3
"""Simple database population script"""

import sqlite3
import os

def create_and_populate_db():
    """Create database and populate with sample data"""
    db_path = os.path.join(os.path.dirname(__file__), 'migration_tool.db')
    
    print(f"Creating/updating database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    
    # Server table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            ip_address VARCHAR(15),
            operating_system VARCHAR(100),
            cpu_cores INTEGER,
            memory_gb INTEGER,
            storage_gb INTEGER,
            environment VARCHAR(50),
            application VARCHAR(200),
            dependencies TEXT,
            current_utilization INTEGER,
            business_criticality VARCHAR(20)
        )
    ''')
    
    # Database table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "database" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            type VARCHAR(50),
            version VARCHAR(20),
            size_gb INTEGER,
            server_name VARCHAR(100),
            port INTEGER,
            environment VARCHAR(50),
            backup_frequency VARCHAR(20),
            business_criticality VARCHAR(20),
            current_connections INTEGER,
            performance_tier VARCHAR(20)
        )
    ''')
    
    # File Share table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_share (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            path VARCHAR(500),
            size_gb INTEGER,
            file_count INTEGER,
            server_name VARCHAR(100),
            share_type VARCHAR(20),
            access_frequency VARCHAR(20),
            backup_status VARCHAR(20),
            business_criticality VARCHAR(20),
            user_count INTEGER
        )
    ''')
    
    # Clear existing data
    print("Clearing existing data...")
    cursor.execute("DELETE FROM server")
    cursor.execute("DELETE FROM 'database'")
    cursor.execute("DELETE FROM file_share")
    
    # Insert sample servers
    print("Inserting sample servers...")
    servers = [
        ('WEB-SERVER-01', '192.168.1.10', 'Windows Server 2019', 4, 16, 500, 'Production', 'IIS Web Server', 'Database Server', 65, 'High'),
        ('DB-SERVER-01', '192.168.1.20', 'Windows Server 2019', 8, 32, 1000, 'Production', 'SQL Server 2019', 'None', 45, 'Critical'),
        ('APP-SERVER-01', '192.168.1.30', 'Linux Ubuntu 20.04', 6, 24, 750, 'Production', 'Node.js Application', 'Database Server', 55, 'High')
    ]
    
    cursor.executemany('''
        INSERT INTO server (name, ip_address, operating_system, cpu_cores, memory_gb, storage_gb, 
                           environment, application, dependencies, current_utilization, business_criticality)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', servers)
    
    # Insert sample databases
    print("Inserting sample databases...")
    databases = [
        ('CustomerDB', 'SQL Server', '2019', 250, 'DB-SERVER-01', 1433, 'Production', 'Daily', 'Critical', 50, 'High'),
        ('InventoryDB', 'MySQL', '8.0', 100, 'APP-SERVER-01', 3306, 'Production', 'Daily', 'High', 25, 'Standard'),
        ('LoggingDB', 'PostgreSQL', '13', 50, 'APP-SERVER-01', 5432, 'Production', 'Weekly', 'Medium', 10, 'Basic')
    ]
    
    cursor.executemany('''
        INSERT INTO "database" (name, type, version, size_gb, server_name, port, environment, 
                              backup_frequency, business_criticality, current_connections, performance_tier)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', databases)
    
    # Insert sample file shares
    print("Inserting sample file shares...")
    file_shares = [
        ('CompanyDocs', '//fileserver/companydocs', 500, 25000, 'FILE-SERVER-01', 'SMB', 'High', 'Enabled', 'High', 150),
        ('UserProfiles', '//fileserver/profiles', 200, 5000, 'FILE-SERVER-01', 'SMB', 'Medium', 'Enabled', 'Medium', 100),
        ('ProjectArchive', '//fileserver/archive', 1000, 50000, 'FILE-SERVER-02', 'NFS', 'Low', 'Enabled', 'Low', 20)
    ]
    
    cursor.executemany('''
        INSERT INTO file_share (name, path, size_gb, file_count, server_name, share_type, 
                               access_frequency, backup_status, business_criticality, user_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', file_shares)
    
    # Commit and close
    conn.commit()
    
    # Verify data
    cursor.execute("SELECT COUNT(*) FROM server")
    servers_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM 'database'")
    databases_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM file_share")
    fileshares_count = cursor.fetchone()[0]
    
    print(f"\n✅ Database populated successfully!")
    print(f"   Servers: {servers_count}")
    print(f"   Databases: {databases_count}")
    print(f"   File Shares: {fileshares_count}")
    
    conn.close()

if __name__ == '__main__':
    create_and_populate_db()
