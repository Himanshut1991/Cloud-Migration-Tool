#!/usr/bin/env python3
"""Simple server test using urllib (built-in)"""

import urllib.request
import urllib.error
import json

def test_backend():
    """Test backend endpoints using urllib"""
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/health",
        "/api/dashboard-data",
        "/api/servers"
    ]
    
    print("Testing Backend with urllib")
    print("=" * 40)
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"Testing: {url}")
        
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    try:
                        json_data = json.loads(data)
                        if isinstance(json_data, list):
                            print(f"  ✅ Success - {len(json_data)} items")
                        elif isinstance(json_data, dict):
                            print(f"  ✅ Success - Response: {json_data}")
                        else:
                            print(f"  ✅ Success - {type(json_data)}")
                    except json.JSONDecodeError:
                        print(f"  ✅ Success - Raw response: {data[:100]}...")
                else:
                    print(f"  ❌ HTTP {response.status}")
                    
        except urllib.error.URLError as e:
            if "Connection refused" in str(e):
                print(f"  ❌ Backend not running - Connection refused")
            else:
                print(f"  ❌ URL Error: {e}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

if __name__ == '__main__':
    test_backend()
