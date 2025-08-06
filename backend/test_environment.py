#!/usr/bin/env python3
"""
Test Python environment and required packages
"""
import sys
import os

def test_python_environment():
    print("=" * 60)
    print("PYTHON ENVIRONMENT TEST")
    print("=" * 60)
    
    # Test Python version
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")
    print()
    
    # Test required imports
    required_packages = [
        ('flask', 'Flask web framework'),
        ('flask_cors', 'Flask CORS extension'),
        ('sqlite3', 'SQLite database'),
        ('json', 'JSON handling'),
        ('datetime', 'Date and time'),
        ('os', 'Operating system interface')
    ]
    
    print("PACKAGE AVAILABILITY:")
    print("-" * 40)
    
    all_available = True
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError as e:
            print(f"❌ {package:15} - MISSING: {e}")
            all_available = False
    
    print()
    
    if all_available:
        print("✅ ALL PACKAGES AVAILABLE - Ready to start backend!")
        
        # Test Flask app creation
        try:
            from flask import Flask, jsonify
            from flask_cors import CORS
            
            app = Flask(__name__)
            CORS(app)
            
            @app.route('/test')
            def test():
                return jsonify({'test': 'success'})
                
            print("✅ Flask app creation successful")
            
            # Test database file
            db_path = os.path.join(os.getcwd(), 'migration_tool.db')
            if os.path.exists(db_path):
                print(f"✅ Database file exists: {db_path}")
            else:
                print(f"⚠️  Database file not found: {db_path}")
                print("   This is OK - will use sample data")
                
        except Exception as e:
            print(f"❌ Flask app creation failed: {e}")
            all_available = False
    else:
        print("❌ MISSING PACKAGES - Install with:")
        print("   pip install flask flask-cors")
    
    print()
    print("=" * 60)
    return all_available

if __name__ == "__main__":
    success = test_python_environment()
    if success:
        print("🚀 Environment ready - you can start the backend!")
    else:
        print("🔧 Fix the issues above before starting the backend")
    
    input("\nPress Enter to continue...")
