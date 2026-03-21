import requests
import json

BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api/v1"

TEST_USER_PHONE = "+264811234567"
TEST_DRIVER_PHONE = "+264817654321"
TEST_OTP = "123456"

state = {
    "user_token": None,
    "driver_token": None,
    "ride_id": None
}

def print_result(name, response):
    status = "PASS" if response.status_code < 400 else "FAIL"
    print(f"{status} | {name} ({response.status_code})")
    if response.status_code >= 400:
        print(f"   Response: {response.text}")

def authenticate():
    print("\n--- Authentication ---")
    # User Auth
    res = requests.post(f"{API_BASE}/registration", json={"phone_number": TEST_USER_PHONE})
    if res.status_code == 201:
        session_info = res.json().get("data", {}).get("sessionInfo")
        if session_info:
            res_verify = requests.post(f"{API_BASE}/verify-otp", json={
                "phone_number": TEST_USER_PHONE, "otp": TEST_OTP, "sessionInfo": session_info
            })
            if res_verify.status_code == 200:
                state["user_token"] = res_verify.json().get("data", {}).get("accessToken")
                print("PASS | User Auth")
    
    # Driver Auth
    res_driver = requests.post(f"{API_BASE}/driver/send-otp", json={"phone_number": TEST_DRIVER_PHONE})
    if res_driver.status_code == 200:
        d_session_info = res_driver.json().get("data", {}).get("sessionInfo")
        if d_session_info:
            res_d_verify = requests.post(f"{API_BASE}/driver/verify-otp", json={
                "phone_number": TEST_DRIVER_PHONE, "otp": TEST_OTP, "sessionInfo": d_session_info
            })
            if res_d_verify.status_code == 200:
                state["driver_token"] = res_d_verify.json().get("data", {}).get("accessToken")
                print("PASS | Driver Auth")

def test_safety_apis():
    print("\n--- Testing Safety APIs (User) ---")
    if not state["user_token"]:
        print("SKIP | Safety Tests (No User Auth)")
        return
        
    headers = {"Authorization": f"Bearer {state['user_token']}"}
    
    # 1. Create a ride first to test with
    ride_payload = {
        "pickup_location": {"latitude": -22.5700, "longitude": 17.0836, "name": "Pickup"},
        "dropoff_location": {"latitude": -22.5800, "longitude": 17.0900, "name": "Dropoff"},
        "ride_type": "standard",
        "estimated_fare": 13.00,
        "passengerCount": 1
    }
    ride_res = requests.post(f"{API_BASE}/request-ride", headers=headers, json=ride_payload)
    if ride_res.status_code == 201:
        state["ride_id"] = ride_res.json().get("data", {}).get("id")
        print(f"PASS | Create Test Ride (ID: {state['ride_id']})")
    
    if not state["ride_id"]:
        print("SKIP | Safety Tests (No Ride ID)")
        return
        
    # 2. Test SOS
    sos_payload = {"location": {"latitude": -22.5750, "longitude": 17.0850}, "reason": "Test emergency"}
    sos_res = requests.post(f"{API_BASE}/ride/{state['ride_id']}/sos", headers=headers, json=sos_payload)
    print_result("SOS Alert", sos_res)
    
    # 3. Test Share Tracking
    track_res = requests.post(f"{API_BASE}/ride/{state['ride_id']}/share-tracking", headers=headers, json={"duration_minutes": 60})
    print_result("Share Tracking", track_res)

def test_driver_vetting_apis():
    print("\n--- Testing Driver Vetting APIs (Driver) ---")
    if not state["driver_token"]:
        print("SKIP | Driver Tests (No Driver Auth)")
        return
        
    headers = {"Authorization": f"Bearer {state['driver_token']}"}
    
    # Optional: ensure driver exists by creating profile if doesn't
    # In many setups, if GET /me fails, we need to create account. We will skip deep setup and just try the endpoints.
    
    # 1. Update Vehicle
    veh_payload = {"vehicle_make": "Toyota", "vehicle_model": "Corolla", "vehicle_color": "White", "vehicle_plate": "N1234W"}
    veh_res = requests.put(f"{API_BASE}/driver/vehicle", headers=headers, json=veh_payload)
    print_result("Update Vehicle Details", veh_res)
    
    # 2. Get Vehicle
    veh_get = requests.get(f"{API_BASE}/driver/vehicle", headers=headers)
    print_result("Get Vehicle Details", veh_get)
    
    # 3. Upload Document Metadata
    doc_payload = {
        "document_type": "drivers_license",
        "document_url": "https://res.cloudinary.com/demo/image/upload/sample.jpg",
        "notes": "Valid until 2030"
    }
    doc_res = requests.post(f"{API_BASE}/driver/documents/metadata", headers=headers, json=doc_payload)
    print_result("Upload Document Metadata", doc_res)

def main():
    print("Starting Test for new SRS APIs...")
    try:
        authenticate()
        test_safety_apis()
        test_driver_vetting_apis()
        print("\nTest Run Completed!")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
