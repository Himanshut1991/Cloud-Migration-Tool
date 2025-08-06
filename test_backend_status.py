#!/usr/bin/env python3

import requests
import json
import sys

def test_backend():
    base_url = "http://127.0.0.1:5000"
    
    endpoints = [
        "/api/servers",
        "/api/databases", 
        "/api/file-shares",
        "/api/resource-rates"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Testing {endpoint}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    print(f"Records found: {len(data['data'])}")
                    if data['data']:
                        print(f"First record keys: {list(data['data'][0].keys())}")
                else:
                    print(f"Response type: {type(data)}")
                    if isinstance(data, list):
                        print(f"Records found: {len(data)}")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"Connection failed - backend not running")
            return False
        except Exception as e:
            print(f"Error testing {endpoint}: {str(e)}")
    
    return True

if __name__ == "__main__":
    print("Testing backend API endpoints...")
    if test_backend():
        print("Backend is running and responding")
    else:
        print("Backend is not running")
        sys.exit(1)
