#!/usr/bin/env python3

import requests
import json

def test_browser_behavior():
    """Test exactly like the browser does"""
    
    print("=== EXACT BROWSER SIMULATION ===")
    
    # Test Health Check (exactly like browser)
    print("\n1. Health Check (like browser):")
    try:
        response = requests.get(
            'http://localhost:5000/health',
            headers={
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Origin': 'null',
                'Referer': 'file:///'
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Cost Estimation (exactly like browser)  
    print("\n2. Cost Estimation (like browser):")
    try:
        response = requests.post(
            'http://localhost:5000/api/cost-estimation',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Origin': 'null',
                'Referer': 'file:///'
            },
            data=json.dumps({
                'cloud_provider': 'AWS',
                'target_region': 'us-east-1'
            })
        )
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print("Success: Got response")
    except Exception as e:
        print(f"Error: {e}")
        
    # Test Migration Strategy (exactly like browser)
    print("\n3. Migration Strategy (like browser):")
    try:
        response = requests.post(
            'http://localhost:5000/api/migration-strategy', 
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Origin': 'null',
                'Referer': 'file:///'
            },
            data=json.dumps({
                'cloud_provider': 'AWS',
                'target_region': 'us-east-1', 
                'complexity': 'medium'
            })
        )
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print("Success: Got response")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_browser_behavior()
