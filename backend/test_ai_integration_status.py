#!/usr/bin/env python3
"""
Test AI Integration Status
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_recommendations import AIRecommendationService
import json

def test_ai_integration():
    print("🧪 Testing AI Integration Status...")
    print("=" * 50)
    
    # Initialize AI service
    ai_service = AIRecommendationService()
    
    # Check if Bedrock is available
    if ai_service.bedrock_client:
        print("✅ AWS Bedrock client initialized successfully")
        print(f"🎯 Model ID: {ai_service.model_id}")
        print(f"🌍 Region: {ai_service.region_name}")
    else:
        print("❌ AWS Bedrock client failed to initialize")
        print("📝 Will use fallback rule-based recommendations")
    
    print("\n" + "=" * 50)
    print("🔍 Testing Cost Estimation AI...")
    
    # Test data
    test_infrastructure = {
        'servers': [
            {'server_id': 'TEST-001', 'vcpu': 4, 'ram': 16, 'disk_size': 500, 'os_type': 'Windows'},
            {'server_id': 'TEST-002', 'vcpu': 8, 'ram': 32, 'disk_size': 1000, 'os_type': 'Linux'}
        ],
        'databases': [
            {'db_name': 'TestDB', 'engine': 'MySQL', 'size_gb': 100},
        ],
        'file_shares': [
            {'share_name': 'TestShare', 'total_size_gb': 500}
        ]
    }
    
    # Test cost estimation
    cost_result = ai_service.get_ai_cost_estimation(test_infrastructure, 'AWS', 'us-east-1')
    
    print(f"💰 Cost Estimation AI Status:")
    print(f"   - AI Used: {not cost_result.get('ai_insights', {}).get('fallback_used', True)}")
    print(f"   - Confidence: {cost_result.get('ai_insights', {}).get('confidence_level', 'N/A')}%")
    print(f"   - Model: {cost_result.get('ai_insights', {}).get('ai_model_used', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("🔍 Testing Migration Strategy AI...")
    
    # Test migration strategy
    strategy_result = ai_service.get_ai_migration_strategy(test_infrastructure, 'AWS', 'us-east-1', 'medium')
    
    print(f"🚀 Migration Strategy AI Status:")
    print(f"   - AI Used: {not strategy_result.get('ai_insights', {}).get('fallback_used', True)}")
    print(f"   - Confidence: {strategy_result.get('ai_insights', {}).get('confidence_level', 'N/A')}%")
    print(f"   - Model: {strategy_result.get('ai_insights', {}).get('ai_model_used', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    
    ai_cost_working = not cost_result.get('ai_insights', {}).get('fallback_used', True)
    ai_strategy_working = not strategy_result.get('ai_insights', {}).get('fallback_used', True)
    
    if ai_cost_working and ai_strategy_working:
        print("🎉 AI Integration: FULLY OPERATIONAL")
        print("✅ Both cost estimation and migration strategy are using AI")
    elif ai_cost_working or ai_strategy_working:
        print("⚠️  AI Integration: PARTIALLY OPERATIONAL")
        print(f"✅ Cost Estimation AI: {'Working' if ai_cost_working else 'Fallback'}")
        print(f"✅ Migration Strategy AI: {'Working' if ai_strategy_working else 'Fallback'}")
    else:
        print("🔄 AI Integration: FALLBACK MODE")
        print("📝 Using intelligent rule-based recommendations")
        print("💡 To enable full AI:")
        print("   1. Verify AWS credentials in .env file")
        print("   2. Ensure Bedrock models are enabled in AWS console")
        print("   3. Check network connectivity to AWS Bedrock")
    
    print("\n" + "=" * 50)
    print("🔧 AI Configuration:")
    print(f"   - AWS Region: {os.getenv('AWS_REGION', 'Not set')}")
    print(f"   - Model ID: {os.getenv('BEDROCK_MODEL_ID', 'Not set')}")
    print(f"   - Access Key ID: {os.getenv('AWS_ACCESS_KEY_ID', 'Not set')[:10]}..." if os.getenv('AWS_ACCESS_KEY_ID') else "   - Access Key ID: Not set")
    
    return ai_cost_working and ai_strategy_working

if __name__ == "__main__":
    success = test_ai_integration()
    exit(0 if success else 1)
