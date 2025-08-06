#!/usr/bin/env python3
"""Simple AI service test script"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_recommendations import AIRecommendationService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ai_service():
    """Test the AI service initialization and basic functionality"""
    print("🧪 Testing AI Recommendation Service...")
    
    try:
        # Initialize AI service
        ai_service = AIRecommendationService()
        
        if ai_service.bedrock_client is None:
            print("❌ AI service not available - using fallback logic")
        else:
            print(f"✅ AI service initialized successfully with model: {ai_service.model_id}")
        
        # Test server recommendation
        print("\n🖥️  Testing server recommendation...")
        server_specs = {
            'server_id': 1,
            'os_type': 'Windows',
            'vcpu': 4,
            'ram': 16,
            'disk_size': 500,
            'disk_type': 'SSD',
            'uptime_pattern': 'Business Hours',
            'current_hosting': 'On-Premises',
            'technology': 'IIS, .NET Framework'
        }
        
        recommendation = ai_service.get_server_recommendation(server_specs)
        print("Server recommendation:", recommendation)
        
        print("\n✅ AI service test completed successfully!")
        
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_service()
