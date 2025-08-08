import requests
import json

# Test cloud preferences
print("Testing Cloud Preferences...")
try:
    # Test GET
    response = requests.get('http://localhost:5000/api/cloud-preferences')
    print(f"GET Status: {response.status_code}")
    print(f"GET Data: {json.dumps(response.json(), indent=2)}")
    
    # Test POST
    test_data = {
        'cloud_provider': 'AWS',
        'region': 'us-west-2',
        'preferred_services': 'EC2,S3,RDS',
        'network_config': 'Custom VPC'
    }
    response = requests.post('http://localhost:5000/api/cloud-preferences', json=test_data)
    print(f"POST Status: {response.status_code}")
    print(f"POST Response: {response.json()}")
    
except Exception as e:
    print(f"Error testing cloud preferences: {e}")

print("\n" + "="*50 + "\n")

# Test business constraints
print("Testing Business Constraints...")
try:
    # Test GET
    response = requests.get('http://localhost:5000/api/business-constraints')
    print(f"GET Status: {response.status_code}")
    print(f"GET Data: {json.dumps(response.json(), indent=2)}")
    
    # Test POST
    test_data = {
        'migration_window': 'After Hours',
        'cutover_date': '2025-12-15',
        'downtime_tolerance': 'Medium',
        'budget_cap': '750000'
    }
    response = requests.post('http://localhost:5000/api/business-constraints', json=test_data)
    print(f"POST Status: {response.status_code}")
    print(f"POST Response: {response.json()}")
    
except Exception as e:
    print(f"Error testing business constraints: {e}")
