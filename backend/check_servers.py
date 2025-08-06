import subprocess
import time
import requests
import sys

def check_server_status():
    print("=== Server Status Check ===\n")
    
    # Check if ports are in use
    print("1. Checking ports...")
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        port_5000 = ':5000' in result.stdout
        port_5173 = ':5173' in result.stdout
        
        print(f"   Port 5000 (Backend): {'✓ IN USE' if port_5000 else '✗ NOT IN USE'}")
        print(f"   Port 5173 (Frontend): {'✓ IN USE' if port_5173 else '✗ NOT IN USE'}")
    except Exception as e:
        print(f"   Error checking ports: {e}")
    
    # Test HTTP responses
    print("\n2. Testing HTTP responses...")
    
    # Test backend
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        print(f"   Backend Health: ✓ Status {response.status_code}")
        backend_working = True
    except requests.exceptions.ConnectionError:
        print("   Backend Health: ✗ Connection refused")
        backend_working = False
    except Exception as e:
        print(f"   Backend Health: ✗ Error: {e}")
        backend_working = False
    
    # Test frontend  
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        print(f"   Frontend: ✓ Status {response.status_code}")
        frontend_working = True
    except requests.exceptions.ConnectionError:
        print("   Frontend: ✗ Connection refused")
        frontend_working = False
    except Exception as e:
        print(f"   Frontend: ✗ Error: {e}")
        frontend_working = False
    
    # Summary
    print("\n3. Summary:")
    if backend_working and frontend_working:
        print("   ✅ Both servers are running correctly!")
    elif backend_working:
        print("   ⚠️  Backend is working, but frontend is not responding")
    elif frontend_working:
        print("   ⚠️  Frontend is working, but backend is not responding")
    else:
        print("   ❌ Neither server is responding")
        print("   \n   Troubleshooting steps:")
        print("   - Check VS Code terminal for error messages")
        print("   - Verify Python and Node.js are installed")
        print("   - Try running servers manually in separate terminals")

if __name__ == "__main__":
    check_server_status()
