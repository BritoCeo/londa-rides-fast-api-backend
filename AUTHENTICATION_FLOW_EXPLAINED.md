# 🔐 Authentication Flow - Explained

## Why "User not found in Firebase Auth" Error?

### The Issue

When you're creating a new account, the system does this:

1. **`/verify-otp`** checks if user exists in **Firestore** (database)
2. If user exists in Firestore → Uses that `user_id`
3. If user doesn't exist → Creates new Firebase Auth user
4. Generates custom token with `user_id`

**The Problem:**
- If you tested before, a user document might exist in **Firestore** (database)
- But that user might NOT exist in **Firebase Auth** (authentication service)
- The code uses the Firestore `user_id` to generate a token
- But when verifying the token, it can't find that user in Firebase Auth
- Result: "User not found in Firebase Auth" error

---

## Two Separate Systems

### Firebase Auth (Authentication)
- Manages user authentication
- Stores user credentials (phone, email)
- Generates tokens
- **User must exist here to verify tokens**

### Firestore (Database)
- Stores user profile data
- Stores rides, subscriptions, etc.
- **User document can exist here independently**

### The Problem
- User document in Firestore ≠ User in Firebase Auth
- They need to be in sync!

---

## What Was Fixed

The code now:
1. ✅ Checks if user exists in Firestore
2. ✅ If yes, verifies they also exist in Firebase Auth
3. ✅ If not in Auth, creates the Auth user automatically
4. ✅ Then generates the token

This ensures both systems are in sync!

---

## For New Accounts

**Flow for a completely new user:**

1. **POST `/registration`** → Creates session
2. **POST `/verify-otp`** → 
   - User doesn't exist in Firestore
   - Creates Firebase Auth user ✅
   - Creates Firestore document ✅
   - Returns custom token ✅
3. **POST `/create-account`** → 
   - Uses token to authenticate
   - Updates Firestore document with full details ✅

---

## For Existing Users (From Previous Tests)

**Flow if user document exists in Firestore:**

1. **POST `/registration`** → Creates session
2. **POST `/verify-otp`** → 
   - User exists in Firestore
   - **Now checks if user exists in Firebase Auth** ✅
   - If not, creates Auth user automatically ✅
   - Returns custom token ✅
3. **POST `/create-account`** → 
   - Uses token to authenticate
   - Updates existing Firestore document ✅

---

## Summary

**Before Fix:**
- User in Firestore but not in Auth → Error ❌

**After Fix:**
- User in Firestore but not in Auth → Auto-creates Auth user ✅
- Everything stays in sync ✅

**You're creating a new account, but if you tested before, there might be leftover data in Firestore. The fix ensures both systems are synchronized!**

