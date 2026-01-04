# 🚗 Driver Authentication & Subscription Guide

## 📋 **Important: Driver ID is Extracted from Authentication Token**

**⚠️ Security Note:** The `driver_id` is automatically extracted from your authentication token. You do NOT need to (and should NOT) include it in request bodies for protected endpoints.

## 🔐 **How Authentication Works**

### **Method 1: Complete Driver Registration Flow** (Recommended)

#### **Step 1: Send OTP to Driver Phone**
```bash
POST /api/v1/driver/send-otp
Content-Type: application/json

{
  "phone_number": "+264813442530"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully (Firebase Development mode)",
  "sessionInfo": "session_123456789"
}
```

#### **Step 2: Verify OTP**
```bash
POST /api/v1/driver/verify-otp
Content-Type: application/json

{
  "phone_number": "+264813442530",
  "otp": "1234",
  "sessionInfo": "session_123456789"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "driver": {
      "id": "driver_abc123xyz",
      "phone_number": "+264813442530",
      "isVerified": true
    }
  }
}
```

#### **Step 3: Complete Driver Registration**
```bash
POST /api/v1/driver/registration-driver
Content-Type: application/json

{
  "otp": "1234",
  "token": "jwt_token_from_step2"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Driver registered successfully",
  "data": {
    "driver": {
      "id": "driver_abc123xyz",
      "name": "John Driver",
      "phone_number": "+264813442530",
      "email": "john@example.com",
      "license_number": "DL123456789",
      "vehicle_type": "Car",
      "vehicle_model": "Toyota Corolla",
      "vehicle_year": 2020,
      "vehicle_color": "White",
      "vehicle_plate": "NA12345",
      "isVerified": true
    }
  }
}
```

#### **Step 4: Create Subscription (Driver ID Extracted from Token)**
```bash
POST /api/v1/driver/subscription
Content-Type: application/json
Authorization: Bearer YOUR_ID_TOKEN

{
  "payment_method": "cash"
}
```

**Note:** The `driver_id` is automatically extracted from the Bearer token. The backend retrieves it from `current_driver["uid"]` after verifying your authentication token.

### **Method 2: Using Firebase SDK** (Mobile Apps)

For mobile applications, exchange the custom token for an ID token:

**React Native Example:**
```javascript
import auth from '@react-native-firebase/auth';

// After getting accessToken from /driver/verify-otp
const userCredential = await auth().signInWithCustomToken(accessToken);
const idToken = await userCredential.user.getIdToken();

// Use idToken for API requests
const response = await fetch('https://api.londarides.com/api/v1/driver/subscription', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${idToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    payment_method: 'cash'
  })
});
```

**Note:** The driver_id is automatically extracted from the idToken on the backend.

## 🔧 **Available Driver Endpoints**

### **Driver Registration (Public):**
- ✅ `POST /api/v1/driver/send-otp` - Send OTP to driver phone
- ✅ `POST /api/v1/driver/verify-otp` - Verify OTP for registration
- ✅ `POST /api/v1/driver/login` - Driver login (alias for verify-otp)
- ✅ `POST /api/v1/driver/create-account` - Complete driver registration (requires auth)

### **Driver Subscription (Protected - driver_id from token):**
- ✅ `POST /api/v1/driver/subscription` - Create subscription (no driver_id in body)
- ✅ `GET /api/v1/driver/subscription` - Get own subscription status (no driver_id needed)
- ✅ `GET /api/v1/driver/subscription/{driver_id}` - Get subscription by ID (path param)
- ✅ `PUT /api/v1/driver/subscription/{driver_id}` - Update subscription (path param)
- ✅ `POST /api/v1/driver/subscription/payment` - Process payment (no driver_id in body)
- ✅ `GET /api/v1/driver/subscription/history/{driver_id}` - Get history (path param)
- ✅ `DELETE /api/v1/driver/subscription/{driver_id}` - Cancel subscription (path param)

### **Driver Management (Protected - driver_id from token):**
- ✅ `GET /api/v1/driver/me` - Get driver profile
- ✅ `PUT /api/v1/driver/update-status` - Update driver status
- ✅ `GET /api/v1/driver/available-rides` - Get available rides
- ✅ `POST /api/v1/driver/accept-ride` - Accept a ride
- ✅ `POST /api/v1/driver/start-ride` - Start a ride
- ✅ `POST /api/v1/driver/complete-ride` - Complete a ride

## 🧪 **Testing with Postman**

### **1. Import Collection**
Import the `Londa_Rides_API_Collection.postman_collection.json` file into Postman.

### **2. Set Variables**
- `base_url`: `http://localhost:8000`
- `driver_id`: Will be set automatically after driver creation

### **3. Test Flow**
1. **Send Driver OTP**: `POST /api/v1/driver/send-otp`
2. **Verify Driver OTP**: `POST /api/v1/driver/verify-otp`
3. **Complete Registration**: `POST /api/v1/driver/registration-driver`
4. **Create Subscription**: `POST /api/v1/driver/subscription`

## 🎯 **Quick Test Commands**

### **Using curl:**
```bash
# Step 1: Send OTP
curl -X POST http://localhost:8000/api/v1/driver/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530"}'

# Step 2: Verify OTP (use sessionInfo from step 1)
curl -X POST http://localhost:8000/api/v1/driver/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530", "otp": "1234", "sessionInfo": "session_123456789"}'

# Step 3: Create subscription (driver_id extracted from token)
curl -X POST http://localhost:8000/api/v1/driver/subscription \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ID_TOKEN" \
  -d '{"payment_method": "cash"}'
```

## 🚨 **Common Issues**

### **1. "Route not found"**
- ✅ Use correct endpoint: `/api/v1/driver/send-otp` (not `/registration`)
- ✅ Check server is running on port 8000

### **2. "Invalid session"**
- ✅ Include `sessionInfo` from OTP response
- ✅ Use the same phone number in both requests

### **3. "Bearer token invalid"**
- ✅ Complete the full registration flow
- ✅ Use the driver ID from registration response

## 🎉 **Result**

Once you complete the driver registration flow, you'll have an authentication token that contains your driver_id. The backend automatically extracts it for all protected endpoints:

**Request Body (What you send):**
```json
{
  "payment_method": "cash"
}
```

**What happens on the backend:**
```python
# Backend automatically extracts driver_id from token
request.driver_id = current_driver["uid"]  # From Bearer token
subscription = await service.create_subscription(request)
```

**Security Benefits:**
- ✅ Drivers cannot make requests on behalf of other drivers
- ✅ No need to manually pass driver_id (reduces errors)
- ✅ Token-based authentication ensures security
- ✅ Consistent with REST API best practices

The driver ID is generated during registration and is securely stored in your authentication token! 🚀
