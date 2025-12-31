---
name: Londa API Complete Implementation
overview: Build the complete Londa Rides CC API following SOLID principles, REST standards, and event-driven architecture. Implement all endpoints from the Postman collection using FastAPI, Firebase (Auth/Firestore/FCM), and Google Maps Platform.
todos:
  - id: core-infra
    content: "Set up core infrastructure: config, Firebase Admin SDK, security, logging, exception handlers with standard JSON responses"
    status: completed
  - id: auth-users
    content: "Implement user authentication: OTP (phone/email), verify-otp, create-account, /me endpoint"
    status: completed
    dependencies:
      - core-infra
  - id: auth-drivers
    content: "Implement driver authentication: send-otp, verify-otp, login, create-account, /driver/me"
    status: completed
    dependencies:
      - core-infra
  - id: notifications
    content: Set up FCM notification system for push notifications to drivers and riders
    status: completed
    dependencies:
      - core-infra
  - id: maps
    content: Integrate Google Maps API for geocoding, distance calculation, and route optimization
    status: completed
    dependencies:
      - core-infra
  - id: rides-user
    content: "Implement user ride management: request-ride, nearby-drivers, cancel-ride, rate-ride, ride-status, get-rides"
    status: completed
    dependencies:
      - auth-users
      - notifications
      - maps
  - id: rides-driver
    content: "Implement driver ride management: available-rides, accept-ride, decline-ride, start-ride, complete-ride, get-rides with transaction-based acceptance"
    status: completed
    dependencies:
      - auth-drivers
      - notifications
  - id: subscriptions-driver
    content: "Implement driver subscription: create, get status, update, payment processing (NAD 150/month), history"
    status: completed
    dependencies:
      - auth-drivers
  - id: subscriptions-parent
    content: "Implement parent subscription: subscribe, get status, update, cancel, usage stats, children profiles (NAD 1000/month)"
    status: completed
    dependencies:
      - auth-users
  - id: payments
    content: "Implement payment management: calculate-fare, process payment (cash only, NAD 13/ride), payment history, monthly subscription"
    status: completed
    dependencies:
      - rides-user
      - subscriptions-driver
      - subscriptions-parent
  - id: profiles
    content: "Implement profile management: update user profile/location, update driver status/location"
    status: completed
    dependencies:
      - auth-users
      - auth-drivers
  - id: analytics
    content: "Implement analytics endpoints: user ride/performance analytics, driver earnings/rides/performance analytics"
    status: completed
    dependencies:
      - rides-user
      - rides-driver
      - payments
  - id: health-endpoints
    content: Update health and test endpoints to match standard JSON response format
    status: completed
    dependencies:
      - core-infra
---

# Lo

nda API Complete Implementation Plan

## Architecture Overview

The API follows a layered architecture: **Routes → Services → Repositories** with feature-based organization. All communication is event-driven using FCM push notifications (NO WebSockets).

```javascript
app/
├── core/                    # Core infrastructure
│   ├── config.py           # Environment configuration
│   ├── security.py         # Firebase auth, JWT helpers
│   ├── firebase.py         # Firebase Admin SDK initialization
│   ├── logging.py          # Structured logging
│   └── exceptions.py       # Custom exceptions & handlers
├── users/                   # User domain
│   ├── router.py           # User routes
│   ├── service.py           # User business logic
│   ├── repository.py       # Firestore operations
│   └── schemas.py          # Pydantic models
├── drivers/                 # Driver domain
├── rides/                   # Ride domain
├── subscriptions/           # Subscription domain (driver & parent)
├── payments/                # Payment domain
├── notifications/           # FCM push notifications
│   ├── fcm.py              # FCM service
│   └── service.py          # Notification orchestration
├── maps/                    # Google Maps integration
│   └── service.py           # Maps API wrapper
└── analytics/               # Analytics domain
```



## Implementation Phases

### Phase 1: Core Infrastructure Setup

**Files to create/modify:**

