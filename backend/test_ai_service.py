#!/usr/bin/env python3
"""Clean test of the improved AIRecommendationService"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_recommendations import AIRecommendationService

def test_ai_service():
    """Test the improved AI service"""
    print("=== Testing AIRecommendationService ===")
    
    ai_service = AIRecommendationService()
    
    # Check if AI is available
    if ai_service.bedrock_client:
        print(f"✅ AI Service initialized successfully")
        print(f"✅ Using model: {ai_service.model_id}")
        print(f"✅ Region: {ai_service.region_name}")
    else:
        print("❌ AI Service in fallback mode")
        return
    
    # Test server recommendation
    print("\n=== Testing Server Recommendation ===")
    server_specs = {
        'server_id': 'TEST-001',
        'os_type': 'Windows Server 2019',
        'vcpu': 4,
        'ram': 16,
        'disk_size': 500,
        'disk_type': 'SSD',
        'uptime_pattern': '24/7',
        'current_hosting': 'On-premises',
        'technology': 'IIS, .NET Framework'
    }
    
    try:
        recommendation = ai_service.get_server_recommendation(server_specs)
        print(f"✅ Server recommendation received")
        print(f"   Primary: {recommendation.get('primary_recommendation', 'N/A')}")
        print(f"   Confidence: {recommendation.get('confidence_level', 'N/A')}")
        print(f"   Reasoning: {recommendation.get('reasoning', 'N/A')[:100]}...")
    except Exception as e:
        print(f"❌ Server recommendation failed: {e}")
    
    print("\n=== AI Service Test Complete ===")

if __name__ == "__main__":
    test_ai_service()
