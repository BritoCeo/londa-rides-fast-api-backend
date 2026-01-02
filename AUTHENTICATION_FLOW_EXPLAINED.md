# 🔐 Authentication Flow - Explained

## Overview

The Londa API uses a **single API** to serve both **User App** and **Driver App**. Authentication is handled through Firebase Authentication with **role-based access control (RBAC)** using custom claims.

---

## 🏗️ Architecture: Single API, Two Apps

### How It Works

Both apps use the **same API base URL** (`/api/v1`), but with different endpoint paths:

- **User App** → `/api/v1/registration`, `/api/v1/login`, `/api/v1/request-ride`, etc.
- **Driver App** → `/api/v1/driver/send-otp`, `/api/v1/driver/login`, `/api/v1/driver/accept-ride`, etc.

### Role-Based Access Control (RBAC)

The API uses **Firebase custom claims** to differentiate between users and drivers:

- **Users** → Token includes `{"user_type": "user"}`
- **Drivers** → Token includes `{"user_type": "driver"}`

**Security Guards:**
- `get_current_user()` → Allows both users and drivers
- `get_current_driver()` → **Only allows drivers** (blocks users with 403 Forbidden)

---

## 👤 User Authentication Flow

### Step 1: Registration (Send OTP)
```
POST /api/v1/registration
Body: { "phone_number": "+264813442530" }
```
- Creates OTP session in Firestore
- Sends OTP via Firebase Authentication
- Returns `sessionInfo` for verification

### Step 2: Verify OTP / Login
```
POST /api/v1/verify-otp  (or POST /api/v1/login)
Body: { 
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "..."
}
```

**What Happens:**
1. ✅ Verifies OTP with Firebase Authentication
2. ✅ Checks if user exists in **Firestore** (database)
3. ✅ If user exists in Firestore but NOT in Firebase Auth → **Auto-creates Auth user**
4. ✅ If user doesn't exist → Creates new Firebase Auth user
5. ✅ Creates/updates Firestore document
6. ✅ Sets custom claims: `{"user_type": "user"}`
7. ✅ Generates custom token with `user_type` claim
8. ✅ Returns `accessToken` and user data

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIs...",
    "user": { "id": "...", "phoneNumber": "...", ... }
  }
}
```

### Step 3: Create Account (Optional)
```
POST /api/v1/create-account
Headers: { "Authorization": "Bearer <accessToken>" }
Body: {
  "name": "John Doe",
  "email": "john@example.com",
  "userType": "student"
}
```
- Updates Firestore document with full details
- Updates custom claims based on `userType` (student, parent, etc.)
- Returns updated user profile

---

## 🚗 Driver Authentication Flow

### Step 1: Send OTP
```
POST /api/v1/driver/send-otp
Body: { "phone_number": "+264813442530" }
```
- Creates OTP session
- Sends OTP via Firebase Authentication
- Returns `sessionInfo`

### Step 2: Verify OTP / Login
```
POST /api/v1/driver/verify-otp  (or POST /api/v1/driver/login)
Body: { 
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "..."
}
```

**What Happens:**
1. ✅ Verifies OTP with Firebase Authentication
2. ✅ Checks if driver exists in **Firestore** (database)
3. ✅ If driver exists in Firestore but NOT in Firebase Auth → **Auto-creates Auth user**
4. ✅ If driver doesn't exist → Creates new Firebase Auth user
5. ✅ Creates/updates Firestore driver document
6. ✅ Sets custom claims: `{"user_type": "driver"}` ⚠️ **Important: This is "driver", not "user"**
7. ✅ Generates custom token with `user_type: "driver"` claim
8. ✅ Returns `accessToken` and driver data

**Response:**
```json
{
  "success": true,
  "message": "Driver login successful",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIs...",
    "driver": { "id": "...", "phoneNumber": "...", ... }
  }
}
```

### Step 3: Create Driver Account (Optional)
```
POST /api/v1/driver/create-account
Headers: { "Authorization": "Bearer <accessToken>" }
Body: {
  "name": "Driver Name",
  "license_number": "ABC123",
  "vehicle_model": "Toyota Corolla",
  "vehicle_plate": "NA12345",
  "vehicle_color": "White"
}
```
- Updates Firestore driver document with full details
- Returns updated driver profile

---

## 🔄 Token Refresh Flow

### Shared Endpoint (Works for Both Users and Drivers)
```
POST /api/v1/refresh-token
Headers: { "Authorization": "Bearer <expired_or_valid_token>" }
```

**What Happens:**
1. ✅ Decodes token (works even if expired)
2. ✅ Extracts `user_id` and `user_type` from token
3. ✅ Verifies user exists in Firebase Auth
4. ✅ Determines user type from:
   - Firestore `userType` field (priority)
   - Firebase Auth custom claims
   - Token `user_type` (fallback)
5. ✅ Checks if user is actually a driver (if `user_type == "user"`)
6. ✅ Generates new custom token with correct `user_type`
7. ✅ Returns new `accessToken` and user/driver data

**Response:**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIs...",
    "user": { ... }  // or "driver": { ... }
  }
}
```

---

## 🔒 Protected Endpoints

### User Endpoints (Protected with `get_current_user`)
These endpoints accept **both users and drivers**:

- `GET /api/v1/me` → Get profile
- `POST /api/v1/request-ride` → Request a ride
- `GET /api/v1/get-rides` → Get user's rides
- `POST /api/v1/cancel-ride` → Cancel ride
- `POST /api/v1/parent/subscribe` → Subscribe to parent package

**How it works:**
- Extracts `user_id` from token (not request body)
- Allows both users and drivers to access