- `app/core/config.py` - Add all environment variables (Firebase, Google Maps, SMTP, Nylas)
- `app/core/firebase.py` - Initialize Firebase Admin SDK
- `app/core/security.py` - Firebase token verification, user context extraction
- `app/core/exceptions.py` - Update to match standard response format with timestamp
- `app/core/logging.py` - Structured JSON logging with correlation IDs
- `requirements.txt` - Add dependencies (firebase-admin, googlemaps, pyfcm, etc.)

**Key features:**

- Firebase Admin SDK initialization with service account
- Standard response wrapper: `{success, message, data?, error?, timestamp}`
- Centralized error handling returning JSON (never HTML)
- Environment variable validation

### Phase 2: Authentication System

**User Authentication (`app/users/`):**

- `router.py` - Routes: `/registration`, `/verify-otp`, `/email-otp-request`, `/email-otp-verify`, `/create-account`, `/me`
- `service.py` - OTP generation/verification, Firebase Auth integration, session management
- `repository.py` - Firestore user document operations
- `schemas.py` - Request/response models for auth flows

**Driver Authentication (`app/drivers/`):**

- `router.py` - Routes: `/driver/send-otp`, `/driver/verify-otp`, `/driver/login`, `/driver/create-account`, `/driver/me`
- `service.py` - Driver-specific auth logic
- `repository.py` - Driver document operations
- `schemas.py` - Driver auth models

**Implementation details:**

- OTP via Firebase Auth (phone) and email (SMTP with Nylas)
- JWT tokens with 30-day expiry (users), 7-day (drivers)
- Session info management for OTP verification
- User types: student, worker, parent

### Phase 3: Notification System

**Files: `app/notifications/`**

- `fcm.py` - FCM client wrapper, token management
- `service.py` - Notification orchestration, batch sending
- Integration with ride events (request, accept, start, complete)

**Features:**

- FCM token storage in Firestore
- Push notifications for ride events
- Background task integration for fan-out

### Phase 4: Maps Integration

**Files: `app/maps/service.py`**

- Google Maps API wrapper
- Geocoding, distance calculation, route optimization
- Caching for geocoding results
- Rate limiting and error handling

### Phase 5: Ride Management

**User Ride Management (`app/rides/`):**

- `router.py` - Routes: `/request-ride`, `/nearby-drivers`, `/cancel-ride`, `/rate-ride`, `/ride-status/{ride_id}`, `/get-rides`
- `service.py` - Ride request logic, driver matching, status transitions
- `repository.py` - Firestore ride operations with transactions
- `schemas.py` - Ride models (pickup/dropoff locations, status enum)
- `events.py` - Event emission for ride state changes

**Driver Ride Management (`app/drivers/rides.py`):**

- Routes: `/driver/available-rides`, `/driver/accept-ride`, `/driver/decline-ride`, `/driver/start-ride`, `/driver/complete-ride`, `/driver/get-rides`
- Transaction-based ride acceptance (first-accept wins)
- Status updates with FCM notifications

**Ride States:**

- `pending` → `accepted` → `started` → `completed` / `cancelled`

### Phase 6: Subscription Management

**Driver Subscription (`app/subscriptions/driver/`):**

- Routes: `/driver/subscription` (POST, GET), `/driver/subscription/{driver_id}`, `/driver/subscription/payment`, `/driver/subscription/history/{driver_id}`
- Amount: NAD 150.00/month, cash only
- Subscription status tracking, expiry management
- Payment history

**Parent Subscription (`app/subscriptions/parent/`):**

- Routes: `/parent/subscribe`, `/parent/subscription`, `/parent/usage`, `/parent/children` (GET, POST)
- Amount: NAD 1000.00/month, unlimited rides
- Child profile management (age 5-18)
- Usage statistics tracking

### Phase 7: Payment Management

**Files: `app/payments/`**

- Routes: `/payment/calculate-fare`, `/payment/process`, `/payment/history`, `/subscribe-monthly`
- Cash-only payment processing
- Default fare: NAD 13.00 per ride
- Payment history with pagination
- Integration with ride completion

