# 🔐 Authentication Flow Guide

## How to Get `auth_token` for `/create-account` API

### Complete Authentication Flow

The `/create-account` endpoint requires authentication. Here's the step-by-step process:

---

## Step 1: Register User (Send OTP) 📱

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
  "timestamp": "2025-12-31T..."
}
```

**Save:** `sessionInfo` from the response

---

## Step 2: Verify OTP (Get Access Token) 🔑

**Endpoint:** `POST /api/v1/verify-otp`

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
  },
  "timestamp": "2025-12-31T..."
}
```

**⚠️ IMPORTANT:** The `accessToken` returned is a **Firebase Custom Token**, not an ID token.

---

## Step 3: Exchange Custom Token for ID Token (Client-Side) 🔄

**This step must be done on the client (mobile app/web app) using Firebase SDK:**

### For Web (JavaScript):
```javascript
import { getAuth, signInWithCustomToken } from "firebase/auth";

const auth = getAuth();
const customToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."; // from Step 2

signInWithCustomToken(auth, customToken)
  .then((userCredential) => {
    // Get the ID token
    return userCredential.user.getIdToken();
  })
  .then((idToken) => {
    // Use this idToken as your auth_token
    console.log("ID Token:", idToken);
    // Save this token for API calls
  });
```

### For Mobile (React Native):
```javascript
import auth from '@react-native-firebase/auth';

const customToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...";

auth()
  .signInWithCustomToken(customToken)
  .then(() => {
    return auth().currentUser.getIdToken();
  })
  .then((idToken) => {
    // Use this idToken as your auth_token
    console.log("ID Token:", idToken);
  });
```

---

## Step 4: Create Account (Use ID Token) ✅

**Endpoint:** `POST /api/v1/create-account`

**Headers:**
```
Authorization: Bearer <ID_TOKEN_FROM_STEP_3>
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
    "phone_number": "+264813442530",
    "email": "user@example.com",
    "userType": "student",
    ...
  },
  "timestamp": "2025-12-31T..."
}
```

---

## 🔧 For Postman/API Testing

Since Postman can't exchange custom tokens, you have two options:

### Option 1: Use Firebase Admin SDK to Exchange Token (Backend Helper)

Create a helper endpoint that exchanges the custom token:

```python
# Add to app/users/router.py
@router.post("/exchange-token", status_code=status.HTTP_200_OK)
async def exchange_custom_token(
    request: dict,
    current_user: dict = Depends(get_current_user)  # This won't work with custom token
):
    # This would need special handling
    pass
```

### Option 2: Use Custom Token Directly (Development Only)

**⚠️ Note:** This is a workaround for development/testing only. The current implementation expects an ID token, but you can temporarily modify the security to accept custom tokens for testing.

**Temporary Fix for Testing:**
1. The custom token from `/verify-otp` can be used directly in Postman
2. However, `verify_id_token` will fail because it expects an ID token
3. You may need to modify the security layer temporarily for testing

---

## 📋 Summary

1. **POST `/registration`** → Get `sessionInfo`
2. **POST `/verify-otp`** → Get `accessToken` (custom token)
3. **Client exchanges custom token** → Get ID token (using Firebase SDK)
4. **POST `/create-account`** → Use ID token as `Authorization: Bearer <token>`

---

## 🚨 Current Issue

The `/create-account` endpoint uses `get_current_user` which calls `verify_id_token()`. This expects a Firebase ID token, not a custom token.

**For proper implementation:**
- Custom tokens must be exchanged for ID tokens on the client side
- The ID token is what should be sent to protected endpoints

**For testing/development:**
- You may need to create a test endpoint that accepts custom tokens
- Or modify the security layer to handle both token types

---

## 💡 Recommended Solution

For API testing, create a test endpoint that accepts the custom token directly:

```python
@router.post("/test-create-account", status_code=status.HTTP_201_CREATED)
async def test_create_account(
    request: CreateAccountRequest,
    token: str = Header(..., alias="X-Custom-Token")
):
    """Test endpoint that accepts custom token directly"""
    # Verify custom token and extract user_id
    # Then create account
    pass
```

Or modify the security to handle custom tokens for development.

