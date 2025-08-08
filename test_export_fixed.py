#!/usr/bin/env python3

import requests

def test_export():
    """Test the export API"""
    try:
        response = requests.post('http://localhost:5000/api/export', 
                               json={'format': 'excel', 'types': ['cost_estimation']})
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            print('SUCCESS: Export working')
            result = response.json()
            print(f'Filename: {result.get("filename")}')
            print(f'File size: {result.get("file_size")} bytes')
            print(f'Types included: {result.get("types_included")}')
        else:
            print('ERROR Response:')
            print(response.text)
    except Exception as e:
        print(f'Error testing export: {e}')

if __name__ == '__main__':
    test_export()
