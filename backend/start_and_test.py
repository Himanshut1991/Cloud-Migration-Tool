#!/usr/bin/env python3
"""
Simple test to start the backend and check for errors
"""

import subprocess
import time
import requests

def start_backend():
    try:
        print("Starting simple_app.py...")
        process = subprocess.Popen(['python', 'simple_app.py'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True)
        
        # Give it a few seconds to start
        print("Waiting for backend to start...")
        time.sleep(5)
        
        # Check if it's running
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            print(f"✅ Backend is running! Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Backend not responding: {e}")
            
            # Check the process output for errors
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
        
    except Exception as e:
        print(f"Error starting backend: {e}")

if __name__ == "__main__":
    start_backend()
