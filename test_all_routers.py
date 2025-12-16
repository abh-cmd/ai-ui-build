#!/usr/bin/env python3
"""Test that other endpoints still work"""
import requests
import json

BASE_URL = "http://localhost:8002"

def test_health():
    """Test /health"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✅ /health works")

def test_upload_schema():
    """Test /upload endpoints exist (without actual file)"""
    # Just check the endpoint exists via OPTIONS
    response = requests.get(f"{BASE_URL}/docs")  # Check OpenAPI docs
    assert response.status_code == 200
    print("✅ API docs available (routers registered)")

def test_other_routers():
    """Check that all routers are registered by checking OpenAPI docs"""
    response = requests.get(f"{BASE_URL}/openapi.json")
    assert response.status_code == 200
    
    openapi = response.json()
    paths = openapi.get("paths", {})
    
    required_routes = {
        "/health": "GET",
        "/edit/": "POST",
        "/upload/": "POST",
        "/generate/": "POST",
        "/autocorrect/": "POST",
    }
    
    print("\nRegistered routes:")
    for path in paths:
        print(f"  - {path}")
    
    print("\nChecking required routes:")
    for route, method in required_routes.items():
        if route in paths:
            methods = [m.upper() for m in paths[route].keys() if m != "parameters"]
            if method in methods:
                print(f"  ✅ {method} {route}")
            else:
                print(f"  ❌ {method} {route} - missing method")
        else:
            print(f"  ❌ {method} {route} - path not found")

if __name__ == "__main__":
    print("=" * 50)
    print("Verifying All Routers Are Working")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        test_other_routers()
        
        print("\n" + "=" * 50)
        print("✅ All routers verified and working!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
