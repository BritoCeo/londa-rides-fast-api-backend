# 🔑 How to Get `auth_token` for `/create-account` API

## Quick Answer

**The `auth_token` comes from the `/verify-otp` endpoint response.**

---

## Complete Step-by-Step Flow

### Step 1: Register (Send OTP) 📱

**POST** `/api/v1/registration`

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
  }
}
```

**Save:** `data.sessionInfo` → Use in Step 2

---

### Step 2: Verify OTP (Get Token) 🔑

**POST** `/api/v1/verify-otp`

**Request:**
```json
{
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "abc123xyz..."  // from Step 1
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
      ...
    }
  }
}
```

**✅ THIS IS YOUR `auth_token`!**

**Save:** `data.accessToken` → This is what you use as `auth_token`

---

### Step 3: Create Account (Use Token) ✅

**POST** `/api/v1/create-account`

**Headers:**
```
Authorization: Bearer <accessToken from Step 2>
Content-Type: application/json
```

**Request:**
```json
{
  "phone_number": "+264813442530",
  "email": "user@example.com",
  "name": "John Doe",
  "userType": "student"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account created successfully",
  "data": {
    "id": "user123",
    "name": "John Doe",
    ...
  }
}
```

---

## 📋 For Postman Collection

The Postman collection is already configured to:
1. ✅ Auto-save `sessionInfo` from `/registration`
2. ✅ Auto-save `accessToken` as `auth_token` from `/verify-otp`
3. ✅ Auto-use `auth_token` in Bearer token for protected endpoints

**Just run the requests in order:**
1. "Register User (Send OTP)" 
2. "Verify OTP (Login)" ← Token is auto-saved here
3. "Create User Account" ← Uses saved token automatically

---

## 🔧 Token Types Explained

### Custom Token (What `/verify-otp` Returns)
- **Type:** Firebase Custom Token
- **Purpose:** To be exchanged for ID token on client
- **Can be used:** ✅ Yes, for development/testing (now supported)
- **Expires:** No expiration

### ID Token (Production)
- **Type:** Firebase ID Token  
- **Purpose:** Standard authentication token
- **How to get:** Exchange custom token using Firebase SDK on client
- **Expires:** Yes (1 hour)

---

## ✅ Current Implementation

**Good News!** The security layer now supports **both**:
- ✅ ID tokens (production)
- ✅ Custom tokens (development/testing)

So you can use the `accessToken` from `/verify-otp` directly in Postman!

---

## 🚀 Quick Test Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/registration \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530"}'

# Response: Save sessionInfo

# 2. Verify OTP  
curl -X POST http://localhost:8000/api/v1/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530", "otp": "123456", "sessionInfo": "..."}'

# Response: Save accessToken (this is your auth_token!)

# 3. Create Account
curl -X POST http://localhost:8000/api/v1/create-account \
  -H "Authorization: Bearer <accessToken from step 2>" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530", "name": "John Doe", "userType": "student"}'
```

---

## 💡 Summary

**Answer:** The `auth_token` is the `accessToken` from the `/verify-otp` response.

**Flow:**
1. `/registration` → Get `sessionInfo`
2. `/verify-otp` → Get `accessToken` (this is your `auth_token`)
3. `/create-account` → Use `accessToken` as `Authorization: Bearer <token>`

**In Postman:** The collection auto-saves and uses the token for you! 🎉

