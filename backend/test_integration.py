#!/usr/bin/env python3
"""Integration test with full app context"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import models_new
from services.cost_calculator import CostCalculator
from services.ai_recommendations import AIRecommendationService

def test_full_integration():
    """Test full integration with database and AI"""
    print("=== Full Integration Test ===")
    
    # Create Flask app and database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///migration_tool.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    with app.app_context():
        # Initialize models
        models = {
            'Server': models_new.Server,
            'Database': models_new.DatabaseInstance,
            'FileShare': models_new.FileShare,
            'CloudPreference': models_new.CloudPreference,
            'BusinessConstraint': models_new.BusinessConstraint,
            'ResourceRate': models_new.ResourceRate
        }
        
        # Test AI service directly
        print("\n--- Testing AI Service ---")
        ai_service = AIRecommendationService()
        if ai_service.bedrock_client:
            print(f"✅ AI Service: {ai_service.model_id}")
        else:
            print("⚠️  AI Service: Fallback mode")
        
        # Test cost calculator
        print("\n--- Testing Cost Calculator ---")
        try:
            calculator = CostCalculator(db, models)
            print("✅ Cost Calculator initialized")
            
            # Create sample data
            servers = [
                {
                    'id': 1,
                    'server_name': 'TEST-WEB-01',
                    'os_type': 'Windows Server 2019',
                    'vcpu': 4,
                    'ram': 16,
                    'disk_size': 500,
                    'disk_type': 'SSD',
                    'uptime_pattern': '24/7',
                    'current_hosting': 'On-premises',
                    'technology': 'IIS, .NET'
                }
            ]
            
            databases = []
            file_shares = []
            
            # Calculate costs
            result = calculator.calculate_costs(servers, databases, file_shares)
            
            print(f"✅ Cost calculation completed")
            print(f"   Total: ${result.get('total_monthly_cost', 0):,.2f}")
            
            # Check for AI insights
            if result.get('ai_insights'):
                print(f"✅ AI insights: {len(result['ai_insights'])} items")
            else:
                print("ℹ️  No AI insights")
                
        except Exception as e:
            print(f"❌ Cost calculator failed: {e}")
        
        # Test individual AI recommendation
        print("\n--- Testing Direct AI Recommendation ---")
        try:
            server_spec = {
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
            
            recommendation = ai_service.get_server_recommendation(server_spec)
            
            if recommendation.get('primary_recommendation'):
                print(f"✅ AI recommendation: {recommendation['primary_recommendation']}")
                print(f"   Confidence: {recommendation.get('confidence_level', 'N/A')}")
            else:
                print("⚠️  Using fallback recommendation")
                
        except Exception as e:
            print(f"❌ AI recommendation failed: {e}")
    
    print("\n=== Integration Test Complete ===")

if __name__ == "__main__":
    test_full_integration()
