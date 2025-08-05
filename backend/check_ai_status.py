import json
import urllib.request

try:
    response = urllib.request.urlopen('http://localhost:5000/api/ai-status')
    data = json.loads(response.read().decode())
    print("=== AI Status from Backend ===")
    print(json.dumps(data, indent=2))
    
    response = urllib.request.urlopen('http://localhost:5000/api/cost-estimation')
    data = json.loads(response.read().decode())
    print("\n=== Cost Estimation AI Insights ===")
    print(json.dumps(data['ai_insights'], indent=2))
    
except Exception as e:
    print(f"Error: {e}")
