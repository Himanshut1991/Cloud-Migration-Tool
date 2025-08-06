#!/usr/bin/env python3
"""Test backend endpoints"""

import requests
import json

def test_endpoints():
    base_url = "http://localhost:5000"
    
    # Test dashboard
    print("Testing dashboard endpoint...")
    try:
        response = requests.get(f"{base_url}/api/dashboard")
        print(f"Dashboard status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Dashboard working")
        else:
            print(f"❌ Dashboard error: {response.text}")
    except Exception as e:
        print(f"❌ Dashboard connection error: {e}")
    
    # Test PDF export
    print("\nTesting PDF export...")
    try:
        response = requests.post(
            f"{base_url}/api/export",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"format": "pdf"})
        )
        print(f"PDF export status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ PDF export working: {result.get('filename', 'Unknown file')}")
        else:
            print(f"❌ PDF export error: {response.text}")
    except Exception as e:
        print(f"❌ PDF export connection error: {e}")
    
    # Test Excel export
    print("\nTesting Excel export...")
    try:
        response = requests.post(
            f"{base_url}/api/export",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"format": "excel"})
        )
        print(f"Excel export status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Excel export working: {result.get('filename', 'Unknown file')}")
        else:
            print(f"❌ Excel export error: {response.text}")
    except Exception as e:
        print(f"❌ Excel export connection error: {e}")
    
    # Test Word export
    print("\nTesting Word export...")
    try:
        response = requests.post(
            f"{base_url}/api/export",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"format": "word"})
        )
        print(f"Word export status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Word export working: {result.get('filename', 'Unknown file')}")
        else:
            print(f"❌ Word export error: {response.text}")
    except Exception as e:
        print(f"❌ Word export connection error: {e}")

if __name__ == "__main__":
    test_endpoints()
