import json
import urllib.request

def test_timeline():
    try:
        # Test timeline endpoint
        data = json.dumps({'start_date': '2024-03-01'}).encode('utf-8')
        req = urllib.request.Request(
            'http://localhost:5000/api/timeline',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Timeline endpoint working - Status: {response.status}")
            print(f"   Project duration: {result['project_overview']['total_duration_weeks']} weeks")
            print(f"   Phases: {len(result['phases'])}")
            return True
            
    except Exception as e:
        print(f"❌ Timeline endpoint error: {e}")
        return False

def test_cost_estimation():
    try:
        req = urllib.request.Request('http://localhost:5000/api/cost-estimation')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Cost estimation endpoint working - Status: {response.status}")
            print(f"   Monthly cost: ${result['total_monthly_cost']}")
            print(f"   AI available: {result['ai_insights']['ai_available']}")
            print(f"   Using fallback: {result['ai_insights']['fallback_used']}")
            return True
            
    except Exception as e:
        print(f"❌ Cost estimation endpoint error: {e}")
        return False

if __name__ == '__main__':
    print("Testing specific endpoints:")
    print("=" * 40)
    test_timeline()
    print()
    test_cost_estimation()
