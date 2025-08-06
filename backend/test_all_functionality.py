#!/usr/bin/env python3

import urllib.request
import json
import sys

def test_endpoint(url, name):
    try:
        print(f"Testing {name}: {url}")
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if isinstance(data, list):
                print(f"  ✅ Success - {len(data)} items")
                return True
            elif isinstance(data, dict):
                print(f"  ✅ Success - Object with keys: {list(data.keys())[:5]}")
                return True
    except Exception as e:
        print(f"  ❌ Failed - {str(e)}")
        return False

def main():
    print("Testing All Application Functionality")
    print("=" * 50)
    
    # Test backend health
    if not test_endpoint("http://localhost:5000/api/health", "Health Check"):
        print("❌ Backend is not responding!")
        return False
    
    # Test inventory endpoints
    print("\n📋 INVENTORY MANAGEMENT:")
    inventory_ok = all([
        test_endpoint("http://localhost:5000/api/servers", "Servers"),
        test_endpoint("http://localhost:5000/api/databases", "Databases"),
        test_endpoint("http://localhost:5000/api/file-shares", "File Shares")
    ])
    
    # Test dashboard
    print("\n📊 DASHBOARD:")
    dashboard_ok = test_endpoint("http://localhost:5000/api/dashboard", "Dashboard Data")
    
    # Test configuration endpoints
    print("\n⚙️ CONFIGURATION:")
    config_ok = all([
        test_endpoint("http://localhost:5000/api/cloud-preferences", "Cloud Preferences"),
        test_endpoint("http://localhost:5000/api/business-constraints", "Business Constraints"),
        test_endpoint("http://localhost:5000/api/resource-rates", "Resource Rates")
    ])
    
    # Test analysis endpoints
    print("\n📈 ANALYSIS & PLANNING:")
    analysis_ok = all([
        test_endpoint("http://localhost:5000/api/cost-estimation", "Cost Estimation"),
        test_endpoint("http://localhost:5000/api/ai-status", "AI Status")
    ])
    
    print("\n" + "=" * 50)
    print("OVERALL STATUS:")
    print(f"✅ Inventory: {'PASS' if inventory_ok else 'FAIL'}")
    print(f"✅ Dashboard: {'PASS' if dashboard_ok else 'FAIL'}")
    print(f"✅ Configuration: {'PASS' if config_ok else 'FAIL'}")
    print(f"✅ Analysis: {'PASS' if analysis_ok else 'FAIL'}")
    
    all_ok = inventory_ok and dashboard_ok and config_ok and analysis_ok
    print(f"\n🎯 APPLICATION STATUS: {'FULLY FUNCTIONAL' if all_ok else 'NEEDS FIXES'}")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
