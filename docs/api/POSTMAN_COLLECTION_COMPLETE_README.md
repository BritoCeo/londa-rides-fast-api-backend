# Londa Rides - Complete API Collection

This Postman collection covers the current FastAPI implementation for authentication, rides, drivers, subscriptions, payments, analytics, notifications, and admin endpoints.

## Collection Overview

### Environment Variables
The collection uses these variables:

- `base_url`: `http://localhost:8000`
- `api_base`: `{{base_url}}/api/v1`
- `auth_token`: bearer token used for protected requests
- `user_id`: user id captured from user login flows
- `driver_id`: driver id captured from driver login flows
- `ride_id`: ride id captured from ride-related responses
- `session_info`: OTP session info captured from registration flows
- `child_id`: optional child profile id for parent child-management endpoints
- `notification_id`: optional notification id for notification read endpoints

## 🔐 Authentication Flow

### 1. User Registration (Send OTP)
```bash
POST /api/v1/registration
{
  "phone_number": "+264813442539"
}
```

### 2. Verify OTP & Login
```bash
# User flow
POST /api/v1/verify-otp
{
  "phone_number": "+264813442539",
  "otp": "123456",
  "sessionInfo": "session_xxx"
}

# Driver flow
POST /api/v1/driver/verify-otp
{
  "phone_number": "+264813442540",
  "otp": "123456",
  "sessionInfo": "session_xxx"
}
```

Important: the API returns `accessToken`. In production, exchange Firebase custom tokens for ID tokens before making protected requests.

### 3. Refresh Token
```bash
POST /api/v1/refresh-token
Headers: Authorization: Bearer <expired_or_valid_token>
```

No request body is required.

## 📱 API Categories

### 1. Authentication APIs
- User registration and OTP verification
- Driver registration and OTP verification
- User and driver login
- Refresh token
- Current profile endpoints

### 2. User Management APIs
- Create user account
- Get current user profile
- Update user profile and location

### 3. Driver Management APIs
- Create driver account
- Get driver profile
- Update driver status and location
- Document upload, document metadata, and vehicle endpoints

### 4. Ride APIs
- Ride request, cancellation, status, rating, history, and nearby drivers
- Driver accept, decline, start, complete, messaging, breakdown, and route optimization
- Ride messaging, scheduled rides, carpool, SOS, tracking share, and stop management

### 5. Subscription APIs
- Driver subscription create, read, update, delete, payment, and history
- Parent subscription create, read, update, cancel, usage, and child profile management

### 6. Payment APIs
- Fare calculation
- Ride payment processing
- Payment history
- Monthly subscription payment

### 7. Notifications, Analytics, and Admin APIs
- Notifications inbox and mark-as-read
- User and driver analytics
- Admin login, platform monitoring, driver status updates, and financial reporting

## Quick Start Guide

### Step 1: Set Up Environment
1. Import the collection into Postman
2. Set `base_url` to `http://localhost:8000` for local work or your deployed host for remote testing
3. Start the API with `c:/MyProjects/londa-apis/venv/Scripts/python.exe run.py` or your preferred FastAPI entrypoint

### Step 2: User Authentication
1. Call `Register User (Send OTP)` with your phone number
2. Copy the `sessionInfo` from the response
3. Call `Verify OTP (Login)` or `User Login` with the OTP and `sessionInfo`
4. The collection automatically stores `auth_token` and `user_id` from the response

### Step 3: Driver Authentication
1. Call `Driver Send OTP`
2. Call `Driver Verify OTP` or `Driver Login`
3. The collection stores `auth_token` and `driver_id` from the driver response
4. Run driver-only requests after a driver login so `auth_token` represents a driver token

### Step 4: Test Ride Booking
1. Call `Request Ride` with pickup and dropoff locations
2. Save the returned `ride_id` if it is not auto-saved by the request script
3. Test other ride-related APIs

### Step 5: Test Driver Subscription
1. Ensure you have a valid driver authentication token
2. Call `Create Driver Subscription`
3. Test subscription management APIs

Important: protected endpoints generally extract the acting `user_id` or `driver_id` from the bearer token. Only send ids when the route explicitly uses a path or query parameter.

## Request Examples

### **Request Ride Example**
```json
{
  "pickup_location": {
    "latitude": -22.5609,
    "longitude": 17.0658,
    "name": "Windhoek Central"
  },
  "dropoff_location": {
    "latitude": -22.5709,
    "longitude": 17.0758,
    "name": "University of Namibia"
  },
  "ride_type": "standard",
  "estimated_fare": 13.00,
  "passengerCount": 1
}
```

### Driver Subscription Example
```json
{
  "payment_method": "cash"
}
```

### Refresh Token Example
No body is required. Send only the bearer token.

## Troubleshooting

### Common Issues

1. **"Invalid token"**: Use the refresh token API to get a new token
2. **"User not found"**: Confirm you authenticated with the correct account before calling protected endpoints
3. **"Driver not authenticated"**: Re-run a driver login flow so `auth_token` contains a driver token
4. **"Missing required fields"**: Check that all required fields are included in the request body

### Token Management
- The collection uses a single `auth_token` variable
- User flows overwrite `auth_token` with a user token
- Driver flows overwrite `auth_token` with a driver token
- Use `refresh-token` when tokens expire

## Response Formats

### **Success Response:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### **Error Response:**
```json
{
  "success": false,
  "message": "Error description",
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error message"
  }
}
```

## Namibian Phone Numbers
All examples use Namibian phone numbers in the format `+264XXXXXXXXX`. Update the phone numbers in the requests to match your test data.

## Payment Methods
The system currently supports **cash-only** payments. All payment_method fields should be set to "cash".

## Date Formats
Driver subscription APIs return dates in ISO 8601 format: `YYYYMMDDTHHMMSS+0000`

Example: `"startDate": "20251020T213810+0000"`

---

**Note**: This collection targets the FastAPI application in this repository. Make sure the API is running before executing the requests.
