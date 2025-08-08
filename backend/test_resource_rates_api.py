import requests
import json

try:
    response = requests.get('http://localhost:5000/api/resource-rates')
    print('Status:', response.status_code)
    data = response.json()
    print('Sample rate:')
    if data['resource_rates']:
        print(json.dumps(data['resource_rates'][0], indent=2))
    else:
        print('No rates found')
except Exception as e:
    print('Error:', e)
