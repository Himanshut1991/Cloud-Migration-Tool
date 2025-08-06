#!/usr/bin/env python3
"""
Diagnose import issues and test basic server startup
"""

def test_imports():
    """Test all required imports"""
    print("Testing Python imports...")
    
    try:
        import sys
        print(f"✓ Python version: {sys.version}")
    except Exception as e:
        print(f"✗ Python system error: {e}")
        return False
    
    try:
        import flask
        print(f"✓ Flask version: {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        from flask import Flask
        print("✓ Flask.Flask import successful")
    except ImportError as e:
        print(f"✗ Flask.Flask import failed: {e}")
        return False
        
    try:
        from flask_cors import CORS
        print("✓ Flask-CORS import successful")
    except ImportError as e:
        print(f"✗ Flask-CORS import failed: {e}")
        return False
        
    try:
        import sqlite3
        print("✓ SQLite3 import successful")
    except ImportError as e:
        print(f"✗ SQLite3 import failed: {e}")
        return False
        
    return True

def test_basic_server():
    """Test creating a basic Flask server"""
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return "Server test successful"
            
        print("✓ Flask app created successfully")
        return app
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return None

if __name__ == "__main__":
    print("=== Cloud Migration Tool Backend Diagnostics ===\n")
    
    if test_imports():
        print("\n✓ All imports successful!")
        
        app = test_basic_server()
        if app:
            print("\n✓ Flask app ready to start!")
            print("Attempting to start server on port 5000...")
            try:
                app.run(host='0.0.0.0', port=5000, debug=False)
            except Exception as e:
                print(f"✗ Server startup failed: {e}")
        else:
            print("\n✗ Flask app creation failed")
    else:
        print("\n✗ Import tests failed - please install missing packages")
        print("Run: pip install -r requirements.txt")
