"""
Script to update Postman collection with correct request bodies and authentication
"""
import json
import sys

# Load the collection
with open('postmancollection/Londa_Rides_Detailed_API_Collection.postman_collection.json', 'r', encoding='utf-8') as f:
    collection = json.load(f)

# Define public endpoints (no auth required)
PUBLIC_ENDPOINTS = [
    '/registration',
    '/verify-otp',
    '/request-email-otp',
    '/verify-email-otp',
    '/driver/send-otp',
    '/driver/verify-otp',
    '/health',
    '/test'
]

# Define request body templates based on actual schemas
REQUEST_BODIES = {
    '/registration': {
        "phone_number": "{{test_phone}}"
    },
    '/verify-otp': {
        "phone_number": "{{test_phone}}",
        "otp": "123456",
        "sessionInfo": "{{session_info}}"
    },
    '/request-email-otp': {
        "email": "{{test_email}}"
    },
    '/verify-email-otp': {
        "email": "{{test_email}}",
        "otp": "123456"
    },
    '/create-account': {
        "phone_number": "{{test_phone}}",
        "email": "{{test_email}}",
        "name": "Test User",
        "userType": "student"
    },
    '/request-ride': {
        "user_id": "{{user_id}}",
        "pickup_location": {
            "latitude": -22.5700,
            "longitude": 17.0836,
            "name": "Windhoek City Center",
            "address": "Independence Ave, Windhoek"
        },
        "dropoff_location": {
            "latitude": -22.5800,
            "longitude": 17.0900,
            "name": "University of Namibia",
            "address": "Pionierspark, Windhoek"
        },
        "ride_type": "standard",
        "estimated_fare": 13.00,
        "passengerCount": 1
    },
    '/cancel-ride': {
        "ride_id": "{{ride_id}}",
        "user_id": "{{user_id}}",
        "reason": "Changed my mind"
    },
    '/rate-ride': {
        "ride_id": "{{ride_id}}",
        "user_id": "{{user_id}}",
        "rating": 5,
        "review": "Great ride!"
    },
    '/driver/send-otp': {
        "phone_number": "{{test_phone}}"
    },
    '/driver/verify-otp': {
        "phone_number": "{{test_phone}}",
        "otp": "123456",
        "sessionInfo": "{{session_info}}"
    },
    '/driver/create-account': {
        "phone_number": "{{test_phone}}",
        "email": "{{test_email}}",
        "name": "Test Driver",
        "license_number": "DL123456",
        "vehicle_model": "Toyota Corolla",
        "vehicle_plate": "ABC-123",
        "vehicle_color": "White"
    },
    '/driver/update-status': {
        "status": "online"
    },
    '/driver/update-location': {
        "latitude": -22.5700,
        "longitude": 17.0836,
        "status": "online"
    },
    '/driver/rides/accept': {
        "rideId": "{{ride_id}}"
    },
    '/driver/rides/decline': {
        "rideId": "{{ride_id}}",
        "reason": "Too far"
    },
    '/driver/rides/start': {
        "rideId": "{{ride_id}}"
    },
    '/driver/rides/complete': {
        "rideId": "{{ride_id}}",
        "final_fare": 13.00
    },
    '/driver/subscriptions': {
        "driver_id": "{{driver_id}}",
        "payment_method": "cash"
    },
    '/driver/subscriptions/update': {
        "auto_renew": True,
        "payment_method": "cash"
    },
    '/driver/subscriptions/payment': {
        "driver_id": "{{driver_id}}",
        "payment_method": "cash",
        "amount": 150.00
    },
    '/parent/subscriptions': {
        "user_id": "{{user_id}}",
        "payment_method": "cash",
        "children_profiles": [
            {
                "child_name": "John Doe",
                "child_age": 10,
                "school_name": "Windhoek Primary School",
                "pickup_address": "123 Main St, Windhoek",
                "dropoff_address": "456 School Rd, Windhoek",
                "emergency_contact": {
                    "name": "Jane Doe",
                    "phone": "+264813442530"
                }
            }
        ]
    },
    '/parent/subscriptions/update': {
        "user_id": "{{user_id}}",
        "auto_renew": True
    },
    '/parent/subscriptions/cancel': {
        "user_id": "{{user_id}}",
        "reason": "No longer needed"
    },
    '/parent/subscriptions/children': {
        "user_id": "{{user_id}}",
        "child_name": "John Doe",
        "child_age": 10,
        "school_name": "Windhoek Primary School",
        "pickup_address": "123 Main St, Windhoek",
        "dropoff_address": "456 School Rd, Windhoek",
        "emergency_contact": {
            "name": "Jane Doe",
            "phone": "+264813442530"
        }
    },
    '/payments/calculate-fare': {
        "pickup_location": {
            "latitude": -22.5700,
            "longitude": 17.0836
        },
        "dropoff_location": {
            "latitude": -22.5800,
            "longitude": 17.0900
        },
        "ride_type": "standard"
    },
    '/payments/process': {
        "ride_id": "{{ride_id}}",
        "user_id": "{{user_id}}",
        "amount": 13.00,
        "payment_method": "cash"
    },
    '/update-profile': {
        "name": "Updated Name",
        "email": "updated@example.com"
    },
    '/update-location': {
        "latitude": -22.5700,
        "longitude": 17.0836
    }
}

