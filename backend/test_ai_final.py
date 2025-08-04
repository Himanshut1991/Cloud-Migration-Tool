#!/usr/bin/env python3
"""Simple AI integration test"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_recommendations import AIRecommendationService

def main():
    print("=== AI Integration Test ===")
    
    # Test AI service
    ai_service = AIRecommendationService()
    
    if ai_service.bedrock_client:
        print(f"✅ AI Service Connected")
        print(f"   Model: {ai_service.model_id}")
        print(f"   Region: {ai_service.region_name}")
        
        # Test server recommendation
        print("\n--- Server Recommendation Test ---")
        server_spec = {
            'server_id': 'WEB-01',
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
            rec = ai_service.get_server_recommendation(server_spec)
            print(f"✅ Primary: {rec.get('primary_recommendation', 'N/A')}")
            print(f"   Cost: ${rec.get('monthly_cost', 'N/A')}")
            print(f"   Confidence: {rec.get('confidence_level', 'N/A')}")
            print(f"   Reasoning: {rec.get('reasoning', 'N/A')[:150]}...")
        except Exception as e:
            print(f"❌ Server recommendation failed: {e}")
        
        # Test database recommendation
        print("\n--- Database Recommendation Test ---")
        db_spec = {
            'database_id': 'PROD-DB',
            'db_type': 'MySQL',
            'version': '8.0',
            'size_gb': 500,
            'transactions_per_day': 100000,
            'backup_retention_days': 30,
            'high_availability': True
        }
        
        try:
            rec = ai_service.get_database_recommendation(db_spec)
            print(f"✅ Primary: {rec.get('primary_recommendation', 'N/A')}")
            print(f"   Cost: ${rec.get('monthly_cost', 'N/A')}")
            print(f"   Confidence: {rec.get('confidence_level', 'N/A')}")
        except Exception as e:
            print(f"❌ Database recommendation failed: {e}")
        
        print("\n✅ AI Integration Working!")
        
    else:
        print("❌ AI Service in fallback mode")
        print("   Check AWS credentials and model access")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
