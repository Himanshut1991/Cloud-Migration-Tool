#!/usr/bin/env python3
"""
Test script for export functionality
"""
import requests
import json

def test_export_api():
    """Test the export API with all formats and types"""
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_cases = [
        {
            "format": "excel",
            "types": ["cost_estimation", "migration_strategy", "timeline"]
        },
        {
            "format": "pdf", 
            "types": ["cost_estimation", "migration_strategy"]
        },
        {
            "format": "word",
            "types": ["cost_estimation"]
        }
    ]
    
    print("🧪 Testing Export API Functionality")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['format'].upper()} export")
        print(f"   Types: {', '.join(test_case['types'])}")
        
        try:
            # Make export request
            response = requests.post(
                f"{base_url}/api/export",
                json=test_case,
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   📄 Filename: {result.get('filename')}")
                print(f"   📏 File size: {result.get('file_size')} bytes")
                print(f"   📅 Generated: {result.get('timestamp')}")
                print(f"   🔗 Download URL: {result.get('download_url')}")
                
                # Test download endpoint
                download_url = f"{base_url}{result.get('download_url')}"
                download_response = requests.get(download_url)
                
                if download_response.status_code == 200:
                    print(f"   ⬇️ Download test: SUCCESS")
                else:
                    print(f"   ❌ Download test: FAILED ({download_response.status_code})")
                    
            else:
                print(f"   ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Export API testing completed!")

if __name__ == "__main__":
    test_export_api()