def update_endpoint_auth(item, path):
    """Update authentication for an endpoint"""
    # Check if this is a public endpoint
    is_public = any(path.endswith(ep) for ep in PUBLIC_ENDPOINTS)
    
    if is_public:
        # Remove auth (set to noauth)
        if 'request' in item:
            item['request']['auth'] = {"type": "noauth"}
    else:
        # Ensure Bearer auth is set
        if 'request' in item:
            if 'auth' not in item['request'] or item['request'].get('auth', {}).get('type') != 'bearer':
                item['request']['auth'] = {
                    "type": "bearer",
                    "bearer": [
                        {
                            "key": "token",
                            "value": "{{auth_token}}",
                            "type": "string"
                        }
                    ]
                }

def update_request_body(item, path):
    """Update request body for an endpoint"""
    if 'request' not in item:
        return
    
    # Find matching request body
    body = None
    for endpoint, body_template in REQUEST_BODIES.items():
        if path.endswith(endpoint):
            body = body_template
            break
    
    if body and item['request'].get('method') in ['POST', 'PUT', 'PATCH']:
        # Update body
        item['request']['body'] = {
            "mode": "raw",
            "raw": json.dumps(body, indent=2),
            "options": {
                "raw": {
                    "language": "json"
                }
            }
        }
        
        # Ensure Content-Type header
        headers = item['request'].get('header', [])
        content_type_exists = any(h.get('key') == 'Content-Type' for h in headers)
        if not content_type_exists:
            headers.append({
                "key": "Content-Type",
                "value": "application/json"
            })
            item['request']['header'] = headers

def process_items(items, parent_path=""):
    """Recursively process all items in the collection"""
    for item in items:
        if 'item' in item:
            # This is a folder, process its children
            process_items(item['item'], parent_path)
        else:
            # This is an endpoint
            if 'request' in item and 'url' in item['request']:
                url = item['request']['url']
                if isinstance(url, dict) and 'path' in url:
                    path = '/' + '/'.join(url['path'])
                    full_path = parent_path + path
                    
                    # Update auth
                    update_endpoint_auth(item, full_path)
                    
                    # Update request body
                    update_request_body(item, full_path)

# Process the collection
if 'item' in collection:
    process_items(collection['item'])

# Save updated collection
with open('postmancollection/Londa_Rides_Detailed_API_Collection.postman_collection.json', 'w', encoding='utf-8') as f:
    json.dump(collection, f, indent=2, ensure_ascii=False)

print("Postman collection updated successfully!")
print("   - Updated authentication for all endpoints")
print("   - Updated request bodies to match API schemas")
print("   - Public endpoints set to noauth")
print("   - Protected endpoints use Bearer token")

