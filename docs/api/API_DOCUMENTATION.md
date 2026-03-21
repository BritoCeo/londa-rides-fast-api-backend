# Londa Rides API Documentation

## Base URL
```
http://localhost:8000/api/v1
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

