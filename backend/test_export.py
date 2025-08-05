#!/usr/bin/env python3
"""Test export functionality"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app, db
import json

def test_export():
    """Test export endpoints"""
    with app.test_client() as client:
        # Test health endpoint
        print("Testing health endpoint...")
        response = client.get('/api/health')
        print(f"Health status: {response.status_code}")
        
        # Test Excel export
        print("\nTesting Excel export...")
        response = client.post('/api/export', 
                              json={'format': 'excel'},
                              content_type='application/json')
        print(f"Excel export status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"Excel export result: {json.dumps(data, indent=2)}")
        else:
            print(f"Excel export error: {response.get_data(as_text=True)}")
        
        # Test PDF export
        print("\nTesting PDF export...")
        response = client.post('/api/export', 
                              json={'format': 'pdf'},
                              content_type='application/json')
        print(f"PDF export status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"PDF export result: {json.dumps(data, indent=2)}")
        else:
            print(f"PDF export error: {response.get_data(as_text=True)}")

if __name__ == '__main__':
    print("Testing Export Functionality")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Initialize database
            db.create_all()
            print("Database initialized")
            
            # Run tests
            test_export()
            
        except Exception as e:
            print(f"Test error: {e}")
            import traceback
            traceback.print_exc()
