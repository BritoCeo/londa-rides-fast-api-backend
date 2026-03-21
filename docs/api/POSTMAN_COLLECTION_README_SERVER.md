# Londa Rides API Collection - Postman Testing Guide

## Overview

Use `postmancollection/Londa_Rides_API_Collection_Complete.postman_collection.json` to test the current FastAPI backend in this repository.

## Setup

### 1. Import the Collection
1. Open Postman.
2. Import `postmancollection/Londa_Rides_API_Collection_Complete.postman_collection.json`.

### 2. Collection Variables
The collection uses these variables:
- `base_url`: defaults to `http://localhost:8000`
- `api_base`: `{{base_url}}/api/v1`
- `auth_token`: bearer token used for protected requests
- `user_id`
- `driver_id`
- `ride_id`
- `session_info`
- `child_id`
- `notification_id`

### 3. Run the API
Start the FastAPI application from the workspace root:
```bash
c:/MyProjects/londa-apis/venv/Scripts/python.exe run.py
```

## Recommended Testing Flow

### 1. Basic Health Check
1. `GET /health`
2. `GET /test`

### 2. User Authentication Flow
1. `POST /api/v1/registration`
2. `POST /api/v1/verify-otp`
3. `POST /api/v1/create-account`
4. `GET /api/v1/me`

### 3. Driver Authentication Flow
1. `POST /api/v1/driver/send-otp`
2. `POST /api/v1/driver/verify-otp`
3. `POST /api/v1/driver/create-account`
4. `GET /api/v1/driver/me`

### 4. Ride Flow
1. `POST /api/v1/request-ride`
2. `GET /api/v1/nearby-drivers`
3. `POST /api/v1/driver/accept-ride`
4. `POST /api/v1/driver/start-ride`
5. `POST /api/v1/driver/complete-ride`
6. `PUT /api/v1/rate-ride`

## Authentication Notes

1. The collection stores the latest token in `auth_token`.
2. User login requests set `auth_token` for user endpoints.
3. Driver login requests overwrite `auth_token` for driver endpoints.
4. In production, Firebase custom tokens should be exchanged for ID tokens before protected calls.

## Example Requests

### User Registration
```json
{
  "phone_number": "+264811234567"
}
```

### Driver Subscription Payment
```json
{
  "payment_method": "cash",
  "amount": 150.0
}
```

### Ride Request
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
  "estimated_fare": 13.0,
  "passengerCount": 1
}
```

## Notes

1. Payment examples in this codebase are cash-only unless a route explicitly changes that behavior.
2. Protected endpoints usually derive the acting user or driver id from the bearer token.
3. Use the verification and README files in `docs/api` alongside the collection when updating or testing endpoints.

## 🚨 Error Handling

The collection includes proper error handling for:
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **409 Conflict**: Duplicate resources
- **500 Internal Server Error**: Server errors

## 📊 Response Examples

### **Success Response**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data
  }
}
```

### **Error Response**
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

## 🔧 Environment Configuration

### **Development**
- `base_url`: `http://localhost:8000`
- `auth_token`: Set after login
- `user_id`: Set after user creation
- `driver_id`: Set after driver registration
- `ride_id`: Set after ride creation

### **Production**
- `base_url`: `https://api.londarides.com`
- Update all variables accordingly

## 📈 Testing Tips

1. **Start with Health Check**: Always test `/health` first
2. **Authentication First**: Complete auth flow before testing other APIs
3. **Driver Subscription**: Test the new subscription APIs thoroughly
4. **Complete Workflows**: Test end-to-end ride flows
5. **Error Scenarios**: Test with invalid data to verify error handling
6. **Performance**: Monitor response times during testing

## 🎉 Ready to Test!

The Postman collection is now ready for comprehensive testing of the Londa Rides CC platform. All APIs are organized, documented, and ready for use! 🚀
