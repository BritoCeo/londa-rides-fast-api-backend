# 📱 Londa Rides API - Complete Documentation

**Version:** 1.0.0  
**Last Updated:** December 31, 2024  
**Base URL:** `http://localhost:8000/api/v1` (Development)  
**Production URL:** `https://api.londarides.com/api/v1` (Production)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Response Format](#response-format)
3. [Error Handling](#error-handling)
4. [User Authentication APIs](#1-user-authentication-apis)
   - 1.1 Register User (Send OTP)
   - 1.2 Verify OTP (Login)
   - 1.3 Request Email OTP
   - 1.4 Verify Email OTP
   - 1.5 Create User Account
   - 1.6 Refresh Token
5. [User Profile APIs](#2-user-profile-apis)
6. [Ride Management APIs (User)](#3-ride-management-apis-user)
7. [Driver Authentication APIs](#4-driver-authentication-apis)
8. [Driver Profile APIs](#5-driver-profile-apis)
9. [Driver Ride Management APIs](#6-driver-ride-management-apis)
10. [Driver Subscription APIs](#7-driver-subscription-apis)
11. [Parent Subscription APIs](#8-parent-subscription-apis)
12. [Payment APIs](#9-payment-apis)
13. [Analytics APIs](#10-analytics-apis)
14. [Health Check APIs](#11-health-check-apis)

---

## 🔐 Authentication

Most endpoints require authentication using Firebase ID tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_firebase_id_token>
```

**How to get the token:**
1. User/Driver registers via phone number (sends OTP)
2. User/Driver verifies OTP
3. API returns `accessToken` in the response
4. Use this token for all subsequent authenticated requests

**Note:** The token is a Firebase custom token that should be exchanged for an ID token using the Firebase SDK on the client side before making API calls.

---

## 📤 Response Format

### Success Response

All successful API responses follow this format:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {
    // Response data here
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

### Error Response

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error description",
  "error": {
    "code": "ERROR_CODE",
    "details": {}
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## ⚠️ Error Handling

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

---

## 1. User Authentication APIs

### 1.1 Register User (Send OTP)

**Endpoint:** `POST /api/v1/registration`  
**Authentication:** Not required  
**Description:** Sends an OTP to the user's phone number for registration/login.

#### Request Body

```json
{
  "phone_number": "+264813442530"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format (must start with +) |

#### Response (201 Created)

```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "sessionInfo": "AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `sessionInfo` | string | Session information needed for OTP verification |

---

### 1.2 Verify OTP (Login)

**Endpoint:** `POST /api/v1/verify-otp`  
**Authentication:** Not required  
**Description:** Verifies the OTP sent to the user's phone and returns an access token.

#### Request Body

```json
{
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format |
| `otp` | string | Yes | OTP code (4-6 digits) |
| `sessionInfo` | string | No | Session info from registration response |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "zdXCHy7je3OaOVC4qHwS",
      "phone_number": "+264813442530",
      "email": null,
      "name": null,
      "userType": null,
      "createdAt": "2024-12-31T19:00:00.000000",
      "updatedAt": "2024-12-31T19:00:00.000000"
    }
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `accessToken` | string | Firebase custom token (exchange for ID token on client) |
| `user` | object | User profile data |

---

### 1.3 Request Email OTP

**Endpoint:** `POST /api/v1/email-otp-request`  
**Authentication:** Not required  
**Description:** Sends an OTP to the user's email address.

#### Request Body

```json
{
  "email": "user@example.com"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "OTP sent to email successfully",
  "data": {
    "sessionInfo": "email_session_123"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 1.4 Verify Email OTP

**Endpoint:** `PUT /api/v1/email-otp-verify`  
**Authentication:** Not required  
**Description:** Verifies the OTP sent to the user's email.

#### Request Body

```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Email address |
| `otp` | string | Yes | OTP code (4-6 digits) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Email verified successfully",
  "data": null,
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 1.5 Create User Account

**Endpoint:** `POST /api/v1/create-account`  
**Authentication:** Required (Bearer token)  
**Description:** Creates a complete user account after OTP verification. This endpoint completes the user profile.

#### Request Body

```json
{
  "phone_number": "+264813442530",
  "email": "user@example.com",
  "name": "John Doe",
  "userType": "student"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format |
| `email` | string | No | Email address |
| `name` | string | Yes | User's full name (1-100 characters) |
| `userType` | string | Yes | User type: `student`, `worker`, or `parent` |

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Account created successfully",
  "data": {
    "id": "zdXCHy7je3OaOVC4qHwS",
    "phone_number": "+264813442530",
    "email": "user@example.com",
    "name": "John Doe",
    "userType": "student",
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 1.6 Refresh Token

**Endpoint:** `POST /api/v1/refresh-token`  
**Authentication:** Required (Bearer token - can be expired)  
**Description:** Refreshes an expired or valid authentication token. Accepts Firebase ID tokens or custom tokens (even if expired), verifies the user exists, and returns a new custom token. Works for both users and drivers.

#### Request Headers

```
Authorization: Bearer <your_token>
```

**Note:** The token can be expired. The endpoint will decode it to extract user information and generate a new token.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "zdXCHy7je3OaOVC4qHwS",
      "phone_number": "+264813442530",
      "email": "user@example.com",
      "name": "John Doe",
      "userType": "student",
      "createdAt": "2024-12-31T19:00:00.000000",
      "updatedAt": "2024-12-31T19:00:00.000000"
    }
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `accessToken` | string | New Firebase custom token (exchange for ID token on client) |
| `user` | object | User profile data (or driver data if user is a driver) |

#### Error Responses

**401 Unauthorized - Invalid Token:**
```json
{
  "success": false,
  "message": "Invalid token format",
  "error": {
    "code": "UNAUTHORIZED",
    "details": {}
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

**401 Unauthorized - User Not Found:**
```json
{
  "success": false,
  "message": "User not found. Please re-authenticate.",
  "error": {
    "code": "UNAUTHORIZED",
    "details": {}
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Usage Notes

- **Token Expiration:** Firebase ID tokens expire after 1 hour. Use this endpoint to refresh expired tokens without requiring re-authentication.
- **Client-Side:** After receiving the new `accessToken`, exchange it for an ID token using the Firebase SDK on the client side.
- **Automatic Refresh:** The Firebase SDK can automatically refresh tokens, but this endpoint provides a server-side refresh option.
- **Unified Endpoint:** Works for both users and drivers - the endpoint automatically detects the user type.

---

## 2. User Profile APIs

### 2.1 Get Current User Profile

**Endpoint:** `GET /api/v1/me`  
**Authentication:** Required (Bearer token)  
**Description:** Retrieves the profile data of the currently logged-in user.

#### Request Headers

```
Authorization: Bearer <your_token>
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "User profile retrieved successfully",
  "data": {
    "id": "zdXCHy7je3OaOVC4qHwS",
    "phone_number": "+264813442530",
    "email": "user@example.com",
    "name": "John Doe",
    "userType": "student",
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 2.2 Update User Profile

**Endpoint:** `PUT /api/v1/update-profile`  
**Authentication:** Required (Bearer token)  
**Description:** Updates the user's profile information.

#### Request Body

```json
{
  "name": "John Smith",
  "email": "newemail@example.com"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | User's full name (1-100 characters) |
| `email` | string | No | Email address |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": "zdXCHy7je3OaOVC4qHwS",
    "phone_number": "+264813442530",
    "email": "newemail@example.com",
    "name": "John Smith",
    "userType": "student",
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:05:00.000000"
  },
  "timestamp": "2024-12-31T19:05:00.000000"
}
```

---

### 2.3 Update User Location

**Endpoint:** `POST /api/v1/update-location`  
**Authentication:** Required (Bearer token)  
**Description:** Updates the user's current location.

#### Request Body

```json
{
  "latitude": -22.5700,
  "longitude": 17.0836
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `latitude` | float | Yes | Latitude (-90 to 90) |
| `longitude` | float | Yes | Longitude (-180 to 180) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Location updated successfully",
  "data": null,
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 3. Ride Management APIs (User)

### 3.1 Request Ride

**Endpoint:** `POST /api/v1/request-ride`  
**Authentication:** Required (Bearer token)  
**Description:** Creates a new ride request. The user ID is automatically obtained from the authentication token.

#### Request Body

```json
{
  "pickup_location": {
    "latitude": -22.5700,
    "longitude": 17.0836,
    "name": "Pickup Point",
    "address": "123 Main Street, Windhoek"
  },
  "dropoff_location": {
    "latitude": -22.5800,
    "longitude": 17.0900,
    "name": "Dropoff Point",
    "address": "456 Oak Avenue, Windhoek"
  },
  "ride_type": "standard",
  "estimated_fare": 13.00,
  "passengerCount": 1
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pickup_location` | object | Yes | Pickup location details |
| `pickup_location.latitude` | float | Yes | Latitude (-90 to 90) |
| `pickup_location.longitude` | float | Yes | Longitude (-180 to 180) |
| `pickup_location.name` | string | No | Location name |
| `pickup_location.address` | string | No | Full address |
| `dropoff_location` | object | Yes | Dropoff location details |
| `dropoff_location.latitude` | float | Yes | Latitude (-90 to 90) |
| `dropoff_location.longitude` | float | Yes | Longitude (-180 to 180) |
| `dropoff_location.name` | string | No | Location name |
| `dropoff_location.address` | string | No | Full address |
| `ride_type` | string | No | Ride type (default: "standard") |
| `estimated_fare` | float | No | Estimated fare in NAD (default: 13.00) |
| `passengerCount` | integer | No | Number of passengers (1-8, default: 1) |

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Ride requested successfully",
  "data": {
    "id": "ride_123456789",
    "userId": "zdXCHy7je3OaOVC4qHwS",
    "driverId": null,
    "pickupLocation": {
      "latitude": -22.5700,
      "longitude": 17.0836,
      "name": "Pickup Point",
      "address": "123 Main Street, Windhoek"
    },
    "dropoffLocation": {
      "latitude": -22.5800,
      "longitude": 17.0900,
      "name": "Dropoff Point",
      "address": "456 Oak Avenue, Windhoek"
    },
    "status": "pending",
    "rideType": "standard",
    "estimatedFare": 13.00,
    "finalFare": null,
    "passengerCount": 1,
    "rating": null,
    "review": null,
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000",
    "expiresAt": "2024-12-31T19:10:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 3.2 Get Nearby Drivers

**Endpoint:** `GET /api/v1/nearby-drivers`  
**Authentication:** Required (Bearer token)  
**Description:** Finds available drivers near the user's location.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `latitude` | float | Yes | User's latitude |
| `longitude` | float | Yes | User's longitude |
| `radius` | float | No | Search radius in km (default: 5) |

#### Example Request

```
GET /api/v1/nearby-drivers?latitude=-22.5700&longitude=17.0836&radius=5.0
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Nearby drivers retrieved successfully",
  "data": {
    "drivers": [
      {
        "id": "driver_123",
        "name": "John Driver",
        "phone_number": "+264812345678",
        "status": "online",
        "location": {
          "latitude": -22.5710,
          "longitude": 17.0840
        },
        "vehicle": {
          "model": "Toyota Corolla",
          "plate": "ABC-123",
          "color": "White"
        }
      }
    ],
    "count": 1
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 3.3 Cancel Ride

**Endpoint:** `POST /api/v1/cancel-ride`  
**Authentication:** Required (Bearer token)  
**Description:** Cancels a ride request. The user ID is automatically obtained from the authentication token.

#### Request Body

```json
{
  "ride_id": "ride_123456789",
  "reason": "Changed my mind"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ride_id` | string | Yes | Ride ID (cannot be empty) |
| `reason` | string | No | Cancellation reason |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride cancelled successfully",
  "data": {
    "id": "ride_123456789",
    "status": "cancelled",
    "updatedAt": "2024-12-31T19:05:00.000000"
  },
  "timestamp": "2024-12-31T19:05:00.000000"
}
```

---

### 3.4 Rate Ride

**Endpoint:** `PUT /api/v1/rate-ride`  
**Authentication:** Required (Bearer token)  
**Description:** Rates a completed ride. The user ID is automatically obtained from the authentication token.

#### Request Body

```json
{
  "ride_id": "ride_123456789",
  "rating": 5,
  "review": "Great driver, very professional!"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ride_id` | string | Yes | Ride ID (cannot be empty) |
| `rating` | integer | Yes | Rating from 1 to 5 |
| `review` | string | No | Review text (max 500 characters) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride rated successfully",
  "data": {
    "id": "ride_123456789",
    "rating": 5,
    "review": "Great driver, very professional!",
    "updatedAt": "2024-12-31T19:10:00.000000"
  },
  "timestamp": "2024-12-31T19:10:00.000000"
}
```

---

### 3.5 Get Ride Status

**Endpoint:** `GET /api/v1/ride-status/{ride_id}`  
**Authentication:** Required (Bearer token)  
**Description:** Gets the current status of a ride.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ride_id` | string | Yes | Ride ID |

#### Example Request

```
GET /api/v1/ride-status/ride_123456789
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride status retrieved successfully",
  "data": {
    "id": "ride_123456789",
    "userId": "zdXCHy7je3OaOVC4qHwS",
    "driverId": "driver_123",
    "status": "accepted",
    "pickupLocation": {
      "latitude": -22.5700,
      "longitude": 17.0836,
      "address": "123 Main Street, Windhoek"
    },
    "dropoffLocation": {
      "latitude": -22.5800,
      "longitude": 17.0900,
      "address": "456 Oak Avenue, Windhoek"
    },
    "estimatedFare": 13.00,
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:01:00.000000"
  },
  "timestamp": "2024-12-31T19:01:00.000000"
}
```

---

### 3.6 Get All User Rides

**Endpoint:** `GET /api/v1/get-rides`  
**Authentication:** Required (Bearer token)  
**Description:** Gets all rides for the logged-in user with pagination.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1, min: 1) |
| `limit` | integer | No | Items per page (default: 10, min: 1, max: 100) |

#### Example Request

```
GET /api/v1/get-rides?page=1&limit=10
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Rides retrieved successfully",
  "data": {
    "rides": [
      {
        "id": "ride_123456789",
        "userId": "zdXCHy7je3OaOVC4qHwS",
        "driverId": "driver_123",
        "status": "completed",
        "estimatedFare": 13.00,
        "finalFare": 13.00,
        "rating": 5,
        "createdAt": "2024-12-31T19:00:00.000000"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "hasMore": false
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 4. Driver Authentication APIs

### 4.1 Send Driver OTP

**Endpoint:** `POST /api/v1/driver/send-otp`  
**Authentication:** Not required  
**Description:** Sends an OTP to the driver's phone number for registration/login.

#### Request Body

```json
{
  "phone_number": "+264812345678"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "sessionInfo": "AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 4.2 Verify Driver OTP

**Endpoint:** `POST /api/v1/driver/verify-otp`  
**Authentication:** Not required  
**Description:** Verifies the OTP sent to the driver's phone and returns an access token.

#### Request Body

```json
{
  "phone_number": "+264812345678",
  "otp": "123456",
  "sessionInfo": "AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs"
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "driver_123",
      "phone_number": "+264812345678",
      "name": null,
      "status": "offline",
      "createdAt": "2024-12-31T19:00:00.000000"
    }
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 4.3 Driver Login

**Endpoint:** `POST /api/v1/driver/login`  
**Authentication:** Not required  
**Description:** Driver login with OTP (same as verify-otp, different endpoint name).

#### Request Body

```json
{
  "phone_number": "+264812345678",
  "otp": "123456",
  "sessionInfo": "AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs"
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver login successful",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "driver": {
      "id": "driver_123",
      "phone_number": "+264812345678",
      "name": "John Driver",
      "status": "offline"
    }
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 4.4 Create Driver Account

**Endpoint:** `POST /api/v1/driver/create-account`  
**Authentication:** Required (Bearer token)  
**Description:** Creates a complete driver account after OTP verification.

#### Request Body

```json
{
  "phone_number": "+264812345678",
  "email": "driver@example.com",
  "name": "John Driver",
  "license_number": "DL123456",
  "vehicle_model": "Toyota Corolla",
  "vehicle_plate": "ABC-123",
  "vehicle_color": "White"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format |
| `email` | string | No | Email address |
| `name` | string | Yes | Driver's full name (1-100 characters) |
| `license_number` | string | Yes | Driver's license number (1-50 characters) |
| `vehicle_model` | string | Yes | Vehicle model (1-100 characters) |
| `vehicle_plate` | string | Yes | Vehicle license plate (1-20 characters) |
| `vehicle_color` | string | Yes | Vehicle color (1-50 characters) |

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Driver account created successfully",
  "data": {
    "id": "driver_123",
    "phone_number": "+264812345678",
    "email": "driver@example.com",
    "name": "John Driver",
    "license_number": "DL123456",
    "vehicle_model": "Toyota Corolla",
    "vehicle_plate": "ABC-123",
    "vehicle_color": "White",
    "status": "offline",
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 5. Driver Profile APIs

### 5.1 Get Current Driver Profile

**Endpoint:** `GET /api/v1/driver/me`  
**Authentication:** Required (Bearer token)  
**Description:** Retrieves the profile data of the currently logged-in driver.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver profile retrieved successfully",
  "data": {
    "id": "driver_123",
    "phone_number": "+264812345678",
    "email": "driver@example.com",
    "name": "John Driver",
    "license_number": "DL123456",
    "vehicle_model": "Toyota Corolla",
    "vehicle_plate": "ABC-123",
    "vehicle_color": "White",
    "status": "online",
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 5.2 Update Driver Status

**Endpoint:** `PUT /api/v1/driver/update-status`  
**Authentication:** Required (Bearer token)  
**Description:** Updates the driver's status (online, offline, busy).

#### Request Body

```json
{
  "status": "online"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | Driver status: `online`, `offline`, or `busy` |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver status updated successfully",
  "data": {
    "id": "driver_123",
    "status": "online",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 5.3 Update Driver Location

**Endpoint:** `POST /api/v1/driver/update-location`  
**Authentication:** Required (Bearer token)  
**Description:** Updates the driver's current location.

#### Request Body

```json
{
  "latitude": -22.5700,
  "longitude": 17.0836,
  "status": "online"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `latitude` | float | Yes | Latitude (-90 to 90) |
| `longitude` | float | Yes | Longitude (-180 to 180) |
| `status` | string | No | Driver status: `online`, `offline`, or `busy` |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver location updated successfully",
  "data": null,
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 6. Driver Ride Management APIs

### 6.1 Get Available Rides

**Endpoint:** `GET /api/v1/driver/available-rides`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets all pending ride requests available for drivers to accept.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Maximum number of rides to return (default: 50, min: 1, max: 100) |

#### Example Request

```
GET /api/v1/driver/available-rides?limit=50
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Available rides retrieved successfully",
  "data": {
    "rides": [
      {
        "id": "ride_123456789",
        "userId": "zdXCHy7je3OaOVC4qHwS",
        "pickupLocation": {
          "latitude": -22.5700,
          "longitude": 17.0836,
          "address": "123 Main Street, Windhoek"
        },
        "dropoffLocation": {
          "latitude": -22.5800,
          "longitude": 17.0900,
          "address": "456 Oak Avenue, Windhoek"
        },
        "status": "pending",
        "estimatedFare": 13.00,
        "passengerCount": 1,
        "createdAt": "2024-12-31T19:00:00.000000"
      }
    ],
    "count": 1
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 6.2 Accept Ride

**Endpoint:** `POST /api/v1/driver/accept-ride`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Driver accepts a ride request. Uses Firestore transactions to ensure only one driver can accept a ride.

#### Request Body

```json
{
  "rideId": "ride_123456789"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rideId` | string | Yes | Ride ID to accept |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride accepted successfully",
  "data": {
    "id": "ride_123456789",
    "userId": "zdXCHy7je3OaOVC4qHwS",
    "driverId": "driver_123",
    "status": "accepted",
    "updatedAt": "2024-12-31T19:01:00.000000"
  },
  "timestamp": "2024-12-31T19:01:00.000000"
}
```

---

### 6.3 Decline Ride

**Endpoint:** `POST /api/v1/driver/decline-ride`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Driver declines a ride request.

#### Request Body

```json
{
  "rideId": "ride_123456789",
  "reason": "Too far away"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rideId` | string | Yes | Ride ID to decline |
| `reason` | string | No | Decline reason |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride declined successfully",
  "data": null,
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 6.4 Start Ride

**Endpoint:** `POST /api/v1/driver/start-ride`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Driver starts the ride (picks up passenger).

#### Request Body

```json
{
  "rideId": "ride_123456789"
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride started successfully",
  "data": {
    "id": "ride_123456789",
    "status": "started",
    "updatedAt": "2024-12-31T19:05:00.000000"
  },
  "timestamp": "2024-12-31T19:05:00.000000"
}
```

---

### 6.5 Complete Ride

**Endpoint:** `POST /api/v1/driver/complete-ride`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Driver completes the ride (drops off passenger).

#### Request Body

```json
{
  "rideId": "ride_123456789",
  "final_fare": 13.00
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rideId` | string | Yes | Ride ID to complete |
| `final_fare` | float | No | Final fare in NAD (default: 13.00) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride completed successfully",
  "data": {
    "id": "ride_123456789",
    "status": "completed",
    "finalFare": 13.00,
    "updatedAt": "2024-12-31T19:10:00.000000"
  },
  "timestamp": "2024-12-31T19:10:00.000000"
}
```

---

### 6.6 Get Driver Rides

**Endpoint:** `GET /api/v1/driver/get-rides`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets all rides for the logged-in driver with pagination.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1, min: 1) |
| `limit` | integer | No | Items per page (default: 10, min: 1, max: 100) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver rides retrieved successfully",
  "data": {
    "rides": [
      {
        "id": "ride_123456789",
        "userId": "zdXCHy7je3OaOVC4qHwS",
        "driverId": "driver_123",
        "status": "completed",
        "estimatedFare": 13.00,
        "finalFare": 13.00,
        "rating": 5,
        "createdAt": "2024-12-31T19:00:00.000000"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "hasMore": false
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 7. Driver Subscription APIs

### 7.1 Create Driver Subscription

**Endpoint:** `POST /api/v1/driver/subscription`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Creates a new driver subscription. Drivers must pay NAD 150.00 per month to access the platform.

#### Request Body

```json
{
  "payment_method": "cash"
}
```

**Note:** The `driver_id` is automatically extracted from the authentication token. Do not include it in the request body.

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `payment_method` | string | Yes | Payment method (currently only "cash" is supported) |

#### Error Responses

**401 Unauthorized - Missing Token:**
```json
{
  "success": false,
  "message": "Unauthorized",
  "error": {
    "code": "UNAUTHORIZED",
    "details": {}
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

**409 Conflict - Subscription Already Exists:**
```json
{
  "success": false,
  "message": "Driver already has an active subscription",
  "error": {
    "code": "CONFLICT",
    "details": {}
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Driver subscription created successfully",
  "data": {
    "id": "sub_123456789",
    "driverId": "driver_123",
    "status": "active",
    "amount": 150.00,
    "paymentMethod": "cash",
    "startDate": "2024-12-31T19:00:00.000000",
    "endDate": "2025-01-30T19:00:00.000000",
    "autoRenew": false,
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 7.2 Get Driver Subscription Status

**Endpoint:** `GET /api/v1/driver/subscription`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets the current driver's subscription status.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Subscription status retrieved successfully",
  "data": {
    "id": "sub_123456789",
    "driverId": "driver_123",
    "status": "active",
    "amount": 150.00,
    "paymentMethod": "cash",
    "startDate": "2024-12-31T19:00:00.000000",
    "endDate": "2025-01-30T19:00:00.000000",
    "autoRenew": false
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

**If no subscription found:**

```json
{
  "success": true,
  "message": "No active subscription found",
  "data": null,
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 7.3 Get Driver Subscription by ID

**Endpoint:** `GET /api/v1/driver/subscription/{driver_id}`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets subscription status for a specific driver by ID. Drivers can only view their own subscription.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `driver_id` | string | Yes | Driver ID (must match authenticated driver) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Subscription retrieved successfully",
  "data": {
    "id": "sub_123456789",
    "driverId": "driver_123",
    "status": "active",
    "amount": 150.00,
    "paymentMethod": "cash",
    "startDate": "2024-12-31T19:00:00.000000",
    "endDate": "2025-01-30T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 7.4 Update Driver Subscription

**Endpoint:** `PUT /api/v1/driver/subscription/{driver_id}`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Updates driver subscription settings.

#### Request Body

```json
{
  "auto_renew": true,
  "payment_method": "cash",
  "notification_preferences": {
    "ride_requests": true,
    "payments": true
  }
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `auto_renew` | boolean | No | Enable/disable auto-renewal |
| `payment_method` | string | No | Payment method (currently only "cash") |
| `notification_preferences` | object | No | Notification preferences |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Subscription updated successfully",
  "data": {
    "id": "sub_123456789",
    "autoRenew": true,
    "updatedAt": "2024-12-31T19:05:00.000000"
  },
  "timestamp": "2024-12-31T19:05:00.000000"
}
```

---

### 7.5 Process Subscription Payment

**Endpoint:** `POST /api/v1/driver/subscription/payment`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Processes a subscription payment. Creates a new subscription if one doesn't exist, or renews an existing one.

#### Request Body

```json
{
  "payment_method": "cash",
  "amount": 150.00
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `payment_method` | string | Yes | Payment method (currently only "cash") |
| `amount` | float | Yes | Amount in NAD (must be exactly 150.00) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Payment processed successfully",
  "data": {
    "subscription": {
      "id": "sub_123456789",
      "driverId": "driver_123",
      "status": "active",
      "amount": 150.00,
      "startDate": "2024-12-31T19:00:00.000000",
      "endDate": "2025-01-30T19:00:00.000000"
    },
    "payment": {
      "id": "pay_123456789",
      "driverId": "driver_123",
      "subscriptionId": "sub_123456789",
      "amount": 150.00,
      "paymentMethod": "cash",
      "status": "completed",
      "createdAt": "2024-12-31T19:00:00.000000"
    }
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 7.6 Get Subscription Payment History

**Endpoint:** `GET /api/v1/driver/subscription/history/{driver_id}`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets subscription payment history for a driver. Drivers can only view their own payment history.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `driver_id` | string | Yes | Driver ID (must match authenticated driver) |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1, min: 1) |
| `limit` | integer | No | Items per page (default: 10, min: 1, max: 100) |

#### Example Request

```
GET /api/v1/driver/subscription/history/driver_123?page=1&limit=10
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Payment history retrieved successfully",
  "data": {
    "payments": [
      {
        "id": "pay_123456789",
        "driverId": "driver_123",
        "subscriptionId": "sub_123456789",
        "amount": 150.00,
        "paymentMethod": "cash",
        "status": "completed",
        "createdAt": "2024-12-31T19:00:00.000000"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "hasMore": false
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 8. Parent Subscription APIs

### 8.1 Subscribe to Parent Package

**Endpoint:** `POST /api/v1/parent/subscribe`  
**Authentication:** Required (Bearer token - User)  
**Description:** Subscribes to the parent monthly package (NAD 1000.00 per month for unlimited rides).

#### Request Body

```json
{
  "payment_method": "cash",
  "children_profiles": [
    {
      "child_name": "Jane Doe",
      "child_age": 12,
      "school_name": "Windhoek High School",
      "pickup_address": "123 Main Street, Windhoek",
      "dropoff_address": "456 Oak Avenue, Windhoek",
      "emergency_contact": {
        "name": "John Doe",
        "phone": "+264812345678"
      }
    }
  ]
}
```

**Note:** The `user_id` is automatically extracted from the authentication token. Do not include it in the request body.

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `payment_method` | string | Yes | Payment method (currently only "cash") |
| `children_profiles` | array | Yes | Array of child profiles (minimum 1) |
| `children_profiles[].child_name` | string | Yes | Child's name (1-100 characters) |
| `children_profiles[].child_age` | integer | Yes | Child's age (5-18) |
| `children_profiles[].school_name` | string | Yes | School name (1-200 characters) |
| `children_profiles[].pickup_address` | string | Yes | Pickup address (1-500 characters) |
| `children_profiles[].dropoff_address` | string | Yes | Dropoff address (1-500 characters) |
| `children_profiles[].emergency_contact` | object | Yes | Emergency contact information |
| `children_profiles[].emergency_contact.name` | string | Yes | Emergency contact name (1-100 characters) |
| `children_profiles[].emergency_contact.phone` | string | Yes | Emergency contact phone (E.164 format) |

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Parent subscription created successfully",
  "data": {
    "id": "sub_parent_123",
    "userId": "zdXCHy7je3OaOVC4qHwS",
    "status": "active",
    "amount": 1000.00,
    "paymentMethod": "cash",
    "startDate": "2024-12-31T19:00:00.000000",
    "endDate": "2025-01-30T19:00:00.000000",
    "autoRenew": false,
    "childrenProfiles": [
      {
        "id": "child_123",
        "child_name": "Jane Doe",
        "child_age": 12,
        "school_name": "Windhoek High School",
        "pickup_address": "123 Main Street, Windhoek",
        "dropoff_address": "456 Oak Avenue, Windhoek",
        "emergency_contact": {
          "name": "John Doe",
          "phone": "+264812345678"
        }
      }
    ],
    "createdAt": "2024-12-31T19:00:00.000000",
    "updatedAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 8.2 Get Parent Subscription Status

**Endpoint:** `GET /api/v1/parent/subscription`  
**Authentication:** Required (Bearer token - User)  
**Description:** Gets the parent subscription status for a user.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID (must match authenticated user) |

#### Example Request

```
GET /api/v1/parent/subscription?user_id=zdXCHy7je3OaOVC4qHwS
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Subscription status retrieved successfully",
  "data": {
    "id": "sub_parent_123",
    "userId": "zdXCHy7je3OaOVC4qHwS",
    "status": "active",
    "amount": 1000.00,
    "startDate": "2024-12-31T19:00:00.000000",
    "endDate": "2025-01-30T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 8.3 Update Parent Subscription

**Endpoint:** `PUT /api/v1/parent/subscription`  
**Authentication:** Required (Bearer token - User)  
**Description:** Updates parent subscription settings.

#### Request Body

```json
{
  "auto_renew": true
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `auto_renew` | boolean | No | Enable/disable auto-renewal |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Subscription updated successfully",
  "data": {
    "id": "sub_parent_123",
    "autoRenew": true,
    "updatedAt": "2024-12-31T19:05:00.000000"
  },
  "timestamp": "2024-12-31T19:05:00.000000"
}
```

---

### 8.4 Cancel Parent Subscription

**Endpoint:** `DELETE /api/v1/parent/subscription`  
**Authentication:** Required (Bearer token - User)  
**Description:** Cancels a parent subscription.

#### Request Body

```json
{
  "reason": "No longer needed"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reason` | string | No | Cancellation reason |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Subscription cancelled successfully",
  "data": {
    "id": "sub_parent_123",
    "status": "cancelled",
    "cancellationReason": "No longer needed",
    "updatedAt": "2024-12-31T19:05:00.000000"
  },
  "timestamp": "2024-12-31T19:05:00.000000"
}
```

---

### 8.5 Get Parent Usage Statistics

**Endpoint:** `GET /api/v1/parent/usage`  
**Authentication:** Required (Bearer token - User)  
**Description:** Gets monthly usage statistics for a parent subscription.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID (must match authenticated user) |
| `month` | integer | Yes | Month (1-12) |
| `year` | integer | Yes | Year (>= 2020) |

#### Example Request

```
GET /api/v1/parent/usage?user_id=zdXCHy7je3OaOVC4qHwS&month=12&year=2024
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Usage statistics retrieved successfully",
  "data": {
    "month": 12,
    "year": 2024,
    "totalRides": 25,
    "completedRides": 23,
    "cancelledRides": 2,
    "rides": [
      {
        "id": "ride_123",
        "status": "completed",
        "createdAt": "2024-12-01T08:00:00.000000"
      }
    ]
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 8.6 Get Children Profiles

**Endpoint:** `GET /api/v1/parent/children`  
**Authentication:** Required (Bearer token - User)  
**Description:** Gets all children profiles for a parent.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID (must match authenticated user) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Children profiles retrieved successfully",
  "data": {
    "children": [
      {
        "id": "child_123",
        "child_name": "Jane Doe",
        "child_age": 12,
        "school_name": "Windhoek High School",
        "pickup_address": "123 Main Street, Windhoek",
        "dropoff_address": "456 Oak Avenue, Windhoek",
        "emergency_contact": {
          "name": "John Doe",
          "phone": "+264812345678"
        },
        "createdAt": "2024-12-31T19:00:00.000000"
      }
    ],
    "count": 1
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 8.7 Add Child Profile

**Endpoint:** `POST /api/v1/parent/children`  
**Authentication:** Required (Bearer token - User)  
**Description:** Adds a child profile to an existing parent subscription.

#### Request Body

```json
{
  "child_name": "John Doe Jr",
  "child_age": 10,
  "school_name": "Elementary School",
  "pickup_address": "123 Main Street, Windhoek",
  "dropoff_address": "456 Oak Avenue, Windhoek",
  "emergency_contact": {
    "name": "John Doe",
    "phone": "+264812345678"
  }
}
```

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Child profile added successfully",
  "data": {
    "id": "child_124",
    "child_name": "John Doe Jr",
    "child_age": 10,
    "school_name": "Elementary School",
    "pickup_address": "123 Main Street, Windhoek",
    "dropoff_address": "456 Oak Avenue, Windhoek",
    "emergency_contact": {
      "name": "John Doe",
      "phone": "+264812345678"
    },
    "createdAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 9. Payment APIs

### 9.1 Calculate Fare

**Endpoint:** `POST /api/v1/payment/calculate-fare`  
**Authentication:** Required (Bearer token - User)  
**Description:** Calculates the fare for a ride based on pickup and dropoff locations.

#### Request Body

```json
{
  "pickup_location": {
    "latitude": -22.5700,
    "longitude": 17.0836
  },
  "dropoff_location": {
    "latitude": -22.5800,
    "longitude": 17.0900
  },
  "ride_type": "standard"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pickup_location` | object | Yes | Pickup location |
| `pickup_location.latitude` | float | Yes | Latitude (-90 to 90) |
| `pickup_location.longitude` | float | Yes | Longitude (-180 to 180) |
| `dropoff_location` | object | Yes | Dropoff location |
| `dropoff_location.latitude` | float | Yes | Latitude (-90 to 90) |
| `dropoff_location.longitude` | float | Yes | Longitude (-180 to 180) |
| `ride_type` | string | No | Ride type (default: "standard") |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Fare calculated successfully",
  "data": {
    "distance": 5.2,
    "duration": 12,
    "estimatedFare": 13.00,
    "currency": "NAD"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 9.2 Process Payment

**Endpoint:** `POST /api/v1/payment/process`  
**Authentication:** Required (Bearer token - User)  
**Description:** Processes payment for a ride. The user ID is automatically obtained from the authentication token.

#### Request Body

```json
{
  "ride_id": "ride_123456789",
  "amount": 13.00,
  "payment_method": "cash"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ride_id` | string | Yes | Ride ID |
| `amount` | float | No | Amount in NAD (default: 13.00) |
| `payment_method` | string | No | Payment method (default: "cash", currently only "cash" is supported) |

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Payment processed successfully",
  "data": {
    "id": "pay_123456789",
    "rideId": "ride_123456789",
    "userId": "zdXCHy7je3OaOVC4qHwS",
    "amount": 13.00,
    "paymentMethod": "cash",
    "status": "completed",
    "createdAt": "2024-12-31T19:00:00.000000"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 9.3 Get Payment History

**Endpoint:** `GET /api/v1/payment/history`  
**Authentication:** Required (Bearer token - User)  
**Description:** Gets payment history for the logged-in user with pagination.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1, min: 1) |
| `limit` | integer | No | Items per page (default: 10, min: 1, max: 100) |

#### Example Request

```
GET /api/v1/payment/history?page=1&limit=10
```

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Payment history retrieved successfully",
  "data": {
    "payments": [
      {
        "id": "pay_123456789",
        "rideId": "ride_123456789",
        "userId": "zdXCHy7je3OaOVC4qHwS",
        "amount": 13.00,
        "paymentMethod": "cash",
        "status": "completed",
        "createdAt": "2024-12-31T19:00:00.000000"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "hasMore": false
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 9.4 Subscribe Monthly

**Endpoint:** `POST /api/v1/subscribe-monthly`  
**Authentication:** Required (Bearer token - User)  
**Description:** Subscribes to monthly package (for users who want to pay per ride instead of parent package).

#### Request Body

```json
{
  "paymentMethod": "cash"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `paymentMethod` | string | Yes | Payment method (currently only "cash") |

#### Response (201 Created)

```json
{
  "success": true,
  "message": "Monthly subscription created successfully",
  "data": {
    "subscription": {
      "id": "sub_monthly_123",
      "userId": "zdXCHy7je3OaOVC4qHwS",
      "paymentMethod": "cash",
      "createdAt": "2024-12-31T19:00:00.000000"
    }
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 10. Analytics APIs

### 10.1 Get User Ride Analytics

**Endpoint:** `GET /api/v1/analytics/rides`  
**Authentication:** Required (Bearer token - User)  
**Description:** Gets ride analytics for the logged-in user.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Ride analytics retrieved successfully",
  "data": {
    "totalRides": 25,
    "completedRides": 23,
    "cancelledRides": 2,
    "averageRating": 4.5,
    "totalSpent": 325.00
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 10.2 Get User Performance Analytics

**Endpoint:** `GET /api/v1/analytics/performance`  
**Authentication:** Required (Bearer token - User)  
**Description:** Gets performance analytics for the logged-in user.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Performance analytics retrieved successfully",
  "data": {
    "onTimeRate": 95.5,
    "cancellationRate": 8.0,
    "averageWaitTime": 5.2
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 10.3 Get Driver Earnings

**Endpoint:** `GET /api/v1/driver/analytics/earnings`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets earnings analytics for the logged-in driver.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver earnings retrieved successfully",
  "data": {
    "totalEarnings": 3250.00,
    "thisMonth": 650.00,
    "thisWeek": 195.00,
    "today": 26.00,
    "totalRides": 250,
    "averageEarningPerRide": 13.00
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 10.4 Get Driver Ride Analytics

**Endpoint:** `GET /api/v1/driver/analytics/rides`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets ride analytics for the logged-in driver.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver ride analytics retrieved successfully",
  "data": {
    "totalRides": 250,
    "completedRides": 245,
    "cancelledRides": 5,
    "averageRating": 4.8,
    "totalEarnings": 3250.00
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

### 10.5 Get Driver Performance Analytics

**Endpoint:** `GET /api/v1/driver/analytics/performance`  
**Authentication:** Required (Bearer token - Driver)  
**Description:** Gets performance analytics for the logged-in driver.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Driver performance analytics retrieved successfully",
  "data": {
    "acceptanceRate": 95.0,
    "completionRate": 98.0,
    "averageResponseTime": 3.5,
    "averageRating": 4.8,
    "totalRides": 250,
    "onTimeRate": 96.5
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `acceptanceRate` | float | Percentage of rides accepted |
| `completionRate` | float | Percentage of rides completed |
| `averageResponseTime` | float | Average response time in minutes |
| `averageRating` | float | Average rating received |
| `totalRides` | integer | Total number of rides |
| `onTimeRate` | float | Percentage of on-time arrivals |

---

## 11. Health Check APIs

### 11.1 Health Check

**Endpoint:** `GET /api/v1/health`  
**Authentication:** Not required  
**Description:** Checks if the API service is running and healthy.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "Service is healthy",
  "data": {
    "status": "healthy",
    "service": "Londa APIs",
    "version": "1.0.0"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Service status (always "healthy" if endpoint responds) |
| `service` | string | Service name |
| `version` | string | API version |

---

### 11.2 API Test

**Endpoint:** `GET /api/v1/test`  
**Authentication:** Not required  
**Description:** Test endpoint to verify API Gateway JSON responses are working correctly.

#### Response (200 OK)

```json
{
  "success": true,
  "message": "API Gateway is working correctly",
  "data": {
    "status": "ok",
    "service": "Londa APIs"
  },
  "timestamp": "2024-12-31T19:00:00.000000"
}
```

---

## 📝 Additional Notes

### Rate Limiting

Currently, there are no rate limits implemented. However, it's recommended to:
- Implement rate limiting in production
- Use reasonable request intervals (e.g., 1-2 seconds between requests)
- Handle rate limit errors gracefully in the mobile app

### Pagination

Endpoints that return lists support pagination:
- `page`: Page number (starts at 1)
- `limit`: Items per page (typically 10-100)
- Response includes `total`, `hasMore` fields for pagination UI

### Date/Time Format

All timestamps are returned in ISO 8601 format:
```
2024-12-31T19:00:00.000000
```

### Location Coordinates

All location coordinates use:
- **Latitude**: -90 to 90 (decimal degrees)
- **Longitude**: -180 to 180 (decimal degrees)
- Example: Windhoek, Namibia: `-22.5700, 17.0836`

### Currency

All monetary values are in **NAD (Namibian Dollar)**:
- Driver Subscription: NAD 150.00/month
- Parent Subscription: NAD 1000.00/month
- Per-Ride Payment: NAD 13.00

### Phone Number Format

All phone numbers must be in **E.164 format**:
- Must start with `+`
- Include country code
- Example: `+264813442530` (Namibia)

### User Types

Valid user types:
- `student`: Student user
- `worker`: Working professional
- `parent`: Parent user

### Ride Status Values

Valid ride status values:
- `pending`: Ride requested, waiting for driver
- `accepted`: Driver accepted the ride
- `started`: Driver picked up passenger
- `completed`: Ride finished successfully
- `cancelled`: Ride was cancelled

### Driver Status Values

Valid driver status values:
- `online`: Driver is available for rides
- `offline`: Driver is not available
- `busy`: Driver is currently on a ride

### Payment Methods

Currently supported payment methods:
- `cash`: Cash payment (only method available)

### Subscription Status Values

Valid subscription status values:
- `active`: Subscription is active
- `expired`: Subscription has expired
- `cancelled`: Subscription was cancelled

---

## 🔗 Quick Reference

### Authentication Flow

1. **Register/Login:**
   - `POST /api/v1/registration` → Get `sessionInfo`
   - `POST /api/v1/verify-otp` → Get `accessToken`

2. **Create Account:**
   - `POST /api/v1/create-account` → Complete profile

3. **Use Token:**
   - Include `Authorization: Bearer <token>` in all protected requests

4. **Refresh Token (when expired):**
   - `POST /api/v1/refresh-token` → Get new `accessToken` (works with expired tokens)

### Common Endpoints

| Purpose | Endpoint | Method |
|---------|----------|--------|
| Health Check | `/api/v1/health` | GET |
| Refresh Token | `/api/v1/refresh-token` | POST |
| User Profile | `/api/v1/me` | GET |
| Request Ride | `/api/v1/request-ride` | POST |
| Get Rides | `/api/v1/get-rides` | GET |
| Driver Profile | `/api/v1/driver/me` | GET |
| Available Rides | `/api/v1/driver/available-rides` | GET |
| Accept Ride | `/api/v1/driver/accept-ride` | POST |

---

## 📞 Support

For API support or questions:
- Check the [Firestore Indexes Documentation](FIRESTORE_INDEXES.md) for database setup
- Review [Authentication Flow Guide](AUTHENTICATION_FLOW_EXPLAINED.md) for auth details
- Ensure all required Firestore indexes are created before using query endpoints

---

**Document Version:** 1.0.0  
**Last Updated:** December 31, 2024  
**Maintained by:** Londa Rides Development Team
