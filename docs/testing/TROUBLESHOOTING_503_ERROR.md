# 🔧 Troubleshooting 503 Service Unavailable Error

## Problem

All API requests return `503 Service Unavailable` when running Postman/Newman tests:

```
POST http://localhost:8000/api/v1/registration [503 Service Unavailable]
POST http://localhost:8000/api/v1/verify-otp [503 Service Unavailable]
```

## Root Cause

The **API Gateway** (port 8000) is running, but the **Main Server** (port 3001) is **not running**.

The API Gateway proxies all `/api/v1/*` requests to the main server at `http://localhost:3001`. When the main server is down, the gateway returns a 503 error.

## Solution

### Quick Fix: Start the Main Server

**Option 1: Start All Services (Recommended)**
```bash
# From backend/ directory
npm run dev:all
```

This starts:
- ✅ Main Server (port 3001) - **REQUIRED**
- ✅ API Gateway (port 8000) - **REQUIRED**
- ✅ User Service (port 8002)
- ✅ Driver Service (port 8003)
- ✅ Auth Service (port 8001)
- ✅ Ride Service (port 8004)

**Option 2: Start Only Required Services**
```bash
# Terminal 1: Main Server
cd server
npm run dev:3001

# Terminal 2: API Gateway (if not already running)
cd services/api-gateway
npm run dev
```

### Verify Services Are Running

**Check Main Server:**
```bash
curl http://localhost:3001/test
```

Expected response:
```json
{
  "success": true,
  "message": "Server is working"
}
```

**Check API Gateway:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "..."
}
```

**Check Ports (Windows):**
```powershell
netstat -ano | findstr :3001
netstat -ano | findstr :8000
```

**Check Ports (Linux/Mac):**
```bash
lsof -i :3001
lsof -i :8000
```

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Client    │────────▶│ API Gateway  │────────▶│ Main Server │
│ (Postman/   │         │  Port 8000  │         │  Port 3001  │
│  Newman)    │         │             │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              │ Proxies /api/v1/* requests
                              │
                              ▼
                        503 if main server
                        is not running
```

## Test Script Enhancement

The test script (`test-postman-auth.js`) now automatically checks if the main server is running before executing tests:

```bash
npm run test:postman:auth
```

If the server is not running, you'll see:
```
❌ ERROR: Main server is not running on port 3001!

📋 To fix this, start the main server:
   Option 1: From root directory
      npm run dev:all
   Option 2: From server directory
      cd server
      npm run dev:3001
```

## Skip Server Check (Not Recommended)

If you want to skip the server check (e.g., for CI/CD where you manage servers separately):

```bash
node test-postman-auth.js --skip-server-check
```

## Common Scenarios

### Scenario 1: Only API Gateway Running
- ✅ API Gateway responds to `/health` and `/test`
- ❌ All `/api/v1/*` requests return 503
- **Fix:** Start main server with `npm run dev:all` or `cd server && npm run dev:3001`

### Scenario 2: Both Services Running
- ✅ API Gateway responds to `/health` and `/test`
- ✅ Main server responds to `/test` on port 3001
- ✅ All `/api/v1/*` requests work correctly

### Scenario 3: Port Already in Use
- Error: `EADDRINUSE` or port already in use
- **Fix:** 
  ```powershell
  # Find process using port
  netstat -ano | findstr :3001
  
  # Kill process (replace PID)
  taskkill /PID <PID> /F
  ```

## Prevention

1. **Always use `npm run dev:all`** to start all required services
2. **Check service status** before running tests
3. **Use the test script's built-in check** - it will warn you if servers aren't running

## Related Documentation

- [Newman Postman Testing Guide](./NEWMAN_POSTMAN_TESTING.md)
- [Quick Start Guide](../setup/QUICK_START.md)
- [Testing README](./README.md)

