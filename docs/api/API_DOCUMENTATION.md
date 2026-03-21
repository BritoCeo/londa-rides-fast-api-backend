# Londa Rides API Documentation

## Base URL
```
https://londa-rides-fast-api-backend.onrender.com/api/v1
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### User Service

#### Create User
```
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phoneNumber": "+1234567890",
  "userType": "STUDENT"
}
```

#### Get User by ID
```
GET /users/:id
```

#### Update User
```
PUT /users/:id
Content-Type: application/json

{
  "name": "John Updated",
  "email": "john.updated@example.com"
}
```

### Driver Service

#### Create Driver
```
POST /drivers
Content-Type: application/json

{
  "name": "Driver Name",
  "phoneNumber": "+1234567890",
  "email": "driver@example.com",
  "vehicleType": "Car",
  "registrationNumber": "ABC123"
}
```

### Auth Service

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "phoneNumber": "+1234567890",
  "password": "password123",
  "type": "user"
}
```

#### Refresh Token
```
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "<refresh_token>"
}
```

### Ride Service

#### Request Ride
```
POST /request-ride
Content-Type: application/json

{
  "pickup_location": {
    "latitude": -22.5700,
    "longitude": 17.0836,
    "name": "Pickup Address"
  },
  "dropoff_location": {
    "latitude": -22.5800,
    "longitude": 17.0900,
    "name": "Dropoff Address"
  },
  "ride_type": "school",
  "estimated_fare": 13.00,
  "passengerCount": 1
}
```

#### Get Active Rides
Retrieves active rides for the authenticated parent. Can optionally filter by ride type.
```
GET /parent/active-rides?ride_type=school
```

#### Send Ride Message
Allows drivers to send messages during an active ride.
```
POST /rides/:ride_id/messages
Content-Type: application/json

{
  "content": "I have arrived at the school.",
  "message_type": "text"
}
```

#### Get Ride Messages
Retrieves the message history for a specific ride.
```
GET /rides/:ride_id/messages?limit=50
```

#### Report Breakdown (Driver)
Allows a driver to report a vehicle breakdown, resetting the ride back to pending and notifying nearby drivers.
```
POST /driver/report-breakdown
Content-Type: application/json

{
  "ride_id": "ride-uuid-here"
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "code": "ERROR_CODE",
  "details": { ... },
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
    "make": "Toyota", 
    "model": "Corolla", 
    "license_plate": "N12345W", 
    "color": "White"
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
