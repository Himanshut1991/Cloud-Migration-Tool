#!/usr/bin/env python3

import requests
import json

def test_dashboard_api():
    try:
        print("🔄 Testing Dashboard API...")
        response = requests.get('http://localhost:5000/api/dashboard')
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard API Response:")
            print(json.dumps(data, indent=2))
            
            # Check the data structure
            print("\n📊 Data Structure Analysis:")
            print(f"  - Keys in response: {list(data.keys())}")
            
            if 'summary' in data:
                summary = data['summary']
                print(f"  - Keys in summary: {list(summary.keys())}")
                print(f"  - Total servers: {summary.get('total_servers', 'N/A')}")
                print(f"  - Total databases: {summary.get('total_databases', 'N/A')}")
                print(f"  - Total file shares: {summary.get('total_file_shares', 'N/A')}")
            
            if 'infrastructure_summary' in data:
                infra = data['infrastructure_summary']
                print(f"  - Keys in infrastructure_summary: {list(infra.keys())}")
                print(f"  - Servers: {infra.get('servers', 'N/A')}")
                print(f"  - Databases: {infra.get('databases', 'N/A')}")
                print(f"  - File shares: {infra.get('file_shares', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == '__main__':
    test_dashboard_api()
