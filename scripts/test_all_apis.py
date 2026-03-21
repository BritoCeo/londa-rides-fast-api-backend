import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8004"
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
    
    # Send OTP
    payload = {"phone_number": TEST_PHONE}
    response = requests.post(f"{API_BASE}/registration", json=payload)
    print_result("Register User", response)
    
    if response.status_code == 201:
        state["session_info"] = response.json().get("data", {}).get("sessionInfo")
    
    # Verify OTP
    if state["session_info"]:
        payload = {
            "phone_number": TEST_PHONE,
            "otp": TEST_OTP,
            "sessionInfo": state["session_info"]
        }
        response = requests.post(f"{API_BASE}/verify-otp", json=payload)
        print_result("Verify OTP", response)
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            state["auth_token"] = data.get("accessToken")
            state["user_id"] = data.get("user", {}).get("id")
            print(f"   [Token Acquired]: {state['auth_token'][:20]}...")

def test_user_profile():
    print("\n--- 3. User Profile ---")
    if not state["auth_token"]:
        print("⏭️ Skipping user profile tests (no auth token)")
        return
        
    headers = {"Authorization": f"Bearer {state['auth_token']}"}
    
    # Get Profile
    response = requests.get(f"{API_BASE}/me", headers=headers)
    print_result("Get Current User Profile", response)

def test_rides():
    print("\n--- 4. Ride Management ---")
    if not state["auth_token"]:
        print("⏭️ Skipping ride tests (no auth token)")
        return
        
    headers = {"Authorization": f"Bearer {state['auth_token']}"}
    
    # Nearby Drivers
    response = requests.get(f"{API_BASE}/nearby-drivers?latitude=-22.5609&longitude=17.0658", headers=headers)
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

def test_support_promotions_and_ratings():
    print("\n--- 5. Additional Features ---")
    headers = {"Authorization": f"Bearer {state.get('auth_token', '')}"}
    
    # 1. Promotions
    payload = {"code": "STUDENT2025"}
    response = requests.post(f"{API_BASE}/promotions/apply", headers=headers, json=payload)
    print_result("Apply Promotion", response)
    
    response = requests.get(f"{API_BASE}/referral/code", headers=headers)
    print_result("Get Referral Code", response)

    # 2. Support
    payload = {
        "ride_id": "test_ride_123",
        "issue_type": "driver_behavior",
        "description": "Driver was rude and drove recklessly",
        "role": "rider"
    }
    # Note: this will fail with 400 because test_ride_123 doesn't exist, which is expected
    response = requests.post(f"{API_BASE}/support/ticket", headers=headers, json=payload)
    print_result("Create Support Ticket", response)

    response = requests.get(f"{API_BASE}/support/tickets", headers=headers)
    print_result("Get Support Tickets", response)

    # 3. Ratings (Public endpoint)
    response = requests.get(f"{API_BASE}/driver/test_driver_123/reviews", headers=headers)
    print_result("Get Driver Reviews", response)

def main():
    print("Starting API Tests...")
    try:
        test_health()
        test_auth()
        test_user_profile()
        test_rides()
        
        # New Tests
        test_support_promotions_and_ratings()
        
        print("\n🎉 Test Run Completed!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API. Make sure the server is running on", BASE_URL)

if __name__ == "__main__":
    main()
