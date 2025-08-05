#!/usr/bin/env python3
"""Test script to verify backend functionality"""

import sys
import os
import requests
import time

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def test_simple_server():
    """Test if simple server can start"""
    print("Testing simple server...")
    try:
        from simple_test_server import app
        print("✓ Simple server imports work")
        
        # Test with test client
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✓ Simple server endpoints work")
                return True
            else:
                print(f"✗ Simple server endpoint error: {response.status_code}")
    except Exception as e:
        print(f"✗ Simple server error: {e}")
    return False

def test_main_app():
    """Test if main app can import"""
    print("\nTesting main app...")
    try:
        from app import app, db
        print("✓ Main app imports work")
        
        # Test database
        with app.app_context():
            try:
                db.create_all()
                print("✓ Database initialization works")
                
                # Test basic models
                from app import Server, Database, FileShare
                servers = Server.query.count()
                databases = Database.query.count()
                fileshares = FileShare.query.count()
                
                print(f"✓ Database query works - Servers: {servers}, Databases: {databases}, FileShares: {fileshares}")
                
                if servers == 0 and databases == 0 and fileshares == 0:
                    print("! No sample data found - need to populate")
                    return "no_data"
                
                return True
            except Exception as e:
                print(f"✗ Database error: {e}")
    except Exception as e:
        print(f"✗ Main app error: {e}")
        import traceback
        traceback.print_exc()
    return False

def populate_sample_data():
    """Populate sample data"""
    print("\nPopulating sample data...")
    try:
        from populate_sample_data import populate_all_data
        from app import app
        
        with app.app_context():
            populate_all_data()
            print("✓ Sample data populated")
            return True
    except Exception as e:
        print(f"✗ Sample data error: {e}")
        import traceback
        traceback.print_exc()
    return False

if __name__ == '__main__':
    print("Backend Diagnosis Tool")
    print("=" * 40)
    
    # Test simple server
    simple_works = test_simple_server()
    
    # Test main app
    main_result = test_main_app()
    
    # Populate data if needed
    if main_result == "no_data":
        if populate_sample_data():
            main_result = test_main_app()
    
    print("\n" + "=" * 40)
    print("Results:")
    print(f"Simple Server: {'✓ Working' if simple_works else '✗ Failed'}")
    print(f"Main App: {'✓ Working' if main_result is True else '✗ Failed'}")
    
    if simple_works and main_result is True:
        print("\n✓ Backend should work properly!")
        print("Try running: python app.py")
    else:
        print("\n✗ Backend has issues that need fixing")
