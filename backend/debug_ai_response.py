#!/usr/bin/env python3
"""
Debug AI Response Structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_recommendations import AIRecommendationService
import json

def debug_ai_response():
    print("🔍 Debugging AI Response Structure...")
    print("=" * 50)
    
    ai_service = AIRecommendationService()
    
    # Test data
    test_infrastructure = {
        'servers': [
            {'server_id': 'TEST-001', 'vcpu': 4, 'ram': 16, 'disk_size': 500, 'os_type': 'Windows'}
        ],
        'databases': [
            {'db_name': 'TestDB', 'engine': 'MySQL', 'size_gb': 100}
        ],
        'file_shares': [
            {'share_name': 'TestShare', 'total_size_gb': 500}
        ]
    }
    
    print("📊 Testing Cost Estimation Response...")
    cost_result = ai_service.get_ai_cost_estimation(test_infrastructure, 'AWS', 'us-east-1')
    
    print("🔍 AI Insights Structure:")
    if 'ai_insights' in cost_result:
        ai_insights = cost_result['ai_insights']
        print(f"  - ai_model_used: {ai_insights.get('ai_model_used', 'NOT FOUND')}")
        print(f"  - confidence_level: {ai_insights.get('confidence_level', 'NOT FOUND')}")
        print(f"  - fallback_used: {ai_insights.get('fallback_used', 'NOT FOUND')}")
        print(f"  - Full ai_insights keys: {list(ai_insights.keys())}")
        
        print("\n📝 Full AI Insights JSON:")
        print(json.dumps(ai_insights, indent=2))
    else:
        print("❌ No ai_insights found in response!")
        print("📝 Available keys:", list(cost_result.keys()))
    
    print("\n" + "=" * 50)
    print("🚀 Testing Migration Strategy Response...")
    strategy_result = ai_service.get_ai_migration_strategy(test_infrastructure, 'AWS', 'us-east-1', 'medium')
    
    print("🔍 AI Insights Structure:")
    if 'ai_insights' in strategy_result:
        ai_insights = strategy_result['ai_insights']
        print(f"  - ai_model_used: {ai_insights.get('ai_model_used', 'NOT FOUND')}")
        print(f"  - confidence_level: {ai_insights.get('confidence_level', 'NOT FOUND')}")
        print(f"  - fallback_used: {ai_insights.get('fallback_used', 'NOT FOUND')}")
        print(f"  - Full ai_insights keys: {list(ai_insights.keys())}")
    else:
        print("❌ No ai_insights found in response!")

if __name__ == "__main__":
    debug_ai_response()
