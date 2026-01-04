# 🔐 How to Get Authentication Token

## Overview

This guide explains how to obtain an authentication token for the Londa Rides API. The API uses Firebase Authentication with custom tokens that must be exchanged for ID tokens on the client side.

**⚠️ Important:** The `accessToken` returned by the API is a **Firebase Custom Token**. You must exchange it for an ID token using the Firebase SDK before making authenticated requests.

---

## Quick Start

### For Mobile Apps (React Native, Flutter, iOS, Android)

See the [Frontend Integration Guide](./FRONTEND_INTEGRATION_GUIDE.md) for complete code examples.

### For API Testing (Postman)

1. **POST `/api/v1/registration`** → Get `sessionInfo`
2. **POST `/api/v1/verify-otp`** → Get `accessToken` (custom token)
3. Use the custom token directly in Postman (development mode only)

**Note:** In production, always exchange custom tokens for ID tokens using Firebase SDK.

---

## Complete Authentication Flow

### Step 1: Register User (Send OTP)

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

---

### Step 2: Verify OTP (Get Custom Token)

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

---

### Step 3: Exchange Custom Token for ID Token (Client-Side)

**This step MUST be done on the client using Firebase SDK.**

#### React Native Example

```javascript
import auth from '@react-native-firebase/auth';
import * as SecureStore from 'expo-secure-store';

const customToken = response.data.accessToken; // from Step 2

// Sign in with custom token
const userCredential = await auth().signInWithCustomToken(customToken);

// Get ID token
const idToken = await userCredential.user.getIdToken();

// Save securely
await SecureStore.setItemAsync('auth_token', idToken);
```

#### Flutter Example

```dart
import 'package:firebase_auth/firebase_auth.dart';

final userCredential = await FirebaseAuth.instance.signInWithCustomToken(customToken);
final idToken = await userCredential.user?.getIdToken();
```

#### iOS (Swift) Example

```swift
let userCredential = try await Auth.auth().signIn(withCustomToken: customToken)
let idToken = try await userCredential.user.getIDToken()
```

#### Android (Kotlin) Example

```kotlin
val result = auth.signInWithCustomToken(customToken).await()
val idToken = result.user?.getIdToken(false)?.await()?.token
```

---

### Step 4: Use ID Token for Authenticated Requests

**Example: Get User Profile**

```http
GET /api/v1/me
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

---

## Driver Authentication Flow

The driver flow is similar but uses different endpoints:

1. **POST `/api/v1/driver/send-otp`** → Get `sessionInfo`
2. **POST `/api/v1/driver/verify-otp`** → Get `accessToken` (custom token)
3. **Exchange custom token for ID token** (same as Step 3 above)
4. **Use ID token** for authenticated requests

---

## Token Refresh

ID tokens expire after 1 hour. Implement automatic token refresh:

### React Native Example

```javascript
import auth from '@react-native-firebase/auth';

async function refreshToken() {
  const currentUser = auth().currentUser;
  if (currentUser) {
    // Firebase SDK handles refresh automatically
    const idToken = await currentUser.getIdToken(true); // Force refresh
    return idToken;
  }
  
  // If Firebase refresh fails, use API refresh endpoint
  const oldToken = await SecureStore.getItemAsync('auth_token');
  const response = await fetch(`${API_BASE_URL}/refresh-token`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${oldToken}` }
  });
  
  const data = await response.json();
  const newCustomToken = data.data.accessToken;
  
  // Exchange new custom token for ID token
  const userCredential = await auth().signInWithCustomToken(newCustomToken);
  return await userCredential.user.getIdToken();
}
```

---

## For Postman/API Testing

**Development Mode:** The backend accepts custom tokens directly in development mode for testing convenience.

1. Get custom token from `/verify-otp` or `/driver/verify-otp`
2. Use it directly in `Authorization: Bearer <custom_token>` header
3. The backend will decode it in development mode

**⚠️ Warning:** In production, always use ID tokens. Custom token support in development is for testing only.

---

## Token Storage Best Practices

### ✅ DO:
- Store tokens in secure storage (Keychain, SecureStore, EncryptedSharedPreferences)
- Refresh tokens before expiration
- Use HTTPS in production
- Never log tokens in production

### ❌ DON'T:
- Store tokens in plain text or localStorage
- Include tokens in error logs
- Send custom tokens directly to protected endpoints (in production)

---

## Additional Resources

- [Frontend Integration Guide](./FRONTEND_INTEGRATION_GUIDE.md) - Complete integration examples
- [Authentication Flow Guide](./AUTHENTICATION_FLOW_GUIDE.md) - Step-by-step guide
- [Authentication Flow Explained](./AUTHENTICATION_FLOW_EXPLAINED.md) - Technical details
- [API Documentation](./API_DOCUMENTATION.md) - Full API reference

---

**Need Help?**  
Refer to the [Frontend Integration Guide](./FRONTEND_INTEGRATION_GUIDE.md) for complete code examples for all platforms.
