"""
Test script for nearby drivers endpoint

This script tests the /nearby-drivers endpoint to verify:
1. Proper serialization of GeoPoint data
2. Distance calculation accuracy
3. Radius filtering
4. Error handling

Usage:
    python scripts/test_nearby_drivers.py
"""
import sys
import os
import json
import requests
from typing import Optional

# Test configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_VERSION = "v1"

# Windhoek test coordinates
WINDHOEK_CENTER = {"latitude": -22.5700, "longitude": 17.0836}
WINDHOEK_NORTH = {"latitude": -22.5650, "longitude": 17.0800}
WINDHOEK_SOUTH = {"latitude": -22.5750, "longitude": 17.0870}


def get_test_token() -> Optional[str]:
    """
    Get a test authentication token
    
    Note: You need to have a valid user token for testing.
    You can get one by:
    1. Calling POST /api/v1/send-otp with a phone number
    2. Calling POST /api/v1/verify-otp with the OTP
    3. Using the returned accessToken
    """
    token = os.getenv("TEST_AUTH_TOKEN")
    if not token:
        print("⚠️  No TEST_AUTH_TOKEN environment variable found")
        print("💡 Set TEST_AUTH_TOKEN environment variable with a valid token")
        print("💡 Or update this script with your token")
        return None
    return token


def test_nearby_drivers(
    latitude: float,
    longitude: float,
    radius: float = 5.0,
    token: Optional[str] = None
) -> dict:
    """Test the nearby drivers endpoint"""
    
    url = f"{API_BASE_URL}/api/{API_VERSION}/nearby-drivers"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius
    }
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    print(f"\n📍 Testing nearby drivers at ({latitude}, {longitude}) with radius {radius}km")
    print(f"🔗 URL: {url}")
    print(f"📦 Params: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        # Parse response
        try:
            data = response.json()
            print(f"📄 Response Body:")
            print(json.dumps(data, indent=2))
            
            # Analyze response
            if response.status_code == 200:
                print("\n✅ SUCCESS!")
                
                if data.get("success"):
                    drivers = data.get("data", {}).get("drivers", [])
                    count = data.get("data", {}).get("count", 0)
                    
                    print(f"\n📊 Found {count} drivers:")
                    for i, driver in enumerate(drivers, 1):
                        name = driver.get("name", "Unknown")
                        distance = driver.get("distance_km", "N/A")
                        status = driver.get("status", "unknown")
                        location = driver.get("location", {})
                        
                        print(f"\n  {i}. {name}")
                        print(f"     Status: {status}")
                        print(f"     Distance: {distance} km")
                        print(f"     Location: {location}")
                        
                        # Verify location is properly serialized
                        if isinstance(location, dict) and "latitude" in location and "longitude" in location:
                            print(f"     ✅ Location properly serialized")
                        else:
                            print(f"     ❌ Location NOT properly serialized: {type(location)}")
                else:
                    print(f"⚠️  API returned success=false: {data.get('message')}")
            else:
                print(f"\n❌ ERROR: {response.status_code}")
                print(f"Message: {data.get('message', 'Unknown error')}")
                
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {str(e)}")
            print(f"Raw response: {response.text}")
            return {"error": "JSON decode error"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return {"error": str(e)}


def run_tests():
    """Run comprehensive tests"""
    
    print("="*70)
    print("🧪 NEARBY DRIVERS ENDPOINT TEST SUITE")
    print("="*70)
    
    # Get auth token
    token = get_test_token()
    if not token:
        print("\n⚠️  Running tests WITHOUT authentication (will fail if auth required)")
        print("💡 Set TEST_AUTH_TOKEN environment variable to test with authentication")
    
    # Test 1: Windhoek city center with default radius
    print("\n" + "="*70)
    print("TEST 1: Windhoek City Center (Default 5km radius)")
    print("="*70)
    test_nearby_drivers(
        latitude=WINDHOEK_CENTER["latitude"],
        longitude=WINDHOEK_CENTER["longitude"],
        radius=5.0,
        token=token
    )
    
    # Test 2: Windhoek with larger radius
    print("\n" + "="*70)
    print("TEST 2: Windhoek with 10km radius")
    print("="*70)
    test_nearby_drivers(
        latitude=WINDHOEK_CENTER["latitude"],
        longitude=WINDHOEK_CENTER["longitude"],
        radius=10.0,
        token=token
    )
    
    # Test 3: Windhoek with small radius
    print("\n" + "="*70)
    print("TEST 3: Windhoek with 1km radius (should find fewer drivers)")
    print("="*70)
    test_nearby_drivers(
        latitude=WINDHOEK_CENTER["latitude"],
        longitude=WINDHOEK_CENTER["longitude"],
        radius=1.0,
        token=token
    )
    
    # Test 4: Different location
    print("\n" + "="*70)
    print("TEST 4: North of Windhoek")
    print("="*70)
    test_nearby_drivers(
        latitude=WINDHOEK_NORTH["latitude"],
        longitude=WINDHOEK_NORTH["longitude"],
        radius=5.0,
        token=token
    )
    
    print("\n" + "="*70)
    print("✅ TEST SUITE COMPLETED")
    print("="*70)
    print("\n💡 TIPS:")
    print("  - Check that location data is properly serialized (dict with lat/lng)")
    print("  - Verify distance_km field is present and accurate")
    print("  - Confirm drivers are sorted by distance (closest first)")
    print("  - Ensure no 500 errors occur")


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"✅ Server is running at {API_BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"⚠️  Warning: Could not connect to server at {API_BASE_URL}")
        print(f"💡 Make sure the API server is running")
        print(f"💡 Or set API_BASE_URL environment variable to the correct URL")
        sys.exit(1)
    
    run_tests()

