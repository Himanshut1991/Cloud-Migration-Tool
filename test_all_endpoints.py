import json
import urllib.request
import urllib.parse

def test_endpoint(url, method='GET', data=None):
    """Test an API endpoint"""
    try:
        if method == 'POST' and data:
            data_bytes = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'})
        else:
            req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ {method} {url} - Status: {response.status}")
            if isinstance(result, dict):
                print(f"   Response keys: {list(result.keys())}")
            elif isinstance(result, list):
                print(f"   Response: List with {len(result)} items")
            else:
                print(f"   Response type: {type(result)}")
            return True
    except Exception as e:
        print(f"❌ {method} {url} - Error: {e}")
        return False

def main():
    base_url = 'http://localhost:5000/api'
    
    print("Testing Cloud Migration Tool Backend APIs")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoints = [
        ('GET', '/health'),
        ('GET', '/dashboard'),
        ('GET', '/servers'),
        ('GET', '/databases'),
        ('GET', '/file-shares'),
        ('GET', '/cloud-preferences'),
        ('GET', '/business-constraints'),
        ('GET', '/resource-rates'),
    ]
    
    for method, endpoint in test_endpoints:
        test_endpoint(f"{base_url}{endpoint}", method)
    
    print("\nTesting Analysis Endpoints:")
    print("-" * 30)
    
    # Test analysis endpoints
    test_endpoint(f"{base_url}/cost-estimation", 'GET')
    test_endpoint(f"{base_url}/ai-status", 'GET')
    test_endpoint(f"{base_url}/migration-strategy", 'POST', {})
    test_endpoint(f"{base_url}/timeline", 'POST', {'start_date': '2024-03-01'})

if __name__ == '__main__':
    main()
