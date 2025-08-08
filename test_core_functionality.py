#!/usr/bin/env python3

import requests

def test_core_functionality():
    """Test that core functionality still works"""
    
    tests = [
        ('GET', 'http://localhost:5000/api/servers', None, 'Server inventory'),
        ('GET', 'http://localhost:5000/api/databases', None, 'Database inventory'),
        ('GET', 'http://localhost:5000/api/file-shares', None, 'File share inventory'),
        ('POST', 'http://localhost:5000/api/cost-estimation', {
            'cloud_provider': 'AWS',
            'target_region': 'us-east-1'
        }, 'Cost estimation'),
        ('POST', 'http://localhost:5000/api/migration-strategy', {
            'cloud_provider': 'AWS', 
            'target_region': 'us-east-1',
            'complexity': 'medium'
        }, 'Migration strategy'),
    ]
    
    print("Testing core functionality...")
    
    for method, url, data, description in tests:
        try:
            if method == 'GET':
                response = requests.get(url)
            else:
                response = requests.post(url, json=data)
                
            print(f"✅ {description}: Status {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {description}: Exception {e}")

if __name__ == '__main__':
    test_core_functionality()
