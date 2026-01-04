# 🔐 Authentication Flow Guide

## Overview

This guide explains how to authenticate with the Londa Rides API. The API uses Firebase Authentication with custom tokens that must be exchanged for ID tokens on the client side before making authenticated requests.

**⚠️ Important:** The `accessToken` returned by `/verify-otp` and `/driver/verify-otp` is a **Firebase Custom Token**, not an ID token. You must exchange it for an ID token using the Firebase SDK before making authenticated API calls.

---

## Complete Authentication Flow

### Step 1: Register User (Send OTP) 📱

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

**Save:** `sessionInfo` from the response for Step 2.

---

### Step 2: Verify OTP (Get Custom Token) 🔑

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

**⚠️ IMPORTANT:** The `accessToken` is a **Firebase Custom Token**, not an ID token. You must exchange it for an ID token in Step 3.

---

### Step 3: Exchange Custom Token for ID Token (Client-Side) 🔄

**This step MUST be done on the client using Firebase SDK. The backend cannot exchange tokens for you.**

#### React Native Example

```javascript
import auth from '@react-native-firebase/auth';
import * as SecureStore from 'expo-secure-store';

async function exchangeTokenForIDToken(customToken) {
  try {
    // Sign in with custom token
    const userCredential = await auth().signInWithCustomToken(customToken);
    
    // Get ID token
    const idToken = await userCredential.user.getIdToken();
    
    // Save ID token securely
    await SecureStore.setItemAsync('auth_token', idToken);
    await SecureStore.setItemAsync('user_id', userCredential.user.uid);
    
    console.log('Token exchanged successfully');
    return idToken;
  } catch (error) {
    console.error('Token exchange failed:', error);
    throw error;
  }
}

// Usage
const customToken = response.data.accessToken; // from Step 2
const idToken = await exchangeTokenForIDToken(customToken);
```

#### Flutter Example

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

Future<String> exchangeTokenForIDToken(String customToken) async {
  try {
    final userCredential = await FirebaseAuth.instance.signInWithCustomToken(customToken);
    final idToken = await userCredential.user?.getIdToken();
    
    if (idToken == null) {
      throw Exception('Failed to get ID token');
    }
    
    // Save ID token securely
    const storage = FlutterSecureStorage();
    await storage.write(key: 'auth_token', value: idToken);
    await storage.write(key: 'user_id', value: userCredential.user!.uid);
    
    return idToken;
  } catch (e) {
    print('Token exchange failed: $e');
    rethrow;
  }
}
```

#### iOS (Swift) Example

```swift
import FirebaseAuth

func exchangeTokenForIDToken(customToken: String) async throws -> String {
    let userCredential = try await Auth.auth().signIn(withCustomToken: customToken)
    guard let idToken = try await userCredential.user.getIDToken() else {
        throw NSError(domain: "AuthError", code: -1, userInfo: [NSLocalizedDescriptionKey: "Failed to get ID token"])
    }
    
    // Save to Keychain
    let keychain = Keychain(service: "com.londarides.app")
    try keychain.set(idToken, key: "auth_token")
    try keychain.set(userCredential.user.uid, key: "user_id")
    
    return idToken
}
```

#### Android (Kotlin) Example

```kotlin
import com.google.firebase.auth.FirebaseAuth

suspend fun exchangeTokenForIDToken(customToken: String): String {
    val auth = FirebaseAuth.getInstance()
    val result = auth.signInWithCustomToken(customToken).await()
    val idToken = result.user?.getIdToken(false)?.await()?.token
        ?: throw Exception("Failed to get ID token")
    
    // Save to EncryptedSharedPreferences
    val prefs = EncryptedSharedPreferences.create(
        "auth_prefs",
        MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build(),
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    ).edit()
    prefs.putString("auth_token", idToken)
    prefs.putString("user_id", result.user?.uid)
    prefs.apply()
    
    return idToken
}
```

#### Web (JavaScript) Example

```javascript
import { getAuth, signInWithCustomToken } from "firebase/auth";

const auth = getAuth();

async function exchangeTokenForIDToken(customToken) {
  try {
    const userCredential = await signInWithCustomToken(auth, customToken);
    const idToken = await userCredential.user.getIdToken();
    
    // Save to localStorage (or sessionStorage for better security)
    localStorage.setItem('auth_token', idToken);
    localStorage.setItem('user_id', userCredential.user.uid);
    
    return idToken;
  } catch (error) {
    console.error('Token exchange failed:', error);
    throw error;
  }
}
```

---

### Step 4: Create Account (Use ID Token) ✅

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

**Note:** `user_id` is automatically extracted from the authentication token. Do NOT include it in the request body.

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
    "createdAt": "2025-01-01T00:00:00.000000",
    "updatedAt": "2025-01-01T00:00:00.000000"
  },
  "timestamp": "2025-01-01T00:00:00.000000"
}
```

