#!/usr/bin/env python3
"""Test API endpoints with AI integration"""

import requests
import json
import sys

def test_endpoints():
    """Test the API endpoints to verify AI vs fallback usage"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing API Endpoints for AI Integration")
    print("=" * 60)
    
    # Test Cost Estimation
    print("1️⃣  Testing Cost Estimation API...")
    try:
        response = requests.get(f"{base_url}/api/cost-estimation", timeout=30)
        if response.status_code == 200:
            data = response.json()
            ai_insights = data.get('ai_insights', {})
            
            is_fallback = ai_insights.get('fallback_used', True)
            
            print(f"   💰 Total Monthly Cost: ${data.get('total_monthly_cost', 0)}")
            print(f"   📊 Recommendations Count: {len(ai_insights.get('recommendations', []))}")
            
            if is_fallback:
                print("   📋 Result: RULE-BASED ANALYSIS")
                print(f"   🔍 Reason: {ai_insights.get('fallback_reason', 'AI not available')}")
            else:
                print("   🤖 Result: AI-POWERED ANALYSIS")
                print(f"   🎯 AI Model: {ai_insights.get('ai_model', 'Unknown')}")
                print(f"   📈 Confidence: {ai_insights.get('confidence_level', 0)}%")
                
        else:
            print(f"   ❌ Failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test Migration Strategy
    print("2️⃣  Testing Migration Strategy API...")
    try:
        response = requests.get(f"{base_url}/api/migration-strategy", timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            if 'server_recommendations' in data:
                server_recs = data.get('server_recommendations', [])
                print(f"   🖥️  Server Recommendations: {len(server_recs)}")
                
                if server_recs:
                    first_rec = server_recs[0]
                    is_fallback = first_rec.get('fallback_used', True)
                    
                    if is_fallback:
                        print("   📋 Result: RULE-BASED RECOMMENDATIONS")
                        print(f"   🔍 Reason: {first_rec.get('fallback_reason', 'AI not available')}")
                    else:
                        print("   🤖 Result: AI-POWERED RECOMMENDATIONS") 
                        print(f"   🎯 AI Model: {first_rec.get('ai_model', 'Unknown')}")
                        
                    print(f"   💡 Sample Recommendation: {first_rec.get('recommended_instance', 'N/A')}")
                    
            else:
                print("   ⚠️  No recommendations found in response")
                
        else:
            print(f"   ❌ Failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test AI Status
    print("3️⃣  Testing AI Status...")
    try:
        response = requests.get(f"{base_url}/api/ai-status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"   🤖 AI Available: {status.get('ai_available', False)}")
            print(f"   📡 Provider: {status.get('provider', 'Unknown')}")
            print(f"   💬 Status: {status.get('status_message', 'Unknown')}")
        else:
            print(f"   ❌ Failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    print("✅ API Testing Complete!")

if __name__ == "__main__":
    test_endpoints()
