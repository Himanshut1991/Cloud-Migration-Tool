#!/usr/bin/env python3

import requests

def test_all_exports():
    """Test all export formats and types"""
    
    formats = ['excel', 'pdf', 'word']
    report_types = ['cost_estimation', 'migration_strategy', 'timeline']
    
    print("Testing all export combinations...")
    
    for format_type in formats:
        print(f"\n=== Testing {format_type.upper()} format ===")
        try:
            response = requests.post('http://localhost:5000/api/export', 
                                   json={
                                       'format': format_type, 
                                       'types': report_types
                                   })
            print(f'Status: {response.status_code}')
            if response.status_code == 200:
                result = response.json()
                print(f'✅ SUCCESS: {result.get("filename")}')
                print(f'   File size: {result.get("file_size")} bytes')
                print(f'   Types: {result.get("types_included")}')
            else:
                print(f'❌ ERROR: {response.text}')
        except Exception as e:
            print(f'❌ Exception: {e}')

    # Test download endpoint
    print(f"\n=== Testing Download ===")
    try:
        response = requests.get('http://localhost:5000/api/download/migration_report_20250808_180520.xlsx')
        print(f'Download status: {response.status_code}')
        if response.status_code == 200:
            print('✅ Download working')
        else:
            print(f'❌ Download failed: {response.text}')
    except Exception as e:
        print(f'❌ Download exception: {e}')

if __name__ == '__main__':
    test_all_exports()