### Phase 8: Profile & Settings

**Files: `app/users/profile.py`**

- Routes: `/update-profile`, `/update-location`
- Profile update logic
- Location tracking (throttled updates)

**Files: `app/drivers/profile.py`**

- Routes: `/driver/update-status`, `/driver/update-location`
- Driver status management (online, offline, busy)
- Location updates for nearby driver queries

### Phase 9: Analytics

**Files: `app/analytics/`**

- User analytics: `/analytics/rides`, `/analytics/performance`
- Driver analytics: `/driver/analytics/earnings`, `/driver/analytics/rides`, `/driver/analytics/performance`
- Aggregation queries on Firestore
- Performance metrics calculation

### Phase 10: Health & Test Endpoints

**Files: `app/api/v1/endpoints/health.py`** (update)

- `/health` - Basic health check
- `/test` - API Gateway test (returns standard JSON format)

## Technical Specifications

### Response Format

All endpoints return:

```json
{
  "success": true|false,
  "message": "string",
  "data": {...},  // optional
  "error": {...}, // optional (for errors)
  "timestamp": "ISO string"
}
```



### Error Handling

- All errors return JSON (never HTML)
- HTTP status codes: 200, 201, 400, 401, 403, 404, 409, 422, 500
- Error structure: `{success: false, message: "...", error: {code, details}, timestamp}`

### Firestore Collections

- `users/{userId}` - User documents
- `drivers/{driverId}` - Driver documents
- `rides/{rideId}` - Ride documents
- `driver_subscriptions/{subscriptionId}` - Driver subscriptions
- `parent_subscriptions/{subscriptionId}` - Parent subscriptions
- `payments/{paymentId}` - Payment records
- `fcm_tokens/{userId}` - FCM tokens

### Authentication Flow

1. User/Driver sends phone number → OTP sent
2. User/Driver verifies OTP → JWT token returned
3. Token used in Authorization header: `Bearer {token}`
4. Token verified on each protected request

### Ride Dispatch Flow (Event-Driven)

1. Rider requests ride → Stored in Firestore
2. Event emitted → Background task finds nearby drivers
3. FCM push sent to nearby drivers
4. Driver accepts via REST endpoint → Transaction ensures atomicity
5. Rider notified via FCM

## Dependencies to Add

```txt
firebase-admin==6.5.0
googlemaps==4.10.0
pyfcm==1.5.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
email-validator==2.1.0
phonenumbers==8.13.27
```



## Environment Variables Required

```env
# Firebase
FIREBASE_CREDENTIALS_PATH=path/to/service-account.json
FIREBASE_PROJECT_ID=londa-cd054

# Google Maps
GOOGLE_MAPS_API_KEY=AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=londanase@gmail.com
SMTP_PASS=moxb snfc xvoy hroz
EMAIL_ACTIVATION_SECRET=QQTRjWtG2EUBqj/aQyEUMvtZutQOSGwCVEu5Yr42uyg=

# Nylas (optional)
NYLAS_API_KEY=nyk_v0_QcDKjTkTKFJ48xYkPYGOFdKa3phMIrGQ2fhw9p0RPW9C1iCOHFFUu8QVD7S6n3ID
```



## Testing Strategy

- Unit tests for services (business logic)
- Integration tests for API endpoints
- Firestore emulator for local testing
- Mock Google Maps API responses

## Code Quality Standards

- Functions under 50 lines
- SOLID principles throughout
- Dependency injection via FastAPI `Depends`
- Async/await for all I/O operations
- Type hints on all functions
- Pydantic schemas for validation
- camelCase for API responses (JSON)
- RESTful resource naming

## Implementation Order

1. Core infrastructure (config, Firebase, security, logging)
2. Authentication (users & drivers)
3. Notifications (FCM setup)
4. Maps integration
5. Ride management (core feature)
6. Subscriptions (driver & parent)
7. Payments
8. Profile & settings