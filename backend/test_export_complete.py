#!/usr/bin/env python3
"""Test export and download functionality"""

import requests
import json
import time

def test_export_functionality():
    """Test the complete export workflow"""
    base_url = "http://localhost:5000"
    
    print("📄 Testing Export and Download Functionality")
    print("=" * 60)
    
    # Test all export formats
    formats = ['pdf', 'excel', 'word']
    
    for format_type in formats:
        print(f"\n🧪 Testing {format_type.upper()} export...")
        
        try:
            # Test export
            export_response = requests.post(
                f"{base_url}/api/export",
                json={"format": format_type},
                timeout=30
            )
            
            if export_response.status_code == 200:
                result = export_response.json()
                filename = result.get('filename')
                file_size = result.get('file_size', 0)
                
                print(f"   ✅ Export successful: {filename}")
                print(f"   📊 File size: {file_size:,} bytes")
                
                # Test download
                download_response = requests.get(
                    f"{base_url}/api/download/{filename}",
                    timeout=10
                )
                
                if download_response.status_code == 200:
                    print(f"   ✅ Download successful")
                    print(f"   📥 Downloaded {len(download_response.content):,} bytes")
                else:
                    print(f"   ❌ Download failed: {download_response.status_code}")
                    if download_response.headers.get('content-type') == 'application/json':
                        error = download_response.json().get('error', 'Unknown error')
                        print(f"      Error: {error}")
                        
            else:
                print(f"   ❌ Export failed: {export_response.status_code}")
                if export_response.headers.get('content-type') == 'application/json':
                    error = export_response.json().get('error', 'Unknown error')
                    print(f"      Error: {error}")
                    
        except Exception as e:
            print(f"   ❌ Test failed: {str(e)}")
    
    print(f"\n✅ Export functionality testing completed!")

if __name__ == "__main__":
    test_export_functionality()
