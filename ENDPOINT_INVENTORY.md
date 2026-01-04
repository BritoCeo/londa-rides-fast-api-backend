# Londa Rides API - Complete Endpoint Inventory

**Generated:** 2025-01-XX  
**Base URL:** `http://localhost:8000/api/v1` (Development)  
**Production URL:** `https://api.londarides.com/api/v1` (Production)

## Endpoint Summary

### Health & Status (2 endpoints)
- `GET /health` - Health check
- `GET /test` - API test endpoint

### User Authentication (9 endpoints)
- `POST /api/v1/registration` - Register user (send OTP)
- `POST /api/v1/verify-otp` - Verify OTP (login)
- `POST /api/v1/login` - User login (alias for verify-otp)
- `POST /api/v1/email-otp-request` - Request email OTP
- `PUT /api/v1/email-otp-verify` - Verify email OTP
- `POST /api/v1/create-account` - Create user account (requires auth)
- `POST /api/v1/refresh-token` - Refresh authentication token (requires auth)
- `GET /api/v1/me` - Get current user profile (requires auth)
- `PUT /api/v1/update-profile` - Update user profile (requires auth)
- `POST /api/v1/update-location` - Update user location (requires auth)

### User Ride Management (6 endpoints)
- `POST /api/v1/request-ride` - Request a ride (requires auth)
- `GET /api/v1/nearby-drivers` - Get nearby drivers (requires auth)
- `POST /api/v1/cancel-ride` - Cancel ride (requires auth)
- `PUT /api/v1/rate-ride` - Rate completed ride (requires auth)
- `GET /api/v1/ride-status/{ride_id}` - Get ride status (requires auth)
- `GET /api/v1/get-rides` - Get all user rides (requires auth)

### Driver Authentication (7 endpoints)
- `POST /api/v1/driver/send-otp` - Send driver OTP
- `POST /api/v1/driver/verify-otp` - Verify driver OTP
- `POST /api/v1/driver/login` - Driver login (alias for verify-otp)
- `POST /api/v1/driver/create-account` - Create driver account (requires auth)
- `GET /api/v1/driver/me` - Get current driver profile (requires auth)
- `PUT /api/v1/driver/update-status` - Update driver status (requires auth)
- `POST /api/v1/driver/update-location` - Update driver location (requires auth)

### Driver Ride Management (6 endpoints)
- `GET /api/v1/driver/available-rides` - Get available rides (requires auth)
- `POST /api/v1/driver/accept-ride` - Accept ride (requires auth)
- `POST /api/v1/driver/decline-ride` - Decline ride (requires auth)
- `POST /api/v1/driver/start-ride` - Start ride (requires auth)
- `POST /api/v1/driver/complete-ride` - Complete ride (requires auth)
- `GET /api/v1/driver/get-rides` - Get driver rides (requires auth)

### Driver Subscription (6 endpoints)
- `POST /api/v1/driver/subscription` - Create driver subscription (requires auth)
- `GET /api/v1/driver/subscription` - Get driver subscription status (requires auth)
- `GET /api/v1/driver/subscription/{driver_id}` - Get subscription by ID (requires auth)
- `PUT /api/v1/driver/subscription/{driver_id}` - Update subscription (requires auth)
- `POST /api/v1/driver/subscription/payment` - Process subscription payment (requires auth)
- `GET /api/v1/driver/subscription/history/{driver_id}` - Get payment history (requires auth)

### Parent Subscription (7 endpoints)
- `POST /api/v1/parent/subscribe` - Subscribe to parent package (requires auth)
- `GET /api/v1/parent/subscription` - Get subscription status (requires auth)
- `PUT /api/v1/parent/subscription` - Update subscription (requires auth)
- `DELETE /api/v1/parent/subscription` - Cancel subscription (requires auth)
- `GET /api/v1/parent/usage` - Get usage statistics (requires auth)
- `GET /api/v1/parent/children` - Get children profiles (requires auth)
- `POST /api/v1/parent/children` - Add child profile (requires auth)

### Payment Management (4 endpoints)
- `POST /api/v1/payment/calculate-fare` - Calculate fare (requires auth)
- `POST /api/v1/payment/process` - Process payment (requires auth)
- `GET /api/v1/payment/history` - Get payment history (requires auth)
- `POST /api/v1/subscribe-monthly` - Subscribe monthly (requires auth)

### Analytics (5 endpoints)
- `GET /api/v1/analytics/rides` - Get user ride analytics (requires auth)
- `GET /api/v1/analytics/performance` - Get user performance analytics (requires auth)
- `GET /api/v1/driver/analytics/earnings` - Get driver earnings (requires auth)
- `GET /api/v1/driver/analytics/rides` - Get driver ride analytics (requires auth)
- `GET /api/v1/driver/analytics/performance` - Get driver performance analytics (requires auth)

**Total: 52 endpoints**

## Authentication Requirements

### Public Endpoints (No Auth Required)
- `GET /health`
- `GET /test`
- `POST /api/v1/registration`
- `POST /api/v1/verify-otp`
- `POST /api/v1/login`
- `POST /api/v1/email-otp-request`
- `PUT /api/v1/email-otp-verify`
- `POST /api/v1/driver/send-otp`
- `POST /api/v1/driver/verify-otp`
- `POST /api/v1/driver/login`

### Protected Endpoints (Auth Required)
All other endpoints require `Authorization: Bearer <token>` header.

### Driver-Only Endpoints (Require Driver Auth)
- All `/api/v1/driver/*` endpoints (except send-otp, verify-otp, login)
- `GET /api/v1/driver/analytics/*`
- `POST /api/v1/driver/subscription/*`
- `GET /api/v1/driver/subscription/*`
- `PUT /api/v1/driver/subscription/*`

## Notes

1. **User ID/Driver ID**: Many endpoints automatically extract `user_id` or `driver_id` from the authentication token. Do NOT include these in request bodies.

2. **Field Naming**: 
   - Request bodies use snake_case (e.g., `phone_number`, `user_id`)
   - Response bodies use camelCase (e.g., `phoneNumber`, `userId`)
   - Some fields use mixed conventions (e.g., `sessionInfo`, `rideId`)

3. **Response Format**: All responses follow this structure:
   ```json
   {
     "success": true,
     "message": "...",
     "data": {...},
     "timestamp": "ISO8601"
   }
   ```

