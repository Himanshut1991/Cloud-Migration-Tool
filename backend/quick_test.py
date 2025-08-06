#!/usr/bin/env python3
"""Simple backend test using requests"""

import json
import urllib.request
import urllib.parse

def test_backend():
    print("🔍 Testing backend endpoints...")
    
    # Test 1: Dashboard endpoint
    try:
        print("1. Testing dashboard endpoint...")
        req = urllib.request.Request("http://localhost:5000/api/dashboard")
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"   Status: {response.status}")
            data = json.loads(response.read().decode())
            print(f"   ✅ Dashboard OK: {data.get('infrastructure_summary', {}).get('servers', 0)} servers")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Dashboard HTTP error: {e.code} - {e.reason}")
        error_response = e.read().decode()
        print(f"   Error response: {error_response}")
    except Exception as e:
        print(f"   ❌ Dashboard failed: {e}")
        return
    
    # Test 2: Export endpoint
    try:
        print("2. Testing PDF export endpoint...")
        
        # Create POST request
        data = json.dumps({"format": "pdf"}).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:5000/api/export",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            print(f"   Status: {response.status}")
            result = json.loads(response.read().decode())
            print(f"   ✅ PDF export OK: {result.get('filename', 'unknown')}")
            
    except urllib.error.HTTPError as e:
        print(f"   ❌ PDF export HTTP error: {e.code} - {e.reason}")
        error_response = e.read().decode()
        print(f"   Error response: {error_response}")
    except Exception as e:
        print(f"   ❌ PDF export failed: {e}")

if __name__ == "__main__":
    test_backend()
