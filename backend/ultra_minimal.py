#!/usr/bin/env python3
"""
Ultra minimal test server to check basic functionality
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Cloud Migration Tool Backend!"

@app.route('/api/test')
def test():
    return {"status": "OK", "message": "Server is running"}

if __name__ == '__main__':
    print("Starting ultra minimal server...")
    print("Backend will run on: http://localhost:5000")
    print("Test endpoint: http://localhost:5000/api/test")
    app.run(host='0.0.0.0', port=5000, debug=True)
print("All tests completed.")
