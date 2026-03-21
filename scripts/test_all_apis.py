import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test Data
TEST_PHONE = "+264811234567"
TEST_OTP = "123456"

# State
state = {
    "session_info": None,
    "auth_token": None,
    "user_id": None
}

def print_result(name, response):
    status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
    print(f"{status} | {name} ({response.status_code})")
    if response.status_code >= 400:
        print(f"   Response: {response.text}")

def test_health():
    print("\n--- 1. Health & Status ---")
    response = requests.get(f"{BASE_URL}/health")
    print_result("Health Check", response)
    
    response = requests.get(f"{BASE_URL}/test")
    print_result("API Test", response)

def test_auth():
    print("\n--- 2. User Authentication ---")
    # 1. Register / Send OTP
    response = requests.post(f"{API_BASE}/registration", json={"phone_number": TEST_PHONE})
    print_result("Register User", response)
    if response.status_code == 201:
        state["session_info"] = response.json().get("data", {}).get("sessionInfo")

    # 2. Verify OTP
    if state["session_info"]:
        payload = {
            "phone_number": TEST_PHONE,
            "otp": TEST_OTP,
            "sessionInfo": state["session_info"]
        }
        response = requests.post(f"{API_BASE}/verify-otp", json=payload)
        print_result("Verify OTP", response)
        if response.status_code == 200:
            state["auth_token"] = response.json().get("data", {}).get("accessToken")
            print(f"   [Token Acquired]: {state['auth_token'][:20]}...")

def test_user_profile():
    print("\n--- 3. User Profile ---")
    if not state["auth_token"]:
        print("⏭️ SKIP | User Profile Test (No Auth Token)")
        return

    headers = {"Authorization": f"Bearer {state['auth_token']}"}
    response = requests.get(f"{API_BASE}/me", headers=headers)
    print_result("Get Current User Profile", response)

def test_rides():
    print("\n--- 4. Ride Management ---")
    if not state["auth_token"]:
        print("⏭️ SKIP | Ride Tests (No Auth Token)")
        return

    headers = {"Authorization": f"Bearer {state['auth_token']}"}
    
    # Get Nearby Drivers
    params = {"latitude": -22.5700, "longitude": 17.0836, "radius": 5}
    response = requests.get(f"{API_BASE}/nearby-drivers", headers=headers, params=params)
    print_result("Get Nearby Drivers", response)

    # Request Ride
    payload = {
        "pickup_location": {
            "latitude": -22.5700, "longitude": 17.0836,
            "name": "Windhoek City Center", "address": "Independence Ave"
        },
        "dropoff_location": {
            "latitude": -22.5800, "longitude": 17.0900,
            "name": "University of Namibia", "address": "Pionierspark"
        },
        "ride_type": "standard",
        "estimated_fare": 13.00,
        "passengerCount": 1
    }
    response = requests.post(f"{API_BASE}/request-ride", headers=headers, json=payload)
    print_result("Request Ride", response)

def main():
    print("🚀 Starting API Tests...")
    try:
        test_health()
        test_auth()
        test_user_profile()
        test_rides()
        print("\n🎉 Test Run Completed!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API. Make sure the server is running on", BASE_URL)

if __name__ == "__main__":
    main()
