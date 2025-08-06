#!/usr/bin/env python3
"""
Final verification script - test if servers are working
"""
import time
import subprocess
import os

def check_port(port):
    """Check if a port is in use"""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        return f':{port}' in result.stdout
    except Exception:
        return False

def test_server_response():
    """Test server response with curl or requests"""
    try:
        import requests
        
        print("Testing backend with requests...")
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            print(f"Backend health check: Status {response.status_code}")
            if response.status_code == 200:
                print("✓ Backend is responding!")
                return True
        except requests.exceptions.ConnectionError:
            print("✗ Backend connection refused")
        except Exception as e:
            print(f"✗ Backend error: {e}")
            
    except ImportError:
        print("Requests not available, trying curl...")
        try:
            result = subprocess.run(['curl', '-s', 'http://localhost:5000/api/health'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ Backend responding via curl!")
                return True
            else:
                print("✗ Backend not responding via curl")
        except Exception as e:
            print(f"✗ Curl failed: {e}")
    
    return False

def main():
    print("=== Final Server Verification ===\n")
    
    print("1. Checking if ports are in use...")
    backend_port = check_port(5000)
    frontend_port = check_port(5173)
    
    print(f"Backend port 5000 in use: {backend_port}")
    print(f"Frontend port 5173 in use: {frontend_port}")
    
    if not backend_port:
        print("\n⚠️  Backend port 5000 is not in use!")
        print("This suggests the backend server is not running.")
    
    if not frontend_port:
        print("\n⚠️  Frontend port 5173 is not in use!")  
        print("This suggests the frontend server is not running.")
    
    print("\n2. Testing HTTP response...")
    backend_working = test_server_response()
    
    if backend_working:
        print("\n✅ Backend is working correctly!")
    else:
        print("\n❌ Backend is not responding to HTTP requests")
        print("\nPossible issues:")
        print("- Server failed to start due to import errors")
        print("- Port is blocked by firewall")
        print("- Python path issues")
        print("- Missing dependencies")
    
    print("\n3. Next steps:")
    if not backend_working:
        print("- Check VS Code terminal output for error messages")
        print("- Verify Python and Flask installation")
        print("- Try running: pip install -r requirements.txt")
        print("- Try running backend manually in a new terminal")

if __name__ == "__main__":
    main()
