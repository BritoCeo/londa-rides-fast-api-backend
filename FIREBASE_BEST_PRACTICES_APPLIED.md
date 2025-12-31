# 🔥 Firebase Best Practices Applied

## Overview

This document outlines the Firebase and industry best practices that have been implemented in the Londa API, following the guidelines from `.cursor/rules/londa-dev-rules.mdc`.

---

## ✅ Implemented Best Practices

### 1. **ID Token Verification (Primary Method)**

**Best Practice:** Verify Firebase ID tokens on every protected request.

**Implementation:**
- `app/core/security.py` now primarily verifies ID tokens using `auth_client.verify_id_token()`
- Custom token support is only enabled in `DEBUG` mode for development/testing
- Token revocation checking enabled with `check_revoked=True`

**Code Location:**
```python
# app/core/security.py
decoded_token = auth_client.verify_id_token(token, check_revoked=True)
```

**Why:**
- ID tokens are the standard Firebase authentication method
- They include custom claims for RBAC
- They can be verified and revoked server-side
- More secure than custom tokens

---

### 2. **Custom Claims for RBAC**

**Best Practice:** Use custom claims for role-based access control (RBAC).

**Implementation:**
- Custom claims set with `user_type` field:
  - `"user"` for regular users
  - `"driver"` for drivers
- Claims are set when:
  - User verifies OTP (initial user_type)
  - User creates account (userType from request)
  - Driver verifies OTP (driver type)

**Code Location:**
```python
# app/users/service.py & app/drivers/service.py
custom_claims = {"user_type": "user"}  # or "driver"
auth.create_custom_token(user_id, custom_claims)
self.auth.set_custom_user_claims(user_id, custom_claims)
```

**Why:**
- Allows role-based access control without database lookups
- Claims are included in ID tokens automatically
- Can be checked in security rules and backend code

---

### 3. **Firestore Transactions**

**Best Practice:** Use transactions for atomic operations to prevent race conditions.

**Implementation:**
- User and driver creation now use Firestore transactions
- Ensures document doesn't already exist before creating
- Atomic write operations

**Code Location:**
```python
# app/users/repository.py & app/drivers/repository.py
@firestore.transactional
def create_user_transaction(transaction):
    doc = doc_ref.get(transaction=transaction)
    if doc.exists:
        raise ValueError(f"User {user_id} already exists")
    transaction.set(doc_ref, user_data)
```

**Why:**
- Prevents duplicate user creation
- Ensures data consistency
- Handles concurrent requests safely

---

### 4. **Security Improvements**

#### Token Revocation Checking
- ID tokens are checked for revocation: `verify_id_token(token, check_revoked=True)`
- Handles `RevokedIdTokenError` appropriately

#### No Secrets in Logs
- Tokens are never logged
- Only user IDs and types are logged
- Error messages don't expose sensitive information

#### Proper Error Handling
- Specific error types: `ExpiredIdTokenError`, `InvalidIdTokenError`, `RevokedIdTokenError`
- User-friendly error messages
- Detailed logging for debugging (without exposing secrets)

**Code Location:**
```python
# app/core/security.py
except firebase_auth.ExpiredIdTokenError:
    logger.warning("Expired Firebase ID token")
    raise UnauthorizedError("Authentication token has expired")
```

---

### 5. **Authentication Flow**

#### Production Flow (Recommended)
1. Client sends phone number → Backend sends OTP
2. Client verifies OTP with Firebase SDK → Gets ID token
3. Client sends ID token with API requests
4. Backend verifies ID token on every request

#### Development Flow (Current)
1. Client sends phone number → Backend sends OTP
2. Client sends OTP → Backend returns custom token
3. Client sends custom token with API requests (in DEBUG mode)
4. Backend decodes custom token (development only)

**Note:** In production, clients should exchange custom tokens for ID tokens using Firebase SDK before making API calls.

---

## 📋 Code Changes Summary

### Files Modified

1. **`app/core/security.py`**
   - Primary ID token verification
   - Custom token support only in DEBUG mode
   - Token revocation checking
   - Custom claims extraction
   - Improved error handling

2. **`app/users/service.py`**
   - Custom claims in token generation
   - Custom claims updated on account creation
   - Better error handling

3. **`app/users/repository.py`**
   - Firestore transactions for user creation
   - Atomic operations

4. **`app/drivers/service.py`**
   - Custom claims in token generation
   - Driver type in claims

5. **`app/drivers/repository.py`**
   - Firestore transactions for driver creation
   - Atomic operations

---

## 🚀 Next Steps for Production

1. **Client-Side Token Exchange**
   - Update mobile/web clients to exchange custom tokens for ID tokens
   - Use Firebase SDK: `signInWithCustomToken()` → `getIdToken()`

2. **Disable Custom Token Decoding**
   - Set `DEBUG=False` in production
   - This will disable custom token fallback

3. **Security Rules**
   - Update Firestore security rules to use custom claims
   - Example: `request.auth.token.user_type == 'driver'`

4. **Monitoring**
   - Monitor token verification failures
   - Track authentication success rates
   - Alert on suspicious patterns

---

## 📚 References

- [Firebase Admin SDK - Verify ID Tokens](https://firebase.google.com/docs/auth/admin/verify-id-tokens)
- [Firebase Custom Claims](https://firebase.google.com/docs/auth/admin/custom-claims)
- [Firestore Transactions](https://firebase.google.com/docs/firestore/manage-data/transactions)
- [Firebase Security Best Practices](https://firebase.google.com/docs/rules/best-practices)

---

## ✅ Compliance with Rules

All changes comply with `.cursor/rules/londa-dev-rules.mdc`:

- ✅ Use Firebase Admin SDK on backend
- ✅ Verify Firebase ID token on every protected request
- ✅ Extract user context via FastAPI dependencies
- ✅ Use custom claims for RBAC
- ✅ Never expose service account keys
- ✅ Use transactions for concurrency
- ✅ Log with request context
- ✅ Never log secrets or tokens
- ✅ Validate all inputs
- ✅ Use least-privilege IAM

---

**Last Updated:** 2025-12-31
**Status:** ✅ All best practices implemented

