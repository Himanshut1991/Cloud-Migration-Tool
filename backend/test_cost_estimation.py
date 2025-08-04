#!/usr/bin/env python3
"""Test the cost estimation with AI directly"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.cost_calculator import CostCalculator

def test_cost_estimation_with_ai():
    """Test cost estimation with AI integration"""
    print("=== Testing Cost Estimation with AI ===")
    
    calculator = CostCalculator()
    
    # Test with sample inventory data
    servers = [
        {
            'id': 1,
            'server_name': 'WEB-SERVER-01',
            'os_type': 'Windows Server 2019',
            'vcpu': 4,
            'ram': 16,
            'disk_size': 500,
            'disk_type': 'SSD',
            'uptime_pattern': '24/7',
            'current_hosting': 'On-premises',
            'technology': 'IIS, .NET Framework'
        },
        {
            'id': 2,
            'server_name': 'DB-SERVER-01',
            'os_type': 'Linux',
            'vcpu': 8,
            'ram': 32,
            'disk_size': 1000,
            'disk_type': 'SSD',
            'uptime_pattern': 'Business hours',
            'current_hosting': 'On-premises',
            'technology': 'MySQL, Apache'
        }
    ]
    
    databases = [
        {
            'id': 1,
            'database_name': 'ProductionDB',
            'db_type': 'MySQL',
            'version': '8.0',
            'size_gb': 500,
            'transactions_per_day': 100000,
            'backup_retention_days': 30,
            'high_availability': True
        }
    ]
    
    file_shares = [
        {
            'id': 1,
            'share_name': 'CompanyFiles',
            'share_type': 'SMB',
            'total_size_gb': 2000,
            'active_users': 150,
            'growth_rate_monthly': 5.0,
            'backup_enabled': True
        }
    ]
    
    # Run cost estimation
    try:
        result = calculator.calculate_costs(servers, databases, file_shares)
        
        print(f"✅ Cost calculation completed")
        print(f"   Total Monthly Cost: ${result.get('total_monthly_cost', 0):,.2f}")
        print(f"   Server Costs: ${result.get('server_costs', {}).get('total', 0):,.2f}")
        print(f"   Database Costs: ${result.get('database_costs', {}).get('total', 0):,.2f}")
        print(f"   Storage Costs: ${result.get('storage_costs', {}).get('total', 0):,.2f}")
        
        # Check if AI recommendations are included
        if 'ai_insights' in result:
            print(f"✅ AI Insights available: {len(result['ai_insights'])} insights")
            for insight in result['ai_insights'][:2]:  # Show first 2
                print(f"   - {insight[:100]}...")
        else:
            print("ℹ️  No AI insights (using fallback mode)")
            
        return True
        
    except Exception as e:
        print(f"❌ Cost calculation failed: {e}")
        return False

if __name__ == "__main__":
    test_cost_estimation_with_ai()
