#!/usr/bin/env python3
import json
import urllib.request

def test_ai_integration():
    print("=== Testing AI Integration ===\n")
    
    try:
        # Test AI status
        print("1. Testing AI Status endpoint...")
        response = urllib.request.urlopen('http://localhost:5000/api/ai-status')
        ai_status = json.loads(response.read().decode())
        
        print(f"   AI Available: {ai_status['ai_available']}")
        print(f"   Provider: {ai_status['provider']}")
        print(f"   Status: {ai_status['status_message']}")
        print()
        
        # Test cost estimation
        print("2. Testing Cost Estimation with AI...")
        response = urllib.request.urlopen('http://localhost:5000/api/cost-estimation')
        cost_data = json.loads(response.read().decode())
        
        ai_insights = cost_data.get('ai_insights', {})
        print(f"   AI Available in Cost Estimation: {ai_insights.get('ai_available', False)}")
        print(f"   Fallback Used: {ai_insights.get('fallback_used', True)}")
        print(f"   AI Status: {ai_insights.get('ai_status', 'Unknown')}")
        print(f"   Confidence Level: {ai_insights.get('confidence_level', 0)}%")
        print(f"   Number of Recommendations: {len(ai_insights.get('recommendations', []))}")
        
        if ai_insights.get('ai_available', False):
            print("   🎉 SUCCESS: AI is properly integrated!")
        else:
            print("   ℹ️  INFO: Using rule-based fallback")
            
        print("\n=== Sample Recommendations ===")
        for i, rec in enumerate(ai_insights.get('recommendations', [])[:3], 1):
            print(f"   {i}. {rec}")
            
    except Exception as e:
        print(f"❌ Error testing AI integration: {e}")

if __name__ == '__main__':
    test_ai_integration()
