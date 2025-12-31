# Testing User Authentication APIs

## Problem
The API Gateway is trying to proxy requests to the main server at `http://localhost:3001`, but the main server is not running. This causes "Service unavailable" errors.

## Solution

### Option 1: Start Main Server Separately (Recommended for Testing)

Open a **new terminal window** and run:

```bash
cd server
npm run dev:3001
```

This will start the main server on port 3001. You should see:
```
Server is connected with port 3001 on all interfaces
```

### Option 2: Use Updated dev:all Command

The `package.json` has been updated to include the main server. Use:

```bash
npm run dev:all
```

This will start:
- **MAIN** server on port 3001 (cyan)
- **USER** service on port 8002 (blue)
- **DRIVER** service on port 8003 (green)
- **AUTH** service on port 8001 (yellow)
- **RIDE** service on port 8004 (red)
- **GATEWAY** on port 8000 (magenta)

## Testing User Authentication APIs

Once the main server is running, test the following endpoints using Postman or curl:

### 1. Health Check
```bash
GET http://localhost:8000/health
```

### 2. API Test
```bash
GET http://localhost:8000/test
```

### 3. Register User (Send OTP)
```bash
POST http://localhost:8000/api/v1/registration
Content-Type: application/json

{
  "phone_number": "+264813442530"
}
```

**Expected Response (JSON):**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "sessionInfo": "..."
}
```

### 4. Verify OTP (Login)
```bash
POST http://localhost:8000/api/v1/verify-otp
Content-Type: application/json

{
  "phone_number": "+264813442530",
  "otp": "123456",
  "sessionInfo": "your_session_info_from_registration"
}
```

**Expected Response (JSON):**
```json
{
  "success": true,
  "accessToken": "...",
  "user": { ... }
}
```

### 5. Request Email OTP
```bash
POST http://localhost:8000/api/v1/email-otp-request
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### 6. Verify Email OTP
```bash
PUT http://localhost:8000/api/v1/email-otp-verify
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456"
}
```

### 7. Create User Account
```bash
POST http://localhost:8000/api/v1/create-account
Content-Type: application/json

{
  "phone_number": "+264813442530",
  "email": "user@example.com",
  "name": "John Doe",
  "userType": "student"
}
```

### 8. Get Logged In User Data
```bash
GET http://localhost:8000/api/v1/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Verification Checklist

✅ All responses should be **JSON format** (not HTML)  
✅ Error responses (404, 500, etc.) should also be JSON  
✅ Content-Type header should be `application/json`  
✅ Response format: `{ success, message, data?, error?, timestamp }`

## Troubleshooting

### Error: "Service unavailable" / "Cannot connect to main-server"
- **Solution**: Start the main server on port 3001 (see Option 1 above)

### Error: "Port 3001 is already in use"
- **Solution**: Kill the process using port 3001:
  ```bash
  # Windows
  netstat -ano | findstr :3001
  taskkill /PID <PID> /F
  
  # Linux/Mac
  lsof -ti:3001 | xargs kill
  ```

### Error: "Port 8000 is already in use"
- **Solution**: The API Gateway is already running. You can use it, or kill it and restart:
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

## Quick Test Commands (Windows PowerShell)

```powershell
# Test Health Check
curl http://localhost:8000/health

# Test API Gateway
curl http://localhost:8000/test

# Test Registration (should return JSON error if server not running, or JSON success if running)
curl -X POST http://localhost:8000/api/v1/registration -H "Content-Type: application/json" -d '{\"phone_number\":\"+264813442530\"}'
```

## Postman Collection

Use the `Londa_Rides_Local_Testing.postman_collection.json` file which includes:
- All user authentication endpoints
- Pre-configured request bodies
- Automatic token extraction scripts
- Test scripts to verify JSON responses