### Driver-Only Endpoints (Protected with `get_current_driver`)
These endpoints **only allow drivers**:

- `GET /api/v1/driver/me` → Get driver profile
- `GET /api/v1/driver/available-rides` → Get available rides
- `POST /api/v1/driver/accept-ride` → Accept a ride
- `POST /api/v1/driver/subscription` → Create driver subscription

**How it works:**
- Verifies token
- Checks `user_type == "driver"`
- If `user_type != "driver"` → Returns **403 Forbidden**
- Only drivers can proceed

---

## 🔐 Two Separate Systems

### Firebase Auth (Authentication Service)
- Manages user authentication
- Stores user credentials (phone, email)
- Generates and verifies tokens
- Stores custom claims (`user_type`)
- **User must exist here to verify tokens**

### Firestore (Database)
- Stores user/driver profile data
- Stores rides, subscriptions, payments, etc.
- **User document can exist here independently**

### The Sync Issue (Fixed)

**The Problem:**
- User document in Firestore ≠ User in Firebase Auth
- If you tested before, a user document might exist in Firestore
- But that user might NOT exist in Firebase Auth
- Result: "User not found in Firebase Auth" error

**The Fix:**
The code now automatically:
1. ✅ Checks if user exists in Firestore
2. ✅ If yes, verifies they also exist in Firebase Auth
3. ✅ If not in Auth, **creates the Auth user automatically**
4. ✅ Then generates the token

This ensures both systems are **always in sync**!

---

## 📱 Mobile App Implementation

### User App
```javascript
// Base URL
const API_BASE = "https://api.londarides.com/api/v1";

// Authentication
POST /api/v1/registration
POST /api/v1/login
POST /api/v1/create-account

// Protected endpoints
GET /api/v1/me
POST /api/v1/request-ride
GET /api/v1/get-rides
```

### Driver App
```javascript
// Base URL (same!)
const API_BASE = "https://api.londarides.com/api/v1";

// Authentication
POST /api/v1/driver/send-otp
POST /api/v1/driver/login
POST /api/v1/driver/create-account

// Protected endpoints (driver-only)
GET /api/v1/driver/me
GET /api/v1/driver/available-rides
POST /api/v1/driver/accept-ride
```

**Note:** Both apps use the **same API base URL**, just different endpoint paths!

---

## 🎯 Key Points

### 1. Custom Claims for RBAC
- **Users** get `user_type: "user"` in token
- **Drivers** get `user_type: "driver"` in token
- API checks `user_type` to enforce access control

### 2. Security
- ✅ User IDs extracted from tokens (not request body)
- ✅ Users cannot access driver-only endpoints (403 Forbidden)
- ✅ Drivers can access user endpoints (by design)
- ✅ Token verification on every protected request

### 3. Token Types
- **Custom Token**: Generated by backend, includes custom claims
- **ID Token**: Generated by Firebase SDK after exchanging custom token
- **Best Practice**: Mobile apps should exchange custom token for ID token using Firebase SDK

### 4. Token Refresh
- Works for both users and drivers
- Auto-detects user type
- Accepts expired tokens
- Returns new token with correct `user_type`

---

## 🐛 Common Issues & Solutions

### Issue 1: "User not found in Firebase Auth"
**Cause:** User exists in Firestore but not in Firebase Auth

**Solution:** ✅ **Fixed** - Code now auto-creates Auth user if missing

### Issue 2: "This endpoint requires driver authentication" (403)
**Cause:** User trying to access driver-only endpoint

**Solution:** Use driver login endpoint (`/api/v1/driver/login`) to get driver token

### Issue 3: Token expired
**Cause:** Token has expired

**Solution:** Use `/api/v1/refresh-token` endpoint to get new token

### Issue 4: Wrong user_type in token
**Cause:** User logged in as user but trying to access driver endpoints

**Solution:** Use correct login endpoint:
- Users → `/api/v1/login`
- Drivers → `/api/v1/driver/login`

---

## 📊 Flow Diagrams

### User Registration & Login
```
User App
   │
   ├─ POST /registration
   │  └─→ Creates OTP session
   │
   ├─ POST /login (or /verify-otp)
   │  ├─→ Verifies OTP
   │  ├─→ Creates/updates Firebase Auth user
   │  ├─→ Sets custom claims: {"user_type": "user"}
   │  └─→ Returns accessToken
   │
   └─ POST /create-account (optional)
      └─→ Updates profile with full details
```

### Driver Registration & Login
```
Driver App
   │
   ├─ POST /driver/send-otp
   │  └─→ Creates OTP session
   │
   ├─ POST /driver/login (or /driver/verify-otp)
   │  ├─→ Verifies OTP
   │  ├─→ Creates/updates Firebase Auth user
   │  ├─→ Sets custom claims: {"user_type": "driver"} ⚠️
   │  └─→ Returns accessToken
   │
   └─ POST /driver/create-account (optional)
      └─→ Updates driver profile with full details
```

### Token Refresh (Both Apps)
```
User/Driver App
   │
   └─ POST /refresh-token
      ├─→ Decodes token (even if expired)
      ├─→ Determines user_type
      ├─→ Generates new token with correct user_type
      └─→ Returns new accessToken
```

---

## ✅ Summary

**The API correctly:**
1. ✅ Serves both User and Driver apps from a single API
2. ✅ Uses role-based access control via Firebase custom claims
3. ✅ Properly protects endpoints with appropriate security guards
4. ✅ Auto-syncs Firebase Auth and Firestore
5. ✅ Supports token refresh for both user types
6. ✅ Blocks unauthorized access (users cannot access driver-only endpoints)

**Everything is working correctly!** 🎉

