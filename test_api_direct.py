#!/usr/bin/env python3
"""
Test API endpoints directly to see what data is returned
"""
import requests
import json

API_BASE = 'http://localhost:5000/api'

def test_endpoint(endpoint):
    """Test a specific endpoint"""
    url = f"{API_BASE}{endpoint}"
    try:
        print(f"\n🔍 Testing {endpoint}")
        print(f"📡 URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # Check array lengths
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"   📋 {key}: {len(value)} items")
                        if len(value) > 0:
                            print(f"      🔸 First item keys: {list(value[0].keys()) if isinstance(value[0], dict) else 'Not a dict'}")
                    else:
                        print(f"   📄 {key}: {value}")
            
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"🚨 Connection error: {e}")
        return None

def main():
    """Test all main endpoints"""
    print("🧪 API Endpoint Test")
    print("=" * 50)
    
    endpoints = [
        '/servers',
        '/databases', 
        '/file-shares'
    ]
    
    results = {}
    for endpoint in endpoints:
        results[endpoint] = test_endpoint(endpoint)
    
    print(f"\n📊 SUMMARY")
    print("=" * 30)
    for endpoint, data in results.items():
        if data:
            print(f"✅ {endpoint}: OK")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"   - {key}: {len(value)} items")
        else:
            print(f"❌ {endpoint}: Failed")

if __name__ == "__main__":
    main()
