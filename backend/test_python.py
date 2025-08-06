print("Hello from Python!")
print("Python is working correctly!")

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    import flask
    print("✅ Flask is available")
    print(f"Flask version: {flask.__version__}")
except ImportError as e:
    print(f"❌ Flask not available: {e}")

try:
    from flask import Flask
    app = Flask(__name__)
    print("✅ Flask app created successfully")
except Exception as e:
    print(f"❌ Flask app creation failed: {e}")

print("Python test complete!")
input("Press Enter to continue...")
