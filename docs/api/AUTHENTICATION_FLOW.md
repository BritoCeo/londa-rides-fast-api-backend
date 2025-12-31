# 🔐 Authentication Flow Guide

## Important: Registration Does NOT Require Auth Token!

The **Registration API** (`POST /api/v1/registration`) is a **PUBLIC endpoint** and does **NOT** require an authentication token. This is the **first step** in the authentication flow.

## 🔄 Complete Authentication Flow

### Step 1: Register User (Send OTP) - NO AUTH REQUIRED ✅

```http
POST http://localhost:8000/api/v1/registration
Content-Type: application/json

{
  "phone_number": "+264813442530"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "sessionInfo": "session_info_string_here",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

**What to save:** `sessionInfo` (automatically saved to `{{session_info}}`)

### Step 2: Verify OTP (Login) - NO AUTH REQUIRED ✅

```http
POST http://localhost:8000/api/v1/verify-otp
Content-Type: application/json

{
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "{{session_info}}"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_123",
    "phone_number": "+264813442530",
    "name": "John Doe"
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

**🎯 THIS IS WHERE YOU GET YOUR AUTH TOKEN!**

The `accessToken` from this response is:
- Automatically saved to `{{auth_token}}` collection variable
- Used for all subsequent authenticated requests

### Step 3: Use Auth Token for Protected Endpoints

Now you can use the `{{auth_token}}` for authenticated requests:

```http
GET http://localhost:8000/api/v1/me
Authorization: Bearer {{auth_token}}
```

## 📋 Public Endpoints (No Auth Required)

These endpoints **DO NOT** require authentication:

1. ✅ `POST /api/v1/registration` - Register user (send OTP)
2. ✅ `POST /api/v1/verify-otp` - Verify OTP and login (GET TOKEN HERE!)
3. ✅ `POST /api/v1/email-otp-request` - Request email OTP
4. ✅ `PUT /api/v1/email-otp-verify` - Verify email OTP
5. ✅ `POST /api/v1/create-account` - Create user account
6. ✅ `POST /api/v1/driver/send-otp` - Driver send OTP
7. ✅ `POST /api/v1/driver/login` - Driver login (GET TOKEN HERE!)
8. ✅ `POST /api/v1/driver/verify-otp` - Driver verify OTP
9. ✅ `POST /api/v1/driver/create-account` - Create driver account

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
   - User tokens expire after 30 days
   - Driver tokens expire after 7 days
   - Re-run the login flow to get a new token

### Where is the token stored?

The token is stored in:
- **Postman Collection Variables**: `{{auth_token}}`
- **Auto-populated** after successful login
- **Used automatically** for all authenticated requests

## 📚 Related Documentation

- [Detailed Postman Collection Guide](./DETAILED_POSTMAN_COLLECTION.md)
- [API Documentation](./API_DOCUMENTATION.md)
- [Newman Testing Guide](../testing/NEWMAN_POSTMAN_TESTING.md)

---

**Key Takeaway:** Registration is **PUBLIC** - you get the auth token **AFTER** verifying OTP in the login step!

