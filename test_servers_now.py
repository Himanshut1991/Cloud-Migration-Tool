import requests
import json

def test_backend():
    """Test if backend is responding"""
    try:
        # Test basic health endpoint
        response = requests.get('http://localhost:5000/api/servers', timeout=5)
        print(f"Backend response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Backend data: {json.dumps(data, indent=2)}")
        else:
            print(f"Backend response text: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Backend is not running - Connection refused")
    except requests.exceptions.Timeout:
        print("Backend is not responding - Timeout")
    except Exception as e:
        print(f"Error testing backend: {e}")

def test_frontend():
    """Test if frontend is responding"""
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        print(f"Frontend response status: {response.status_code}")
        if response.status_code == 200:
            print("Frontend is running")
        else:
            print(f"Frontend response: {response.text[:200]}...")
    except requests.exceptions.ConnectionError:
        print("Frontend is not running - Connection refused")
    except requests.exceptions.Timeout:
        print("Frontend is not responding - Timeout")  
    except Exception as e:
        print(f"Error testing frontend: {e}")

if __name__ == "__main__":
    print("Testing servers...")
    print("\n--- Backend Test ---")
    test_backend()
    print("\n--- Frontend Test ---")
    test_frontend()
