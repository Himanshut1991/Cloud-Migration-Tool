#!/usr/bin/env python3
"""Test minimal backend exports directly"""

import urllib.request
import urllib.error
import json

def test_export(format_type):
    """Test export endpoint"""
    try:
        url = "http://localhost:5000/api/export"
        data = json.dumps({"format": format_type}).encode('utf-8')
        
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            print(f"✅ {format_type.upper()} export successful: {result.get('filename', 'Unknown')}")
            return True
            
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"❌ {format_type.upper()} export HTTP error: {e.code}")
        print(f"   Error details: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ {format_type.upper()} export error: {e}")
        return False

def main():
    print("Testing minimal backend exports...")
    
    # Test dashboard first
    try:
        with urllib.request.urlopen("http://localhost:5000/api/dashboard", timeout=10) as response:
            data = json.loads(response.read().decode())
            print(f"✅ Backend responding - {data.get('infrastructure_summary', {}).get('servers', 0)} servers")
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return
    
    # Test exports
    formats = ['pdf', 'excel', 'word']
    for fmt in formats:
        print(f"\nTesting {fmt.upper()} export...")
        test_export(fmt)

if __name__ == "__main__":
    main()
