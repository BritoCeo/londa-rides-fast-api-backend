# 🚗 Driver Subscription Management API Documentation

## 📋 Overview

The Driver Subscription Management APIs handle the monthly subscription system for drivers on the Londa Rides platform. According to the business rules, drivers must pay a monthly subscription fee of **NAD 150.00** to access and offer rides through the platform.

## 🎯 Business Rules

- **Driver Subscription Fee**: NAD 150.00 per month
- **Payment Methods**: Cash only
- **Subscription Status**: Active drivers can offer rides
- **Auto-renewal**: Optional automatic renewal
- **Payment History**: Track all subscription payments

## 🔗 API Endpoints

### 1. Create Driver Subscription
**POST** `/api/v1/driver/subscription`

Creates a new driver subscription with payment processing.

**Authentication:** Required (Bearer token - Driver)

**⚠️ Security Note:** The `driver_id` is automatically extracted from the authentication token. Do NOT include it in the request body.

#### Request Body
```json
{
  "payment_method": "cash"
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `payment_method` | string | Yes | Payment method (currently only "cash" is supported) |

#### Response (201 Created)
```json
{
  "success": true,
  "message": "Driver subscription created successfully",
  "data": {
    "subscription": {
      "id": "sub_123456789",
      "driver_id": "driver_123",
      "amount": 150.00,
      "currency": "NAD",
      "status": "active",
      "subscription_type": "monthly",
      "start_date": "2024-01-01T00:00:00.000Z",
      "end_date": "2024-01-31T23:59:59.999Z",
      "payment_method": "cash",
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    },
    "payment": {
      "transaction_id": "txn_123456789",
      "amount": 150.00,
      "currency": "NAD",
      "status": "completed"
    }
  }
}
```

### 2. Get Driver Subscription Status
**GET** `/api/v1/driver/subscription/{driver_id}`

Retrieves the current subscription status for a driver.

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Driver subscription retrieved successfully",
  "data": {
    "subscription": {
      "id": "sub_123456789",
      "driver_id": "driver_123",
      "amount": 150.00,
      "currency": "NAD",
      "status": "active",
      "subscription_type": "monthly",
      "start_date": "2024-01-01T00:00:00.000Z",
      "end_date": "2024-01-31T23:59:59.999Z",
      "payment_method": "cash",
      "auto_renew": true,
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    },
    "status": {
      "is_active": true,
      "days_remaining": 15,
      "expires_on": "2024-01-31T23:59:59.999Z",
      "auto_renew": true
    }
  }
}
```

### 3. Update Driver Subscription
**PUT** `/api/v1/driver/subscription/{driver_id}`

Updates driver subscription settings.

#### Request Body
```json
{
  "auto_renew": true,
  "payment_method": "cash",
  "notification_preferences": {
    "email": true,
    "sms": true,
    "push": true
  }
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Driver subscription updated successfully",
  "data": {
    "subscription": {
      "id": "sub_123456789",
      "driver_id": "driver_123",
      "auto_renew": true,
      "payment_method": "cash",
      "notification_preferences": {
        "email": true,
        "sms": true,
        "push": true
      },
      "updated_at": "2024-01-01T12:00:00.000Z"
    }
  }
}
```

### 4. Process Subscription Payment
**POST** `/api/v1/driver/subscription/payment`

Processes a payment for driver subscription.

**Authentication:** Required (Bearer token - Driver)

**⚠️ Security Note:** The `driver_id` is automatically extracted from the authentication token. Do NOT include it in the request body.

#### Request Body
```json
{
  "payment_method": "cash",
  "amount": 150.00
}
```

#### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `payment_method` | string | Yes | Payment method (currently only "cash" is supported) |
| `amount` | float | Yes | Amount in NAD (must be exactly 150.00) |

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Subscription payment processed successfully",
  "data": {
    "subscription": {
      "id": "sub_123456789",
      "driver_id": "driver_123",
      "status": "active",
      "payment_date": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    },
    "payment": {
      "id": "pay_123456789",
      "user_id": "driver_123",
      "amount": 150.00,
      "currency": "NAD",
      "payment_method": "cash",
      "status": "completed",
      "transaction_id": "txn_123456789",
      "payment_type": "driver_subscription"
    }
  }
}
```

### 5. Get Driver Subscription History
**GET** `/api/v1/driver/subscription/history/{driver_id}`

Retrieves the subscription payment history for a driver.

#### Query Parameters
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10, max: 100)
- `start_date` (optional): Start date filter (YYYY-MM-DD)
- `end_date` (optional): End date filter (YYYY-MM-DD)

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Driver subscription history retrieved successfully",
  "data": {
    "history": [
      {
        "id": "sub_123456789",
        "driver_id": "driver_123",
        "amount": 150.00,
        "currency": "NAD",
        "status": "active",
        "payment_method": "cash",
        "created_at": "2024-01-01T00:00:00.000Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1
    },
    "summary": {
      "total_payments": 1,
      "total_amount": 150.00,
      "currency": "NAD"
    }
  }
}
```

## 🔒 Authentication

All endpoints require authentication. Include the bearer token in the Authorization header:

```
Authorization: Bearer <your_firebase_id_token>
```

**Important Notes:**
- The `driver_id` is automatically extracted from the authentication token
- Do NOT include `driver_id` in request bodies for protected endpoints
- This prevents drivers from making requests on behalf of other drivers
- For token generation, see the [Authentication Flow Guide](../AUTHENTICATION_FLOW_EXPLAINED.md)

## ✅ Validation Rules

### Create Driver Subscription
- `payment_method`: Required, must be `cash`
- **Note:** `driver_id` is extracted from authentication token, not request body

### Update Driver Subscription
- `auto_renew`: Optional, must be a boolean
- `payment_method`: Optional, must be `cash`
- `notification_preferences`: Optional, must be an object

### Process Subscription Payment
- `payment_method`: Required, must be `cash`
- `amount`: Required, must be exactly 150.00
- **Note:** `driver_id` is extracted from authentication token, not request body

## 🚨 Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Validation error message",
  "errors": [
    {
      "field": "payment_method",
      "message": "Invalid payment method"
    }
  ]
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Driver not found"
}
```

### 409 Conflict
```json
{
  "success": false,
  "message": "Driver already has an active subscription"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Failed to create driver subscription",
  "error": "Error details"
}
```

## 🧪 Testing

Run the driver subscription API tests:

```bash
# Test all driver subscription APIs
npm run test:driver-subscription

# Test specific functionality
node test/test-driver-subscription-apis.js
```

## 📊 Business Logic

### Subscription Lifecycle
1. **Creation**: Driver creates subscription with payment
2. **Activation**: Subscription becomes active after successful payment
3. **Renewal**: Auto-renewal or manual renewal before expiration
4. **Expiration**: Subscription expires after 30 days
5. **Suspension**: Driver cannot offer rides with expired subscription

### Payment Processing
- **Mock Implementation**: Current implementation uses mock payment processing
- **Real Integration**: Replace with actual payment gateway integration
- **Security**: Payment tokens should be handled securely
- **Validation**: Amount must be exactly NAD 150.00

### Driver Status Updates
- **Active Subscription**: Driver can offer rides
- **Expired Subscription**: Driver cannot offer rides
- **Payment Pending**: Driver cannot offer rides until payment is confirmed

## 🔧 Implementation Notes

### Firestore Collections
- **driverSubscriptions**: Stores subscription records
- **payments**: Stores payment records
- **drivers**: Updated with subscription status

### Mock Database Support
- All APIs work with mock database when Firestore is not available
- Mock responses simulate real database behavior
- Useful for development and testing

### Security Considerations
- All endpoints require authentication
- Payment tokens should be encrypted
- Input validation prevents injection attacks
- Rate limiting prevents abuse

## 📈 Future Enhancements

1. **Payment Gateway Integration**: Replace mock with real payment processing
2. **Webhook Support**: Handle payment confirmations via webhooks
3. **Subscription Plans**: Support different subscription tiers
4. **Proration**: Handle mid-month subscription changes
5. **Analytics**: Track subscription metrics and trends
6. **Notifications**: Send subscription reminders and confirmations

## 🎯 Compliance

This implementation follows the Londa Rides CC business rules:
- ✅ Driver subscription fee: NAD 150.00 per month
- ✅ Payment method validation
- ✅ Subscription status management
- ✅ Payment history tracking
- ✅ Auto-renewal support
- ✅ Business rule enforcement

The APIs are ready for production use and can be extended as needed.
