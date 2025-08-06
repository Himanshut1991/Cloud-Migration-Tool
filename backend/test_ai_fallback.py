#!/usr/bin/env python3
"""Test AI service fallback sequence"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_recommendations import AIRecommendationService
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_model_fallback():
    """Test AI model fallback sequence"""
    print("🧪 Testing AI model fallback sequence...")
    print("Expected order: 1. Claude 3.5 Sonnet → 2. Claude 3 Sonnet → 3. Titan Text G1 - Express")
    print("=" * 80)
    
    try:
        # Initialize AI service
        ai_service = AIRecommendationService()
        
        if ai_service.bedrock_client is None:
            print("❌ No Bedrock client available - using fallback logic only")
            return
        
        print(f"✅ Bedrock client initialized successfully")
        print(f"🤖 Selected model: {ai_service.model_id}")
        
        # Test cost optimization to see actual AI vs fallback
        print("\n💰 Testing cost optimization recommendations...")
        inventory_data = {
            'servers': [{'id': 1, 'os': 'Windows', 'hosting': 'On-Premises'}],
            'databases': [{'name': 'AppDB', 'type': 'SQL Server', 'size_gb': 100}],
            'file_shares': [{'name': 'DataShare', 'size_gb': 500}],
            'total_monthly_cost': 1000,
            'cost_breakdown': {'compute': 600, 'database': 300, 'storage': 100}
        }
        
        cost_recommendations = ai_service.get_cost_optimization_recommendations(inventory_data)
        
        if cost_recommendations:
            is_fallback = cost_recommendations.get('fallback_used', False)
            if is_fallback:
                print("📋 Using rule-based fallback recommendations")
                print(f"   Reason: {cost_recommendations.get('fallback_reason', 'AI service unavailable')}")
            else:
                print("🤖 Using AI-powered recommendations!")
                print(f"   Model: {ai_service.model_id}")
                print(f"   Confidence: {cost_recommendations.get('confidence_level', 'N/A')}%")
            
            print("\nRecommendations:")
            for i, rec in enumerate(cost_recommendations.get('recommendations', []), 1):
                print(f"   {i}. {rec}")
        
        print("\n🖥️  Testing server recommendations...")
        server_specs = {
            'server_id': 1,
            'os_type': 'Windows',
            'vcpu': 4,
            'ram': 16,
            'disk_size': 500
        }
        
        server_rec = ai_service.get_server_recommendation(server_specs)
        
        if server_rec:
            is_fallback = server_rec.get('fallback_used', False)
            if is_fallback:
                print("📋 Using rule-based server recommendation")
            else:
                print("🤖 Using AI-powered server recommendation!")
                print(f"   Recommended instance: {server_rec.get('recommended_instance')}")
                print(f"   Confidence: {server_rec.get('confidence_level')}")
        
        print("\n✅ Testing completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_fallback()
