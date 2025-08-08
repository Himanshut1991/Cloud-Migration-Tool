#!/usr/bin/env python3

import requests
import json

def test_export():
    """Test the export API"""
    try:
        response = requests.post('http://localhost:5000/api/export', 
                               json={'format': 'excel', 'types': ['cost_estimation']})
        print('Export API Response:')
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            result = response.json()
            print(f'Success: {result.get("message")}')
            print(f'Filename: {result.get("filename")}')
            print(f'File size: {result.get("file_size")} bytes')
        else:
            print(f'Error Response: {response.json()}')
    except Exception as e:
        print(f'Error testing export: {e}')

if __name__ == '__main__':
    test_export()
