import sqlite3

def check_all_tables():
    conn = sqlite3.connect('migration_tool.db')
    cursor = conn.cursor()
    
    tables = ['servers', 'databases', 'file_shares', 'resource_rates']
    
    for table in tables:
        print(f"\n=== {table.upper()} TABLE ===")
        try:
            cursor.execute(f'PRAGMA table_info({table})')
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
                
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"Records: {count}")
            
            if count > 0:
                cursor.execute(f'SELECT * FROM {table} LIMIT 1')
                sample = cursor.fetchone()
                print("Sample record:")
                for i, val in enumerate(sample):
                    col_name = columns[i][1]
                    print(f"  {col_name}: {val}")
        except Exception as e:
            print(f"Error checking {table}: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_all_tables()
