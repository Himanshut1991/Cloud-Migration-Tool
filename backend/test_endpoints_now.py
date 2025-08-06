#!/usr/bin/env python3
"""
Quick endpoint test to see what backend is running
"""

import requests

def test_endpoint(url, name):
    try:
        response = requests.get(url, timeout=5)
        print(f"\n{name}:")
        print(f"  Status: {response.status_code}")
        print(f"  Content (first 200 chars): {response.text[:200]}")
        if response.headers.get('content-type'):
            print(f"  Content-Type: {response.headers.get('content-type')}")
    except Exception as e:
        print(f"\n{name}: ERROR - {e}")

if __name__ == "__main__":
    print("Testing backend endpoints...")
    
    # Test basic endpoints
    test_endpoint("http://localhost:5000/", "Root endpoint")
    test_endpoint("http://localhost:5000/api/dashboard", "Dashboard API")
    test_endpoint("http://localhost:5000/api/servers", "Servers API")
    test_endpoint("http://localhost:5000/api/export", "Export API")
    test_endpoint("http://localhost:5000/test", "Test endpoint")
    
    print("\nDone testing endpoints.")
