import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'migration_tool.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== DATABASE CONTENT CHECK ===")
cursor.execute('SELECT COUNT(*) FROM servers')
servers_count = cursor.fetchone()[0]
print(f'Servers: {servers_count}')

cursor.execute('SELECT COUNT(*) FROM databases')
databases_count = cursor.fetchone()[0]
print(f'Databases: {databases_count}')

cursor.execute('SELECT COUNT(*) FROM file_shares')
file_shares_count = cursor.fetchone()[0]
print(f'File shares: {file_shares_count}')

cursor.execute('SELECT COUNT(*) FROM resource_rates')
resource_rates_count = cursor.fetchone()[0]
print(f'Resource rates: {resource_rates_count}')

print("\n=== SAMPLE DATA ===")
if servers_count > 0:
    cursor.execute('SELECT server_id, os_type, vcpu, ram FROM servers LIMIT 2')
    for row in cursor.fetchall():
        print(f'Server: {row[0]} ({row[1]}) - {row[2]} vCPU, {row[3]}GB RAM')

if databases_count > 0:
    cursor.execute('SELECT db_name, db_type, size_gb FROM databases LIMIT 2')
    for row in cursor.fetchall():
        print(f'Database: {row[0]} ({row[1]}) - {row[2]}GB')

if file_shares_count > 0:
    cursor.execute('SELECT share_name, total_size_gb FROM file_shares LIMIT 2')
    for row in cursor.fetchall():
        print(f'File Share: {row[0]} - {row[1]}GB')

conn.close()
