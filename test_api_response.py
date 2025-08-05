import requests
import json

# Test the cost estimation endpoint
try:
    response = requests.get('http://localhost:5000/api/cost-estimation')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test migration strategy endpoint
try:
    response = requests.post('http://localhost:5000/api/migration-strategy', json={})
    print(f"\nMigration Strategy Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Migration Strategy Error: {e}")

# Test timeline endpoint
try:
    response = requests.post('http://localhost:5000/api/timeline', json={'start_date': '2024-03-01'})
    print(f"\nTimeline Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Timeline Error: {e}")