---

## Driver Authentication Flow

The driver authentication flow is similar but uses different endpoints:

1. **POST `/api/v1/driver/send-otp`** → Get `sessionInfo`
2. **POST `/api/v1/driver/verify-otp`** → Get `accessToken` (custom token)
3. **Exchange custom token for ID token** (same as Step 3 above)
4. **POST `/api/v1/driver/create-account`** → Use ID token

**Driver Create Account Request:**
```json
{
  "phone_number": "+264813442530",
  "email": "driver@example.com",
  "name": "Driver Name",
  "license_number": "DL123456",
  "vehicle_model": "Toyota Corolla",
  "vehicle_plate": "ABC-123",
  "vehicle_color": "White"
}
```

---

## Token Refresh

ID tokens expire after 1 hour. Implement automatic token refresh:

### React Native Example

```javascript
import auth from '@react-native-firebase/auth';

async function refreshAuthToken() {
  try {
    const currentUser = auth().currentUser;
    if (!currentUser) {
      throw new Error('No authenticated user');
    }
    
    // Get fresh ID token (Firebase SDK handles refresh automatically)
    const idToken = await currentUser.getIdToken(true); // Force refresh
    await SecureStore.setItemAsync('auth_token', idToken);
    return idToken;
  } catch (error) {
    // If Firebase refresh fails, use API refresh endpoint
    const oldToken = await SecureStore.getItemAsync('auth_token');
    
    const response = await fetch(`${API_BASE_URL}/refresh-token`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${oldToken}`
      }
    });
    
    const data = await response.json();
    const newCustomToken = data.data.accessToken;
    
    // Exchange new custom token for ID token
    const userCredential = await auth().signInWithCustomToken(newCustomToken);
    const newIdToken = await userCredential.user.getIdToken();
    await SecureStore.setItemAsync('auth_token', newIdToken);
    return newIdToken;
  }
}
```

---

## 🔧 For Postman/API Testing

**Note:** The backend accepts both ID tokens (production) and custom tokens (development mode only). For testing in Postman:

1. Get custom token from `/verify-otp` or `/driver/verify-otp`
2. Use it directly in the `Authorization: Bearer <custom_token>` header
3. The backend will decode it in development mode

**⚠️ Warning:** In production, always use ID tokens. Custom token support in development is for testing convenience only.

---

## 📋 Complete Flow Summary

### User Flow:
1. **POST `/api/v1/registration`** → Get `sessionInfo`
2. **POST `/api/v1/verify-otp`** → Get `accessToken` (custom token)
3. **Client exchanges custom token** → Get ID token (using Firebase SDK)
4. **POST `/api/v1/create-account`** → Use ID token as `Authorization: Bearer <token>`
5. **All subsequent requests** → Use ID token in Authorization header

### Driver Flow:
1. **POST `/api/v1/driver/send-otp`** → Get `sessionInfo`
2. **POST `/api/v1/driver/verify-otp`** → Get `accessToken` (custom token)
3. **Client exchanges custom token** → Get ID token (using Firebase SDK)
4. **POST `/api/v1/driver/create-account`** → Use ID token as `Authorization: Bearer <token>`
5. **All subsequent requests** → Use ID token in Authorization header

---

## 🔐 Security Best Practices

1. **✅ DO:**
   - Exchange custom tokens for ID tokens on the client side
   - Store ID tokens in secure storage (Keychain, SecureStore, EncryptedSharedPreferences)
   - Refresh tokens before expiration
   - Use HTTPS in production

2. **❌ DON'T:**
   - Store tokens in plain text or localStorage
   - Log tokens in production
   - Send custom tokens directly to protected endpoints (in production)
   - Include `user_id` or `driver_id` in request bodies (they come from the token)

---

## 📚 Additional Resources

- [Frontend Integration Guide](./FRONTEND_INTEGRATION_GUIDE.md) - Complete integration examples
- [API Documentation](./API_DOCUMENTATION.md) - Full API reference
- [Authentication Flow Explained](./AUTHENTICATION_FLOW_EXPLAINED.md) - Detailed technical explanation
- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)

---

**Need Help?**  
Refer to the [Frontend Integration Guide](./FRONTEND_INTEGRATION_GUIDE.md) for complete code examples for all platforms.

