# 🔐 Authentication Flow Guide

## Overview

The Londa Rides API uses Firebase Authentication with custom tokens. The `accessToken` returned by the API is a **Firebase Custom Token** that must be exchanged for an ID token using the Firebase SDK before making authenticated requests.

**⚠️ Important:** For mobile apps, see the [Frontend Integration Guide](../../FRONTEND_INTEGRATION_GUIDE.md) for complete code examples.

---

## Complete Authentication Flow

### Step 1: Register User (Send OTP) - NO AUTH REQUIRED ✅

**Endpoint:** `POST /api/v1/registration`

**Request:**
```json
{
  "phone_number": "+264813442530"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "sessionInfo": "abc123xyz..."
  },
  "timestamp": "2025-01-01T00:00:00.000000"
}
```

**Save:** `sessionInfo` from `data.sessionInfo`

### Step 2: Verify OTP (Get Custom Token) - NO AUTH REQUIRED ✅

**Endpoint:** `POST /api/v1/verify-otp`

**Request:**
```json
{
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "abc123xyz..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user123",
      "phone_number": "+264813442530",
      "email": null,
      "name": null,
      "userType": null,
      "createdAt": "2025-01-01T00:00:00.000000",
      "updatedAt": "2025-01-01T00:00:00.000000"
    }
  },
  "timestamp": "2025-01-01T00:00:00.000000"
}
```

**⚠️ Important:** The `accessToken` is a **Firebase Custom Token**, not an ID token.

### Step 3: Exchange Custom Token for ID Token (Client-Side) 🔄

**This step MUST be done on the client using Firebase SDK.**

For mobile apps, see the [Frontend Integration Guide](../../FRONTEND_INTEGRATION_GUIDE.md) for complete examples.

**For Postman/Testing:** In development mode, you can use the custom token directly. In production, always exchange for ID token.

### Step 4: Use ID Token for Protected Endpoints

**Endpoint:** `GET /api/v1/me`

**Headers:**
```
Authorization: Bearer <ID_TOKEN>
```

**Response:**
```json
{
  "success": true,
  "message": "User profile retrieved successfully",
  "data": {
    "id": "user123",
    "phone_number": "+264813442530",
    "email": "user@example.com",
    "name": "John Doe",
    "userType": "student",
    "createdAt": "2025-01-01T00:00:00.000000",
    "updatedAt": "2025-01-01T00:00:00.000000"
  },
  "timestamp": "2025-01-01T00:00:00.000000"
}
```

## 📋 Public Endpoints (No Auth Required)

These endpoints **DO NOT** require authentication:

1. ✅ `POST /api/v1/registration` - Register user (send OTP)
2. ✅ `POST /api/v1/verify-otp` - Verify OTP and get custom token
3. ✅ `POST /api/v1/login` - Alias for verify-otp
4. ✅ `POST /api/v1/email-otp-request` - Request email OTP
5. ✅ `PUT /api/v1/email-otp-verify` - Verify email OTP
6. ✅ `POST /api/v1/driver/send-otp` - Driver send OTP
7. ✅ `POST /api/v1/driver/verify-otp` - Driver verify OTP and get custom token
8. ✅ `POST /api/v1/driver/login` - Alias for driver verify-otp
9. ✅ `GET /health` - Health check
10. ✅ `GET /test` - API test endpoint

**Note:** `POST /api/v1/create-account` and `POST /api/v1/driver/create-account` **REQUIRE** authentication.

## 🔒 Protected Endpoints (Auth Required)

These endpoints **REQUIRE** the `{{auth_token}}`:

- `GET /api/v1/me` - Get logged in user data
- `GET /api/v1/get-rides` - Get user rides
- `POST /api/v1/request-ride` - Request a ride
- `GET /api/v1/nearby-drivers` - Get nearby drivers
- `POST /api/v1/cancel-ride` - Cancel ride
- `PUT /api/v1/rate-ride` - Rate ride
- All driver management endpoints
- All subscription endpoints
- All payment endpoints
- All analytics endpoints

## 🛠️ Postman Collection Configuration

### Collection-Level Auth

The collection has a **default Bearer token** at the collection level:

```json
{
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{auth_token}}"
      }
    ]
  }
}
```

This applies to **all requests by default**, but:

### Public Endpoints Override

All **public endpoints** (registration, login, etc.) have been configured with:

```json
{
  "auth": {
    "type": "noauth"
  }
}
```

This **overrides** the collection-level auth, so these endpoints don't require a token.

## 📝 How to Get Auth Token

### Method 1: Automatic (Recommended)

1. Run **"Register User (Send OTP)"** - No auth needed
2. Run **"Verify OTP (Login)"** - No auth needed
3. The `accessToken` is **automatically saved** to `{{auth_token}}`
4. All subsequent requests will use this token

### Method 2: Manual

1. Run **"Verify OTP (Login)"** request
2. Copy the `accessToken` from the response
3. In Postman:
   - Click on collection name
   - Go to **Variables** tab
   - Paste token into `auth_token` variable
   - Save collection

### Method 3: From Environment Variables

If you have a token in your `.env.dev` file:

```env
JWT_SECRET=your_secret_here
```

**Note:** The `JWT_SECRET` is used to **sign** tokens, not to get a token. You still need to login to get a token.

## 🔍 Troubleshooting

### Error: "401 Unauthorized" on Registration

**Problem:** Registration endpoint is trying to use auth token.

**Solution:** 
- The collection has been fixed - registration endpoints now have `"auth": { "type": "noauth" }`
- If you still see this, make sure you're using the latest collection
- In Postman, check the request's **Authorization** tab - it should say "Inherit auth from parent" but the parent (request) should have "No Auth"

### Error: "Token not found" or "Invalid token"

**Problem:** `{{auth_token}}` variable is empty or invalid.

**Solution:**
1. Make sure you've completed the login flow:
   - Registration → Verify OTP
2. Check if token was saved:
   - In Postman, click collection → Variables tab
   - Verify `auth_token` has a value
3. Token might be expired:
   - ID tokens expire after 1 hour
   - Use `/api/v1/refresh-token` endpoint to refresh expired tokens
   - Or re-run the login flow to get a new token

### Where is the token stored?

The token is stored in:
- **Postman Collection Variables**: `{{auth_token}}`
- **Auto-populated** after successful login
- **Used automatically** for all authenticated requests

## 📚 Related Documentation

- [Frontend Integration Guide](../../FRONTEND_INTEGRATION_GUIDE.md) - Complete mobile app integration examples
- [Authentication Flow Guide](../../AUTHENTICATION_FLOW_GUIDE.md) - Step-by-step guide with code examples
- [Authentication Flow Explained](../../AUTHENTICATION_FLOW_EXPLAINED.md) - Technical details
- [API Documentation](../../API_DOCUMENTATION.md) - Full API reference
- [How to Get Auth Token](../../HOW_TO_GET_AUTH_TOKEN.md) - Quick reference

---

**Key Takeaways:**
1. Registration is **PUBLIC** - no auth token required
2. You get a **custom token** after verifying OTP
3. **Exchange custom token for ID token** using Firebase SDK (mobile apps)
4. Use **ID token** for all authenticated requests
5. Tokens expire after 1 hour - use `/refresh-token` to refresh

