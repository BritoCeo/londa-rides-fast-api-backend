# Londa Rides API Documentation

## Base URLs
```
Development: http://localhost:8000/api/v1
Production: https://londa-rides-fast-api-backend.onrender.com/api/v1
```

## Authentication
Most protected endpoints require a bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

Notes:
- Public endpoints include user OTP routes, driver OTP routes, and `POST /api/v1/admin/login`.
- `verify-otp`, `login`, and `refresh-token` return `accessToken`. In the Firebase production flow this is a custom token that the client exchanges for an ID token.
- Protected endpoints derive `user_id` or `driver_id` from the authenticated token unless a path or query parameter explicitly requires an id.

## Current API Surface

### Health & Status
- `GET /health`
- `GET /test`
- `GET /api/v1/health/`
- `GET /api/v1/health/test`

### User Authentication & Profile
- `POST /api/v1/registration`
- `POST /api/v1/verify-otp`
- `POST /api/v1/login`
- `POST /api/v1/email-otp-request`
- `PUT /api/v1/email-otp-verify`
- `POST /api/v1/create-account`
- `GET /api/v1/me`
- `PUT /api/v1/update-profile`
- `POST /api/v1/update-location`
- `POST /api/v1/refresh-token`

### User Ride Management
- `POST /api/v1/request-ride`
- `POST /api/v1/cancel-ride`
- `PUT /api/v1/rate-ride`
- `GET /api/v1/ride-status/{ride_id}`
- `GET /api/v1/get-rides`
- `GET /api/v1/nearby-drivers`
- `GET /api/v1/rides/{ride_id}/messages`
- `GET /api/v1/parent/active-rides`
- `POST /api/v1/rides/schedule`
- `GET /api/v1/rides/scheduled`
- `PUT /api/v1/rides/scheduled/{ride_id}`
- `DELETE /api/v1/rides/scheduled/{ride_id}`
- `GET /api/v1/rides/carpool-matches`
- `POST /api/v1/rides/join-carpool`
- `POST /api/v1/ride/{ride_id}/sos`
- `POST /api/v1/ride/{ride_id}/share-tracking`
- `PUT /api/v1/ride/{ride_id}/stops`

### Driver Authentication & Profile
- `POST /api/v1/driver/send-otp`
- `POST /api/v1/driver/verify-otp`
- `POST /api/v1/driver/login`
- `POST /api/v1/driver/create-account`
- `GET /api/v1/driver/me`
- `PUT /api/v1/driver/update-status`
- `POST /api/v1/driver/update-location`
- `POST /api/v1/driver/documents`
- `GET /api/v1/driver/documents/status`
- `GET /api/v1/driver/vehicle`
- `PUT /api/v1/driver/vehicle`
- `POST /api/v1/driver/documents/metadata`

### Driver Ride Management
- `GET /api/v1/driver/available-rides`
- `POST /api/v1/driver/accept-ride`
- `POST /api/v1/driver/decline-ride`
- `POST /api/v1/driver/start-ride`
- `POST /api/v1/driver/complete-ride`
- `GET /api/v1/driver/get-rides`
- `POST /api/v1/rides/{ride_id}/messages`
- `POST /api/v1/driver/report-breakdown`
- `GET /api/v1/driver/route-optimization`

### Platform Features
- Driver subscriptions: create, read, update, delete, payment, and history under `/api/v1/driver/subscription...`
- Parent subscriptions: create, read, update, cancel, usage, and child management under `/api/v1/parent/...`
- Payments: `/api/v1/payment/calculate-fare`, `/api/v1/payment/process`, `/api/v1/payment/history`, `/api/v1/subscribe-monthly`
- Analytics: `/api/v1/analytics/...` and `/api/v1/driver/analytics/...`
- Notifications: `/api/v1/notifications/register-device`, `/api/v1/notifications`, `/api/v1/notifications/{notification_id}/read`
- Admin: `/api/v1/admin/login`, `/api/v1/admin/users`, `/api/v1/admin/drivers`, `/api/v1/admin/drivers/{driver_id}/status`, `/api/v1/admin/rides`, `/api/v1/admin/reports/financial`

## Request Examples

### Create User Account
```json
{
  "phone_number": "+264813442530",
  "email": "user@example.com",
  "name": "Test User",
  "userType": "student"
}
```

### Create Driver Account
```json
{
  "phone_number": "+264813442530",
  "email": "driver@example.com",
  "name": "Test Driver",
  "license_number": "DL-12345",
  "vehicle_model": "Toyota Corolla",
  "vehicle_plate": "N12345W",
  "vehicle_color": "White"
}
```

