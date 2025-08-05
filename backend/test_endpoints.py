#!/usr/bin/env python3
"""Test backend endpoints directly"""

import requests
import json

def test_endpoints():
    """Test all backend endpoints"""
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/health",
        "/api/dashboard-data", 
        "/api/servers",
        "/api/databases",
        "/api/file-shares",
        "/api/cloud-preferences",
        "/api/business-constraints",
        "/api/resource-rates"
    ]
    
    print("Testing Backend Endpoints")
    print("=" * 40)
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"Testing: {url}")
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"  ✅ Success - {len(data)} items")
                elif isinstance(data, dict):
                    print(f"  ✅ Success - {len(data)} fields")
                else:
                    print(f"  ✅ Success - {type(data)}")
            else:
                print(f"  ❌ Error {response.status_code}: {response.text[:100]}")
                
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Connection refused - Backend not running?")
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout - Backend not responding?")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

if __name__ == '__main__':
    test_endpoints()