### Request Ride
```json
{
  "pickup_location": {
    "latitude": -22.5609,
    "longitude": 17.0658,
    "name": "Windhoek Central"
  },
  "dropoff_location": {
    "latitude": -22.5709,
    "longitude": 17.0758,
    "name": "University of Namibia"
  },
  "ride_type": "standard",
  "estimated_fare": 13.0,
  "passengerCount": 1
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {},
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "error": {
    "code": "ERROR_CODE",
    "details": {}
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

---

## Admin Dashboard

### 1. Admin Login
**POST** `/api/v1/admin/login`
- **Description:** Authenticate admin dashboard access.
- **Body:**
  ```json
  { "id_token": "YOUR_FIREBASE_ID_TOKEN" }
  ```

### 2. Get Users / Drivers / Rides
**GET** `/api/v1/admin/users`
**GET** `/api/v1/admin/drivers`
**GET** `/api/v1/admin/rides`
- **Description:** Fetch platform entities for monitoring. Requires Admin Claims.

### 3. Update Vetting Status
**PUT** `/api/v1/admin/drivers/{driver_id}/status`
- **Description:** Approve entirely vetted drivers or suspend them.
- **Body:**
  ```json
  {
    "status": "approved",
    "reason": "Docs verified"
  }
  ```

### 4. Financial Reports
**GET** `/api/v1/admin/reports/financial`
- **Description:** Aggregated financial reporting matching SRS tracking for parent packages vs driver revenue.

---

## Driver Vetting and Compliance

### 1. Upload Document
**POST** `/api/v1/driver/documents`
- **Description:** Upload a multipart form-data document. Must provide `file` and `document_type` (license, permit).

### 2. Vetting Status
**GET** `/api/v1/driver/documents/status`
- **Description:** View pending, approved, or rejected document statuses.

### 3. Update Vehicle
**PUT** `/api/v1/driver/vehicle`
- **Description:** Manage/update vehicle details.
- **Body:**
  ```json
  {
    "vehicle_make": "Toyota",
    "vehicle_model": "Corolla",
    "vehicle_plate": "N12345W",
    "vehicle_color": "White"
  }
  ```

---

## Advanced Ride Scheduling & Carpooling

### 1. Schedule a Ride
**POST** `/api/v1/rides/schedule`
- **Description:** Book a future ride.
- **Body:** Contains `scheduled_time` and `is_recurring`.

### 2. Manage Scheduled Rides
**GET** `/api/v1/rides/scheduled`
**PUT** `/api/v1/rides/scheduled/{ride_id}`
**DELETE** `/api/v1/rides/scheduled/{ride_id}`

### 3. Carpooling
**GET** `/api/v1/rides/carpool-matches`
- **Query Params:** `lat`, `lng`, `dest_lat`, `dest_lng`, `time`
- **Description:** Find existing trips a user could piggyback on.

**POST** `/api/v1/rides/join-carpool`
- **Description:** Join an existing carpool.
- **Body:**
  ```json
  { "ride_id": "uuid", "passengerCount": 1 }
  ```

---

## Secure Parent/Child Handoff Updates

### 1. Update Child Profile
**PUT** `/api/v1/parent/children/{child_id}`
- **Description:** Update a child's profile details.

### 2. Remove Child Profile
**DELETE** `/api/v1/parent/children/{child_id}`
- **Description:** Remove a child graduating or leaving the package.

---

## Notifications & Communications

### 1. Register Device Token
**POST** `/api/v1/notifications/register-device`
- **Description:** Register a user's Firebase Cloud Messaging token.
- **Body:**
  ```json
  { "token": "string", "device_type": "android|ios" }
  ```

### 2. Notification History
**GET** `/api/v1/notifications`
- **Description:** Fetch the user's notification history inbox.

### 3. Mark Read
**PUT** `/api/v1/notifications/{notification_id}/read`
- **Description:** Acknowledge notification receipt.

## Support & Dispute Resolution

### Create Support Ticket
- **URL**: /api/v1/support/ticket
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  `json
  {
    "ride_id": "ride_id_123",
    "issue_type": "driver_behavior",
    "description": "The driver was very rude and drove recklessly.",
    "role": "rider"
  }
  `

### Get User Tickets
- **URL**: /api/v1/support/tickets
- **Method**: GET
- **Auth Required**: Yes

## Ratings & Reputation

### Get Driver Reviews
- **URL**: /api/v1/driver/{driver_id}/reviews
- **Method**: GET
- **Auth Required**: No

### Rate Rider
- **URL**: /api/v1/driver/rate-rider
- **Method**: POST
- **Auth Required**: Yes (Driver)
- **Body**:
  `json
  {
    "ride_id": "ride_id_123",
    "rating": 5,
    "review": "Great passenger"
  }
  `

## Growth & Retention

### Apply Promotion Code
- **URL**: /api/v1/promotions/apply
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  `json
  {
    "code": "STUDENT2025"
  }
  `

### Get Referral Code
- **URL**: /api/v1/referral/code
- **Method**: GET
- **Auth Required**: Yes
