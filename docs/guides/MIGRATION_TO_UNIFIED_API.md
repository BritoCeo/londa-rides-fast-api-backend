# Migration Guide: Microservices to Unified API

## Overview

This guide helps you migrate from the previous microservices architecture to the new unified monolithic API architecture.

## What Changed?

### Architecture Transformation

**Before:** Microservices with API Gateway
- API Gateway (port 8000) → proxies to microservices
- Auth Service (port 8001)
- User Service (port 8002)
- Driver Service (port 8003)
- Ride Service (port 8004)
- Legacy Server (port 3001) - fallback mode

**After:** Unified Monolithic API
- Unified API Gateway (port 8000) → handles all requests directly
- All functionality consolidated into single service

## Migration Steps

### Step 1: Update Your Development Environment

1. **Install dependencies:**
   ```bash
   cd services/api-gateway
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cd services/api-gateway
   cp env.template .env.dev
   # Edit .env.dev with your values
   ```

3. **Build shared package:**
   ```bash
   cd shared
   npm install
   npm run build
   ```

### Step 2: Update Your Scripts

**Old scripts (deprecated):**
```bash
npm run dev:all        # Runs all microservices
npm run dev:main       # Runs legacy server
```

**New scripts (recommended):**
```bash
npm run dev:unified    # Runs unified API gateway
```

### Step 3: Update Environment Variables

**Consolidate variables from:**
- `server/.env.*`
- `services/auth-service/.env.*`
- `services/user-service/.env.*`
- `services/driver-service/.env.*`
- `services/ride-service/.env.*`

**Into:**
- `services/api-gateway/.env.dev`
- `services/api-gateway/.env.uat`
- `services/api-gateway/.env.prd`

See `services/api-gateway/ENVIRONMENT_SETUP.md` for the complete list of required variables.

### Step 4: Update API Endpoints

**No changes required!** All API endpoints remain the same:

- `http://localhost:8000/api/v1/auth/*`
- `http://localhost:8000/api/v1/users/*`
- `http://localhost:8000/api/v1/driver/*`
- `http://localhost:8000/api/v1/rides/*`
- etc.

The unified API gateway maintains the same route structure.

### Step 5: Update Deployment Configuration

If you're using Render or another deployment platform:

1. **Update `render.yaml`** to deploy only the unified API gateway
2. **Remove** microservice service definitions
3. **Update** environment variables to use unified configuration

## Environment Variables Migration

### Variables to Remove

These are no longer needed (microservice-specific):
- `USER_SERVICE_URL`
- `DRIVER_SERVICE_URL`
- `AUTH_SERVICE_URL`
- `RIDE_SERVICE_URL`
- `USE_MICROSERVICES`
- `MAIN_SERVER_URL`

### Variables to Keep

All other variables are consolidated in the unified API gateway:
- `NODE_ENV`
- `PORT` (must be 8000)
- `FIREBASE_SERVICE_ACCOUNT_KEY`
- `FIREBASE_PROJECT_ID`
- `JWT_SECRET`
- `JWT_REFRESH_SECRET`
- `ACCESS_TOKEN_SECRET`
- `SMTP_*` variables
- `GOOGLE_MAPS_API_KEY`
- `NYLAS_API_KEY`
- `TWILIO_*` variables
- `SOCKET_*` variables
- And more...

See `services/api-gateway/ENVIRONMENT_SETUP.md` for the complete list.

## Testing Your Migration

1. **Start the unified API:**
   ```bash
   cd services/api-gateway
   npm run dev
   ```

2. **Test health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test API endpoints:**
   ```bash
   # Test authentication
   curl -X POST http://localhost:8000/api/v1/register \
     -H "Content-Type: application/json" \
     -d '{"phone_number": "+264811234567"}'
   
   # Test user endpoints
   curl http://localhost:8000/api/v1/users
   ```

4. **Check logs** for any errors

## Common Issues

### Issue: "Cannot find module"

**Solution:** Make sure you've built the shared package:
```bash
cd shared
npm run build
```

### Issue: "Port 8000 already in use"

**Solution:** Stop any old services running on port 8000:
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### Issue: "Environment variables not found"

**Solution:** 
1. Copy `env.template` to `.env.dev`
2. Fill in all required values
3. Ensure `NODE_ENV=dev` is set

### Issue: "Firebase initialization failed"

**Solution:**
1. Check `FIREBASE_SERVICE_ACCOUNT_KEY` is set correctly
2. For local: Use file path (e.g., `../../server/service-account-key.json`)
3. For cloud: Use full JSON content

## Rollback Plan

If you need to rollback to the old architecture:

1. **Stop unified API:**
   ```bash
   # Kill the process
   ```

2. **Start old services:**
   ```bash
   npm run dev:all
   ```

3. **Note:** The old architecture is deprecated and will be removed in a future release.

## Benefits of Unified API

1. **Simplified Deployment:** Single service to deploy
2. **Reduced Complexity:** No inter-service communication
3. **Easier Debugging:** All code in one place
4. **Lower Latency:** Direct processing without network hops
5. **Unified Configuration:** Single environment file

## Timeline

- ✅ **Phase 1:** Consolidation complete
- ✅ **Phase 2:** Documentation updated
- ⏳ **Phase 3:** Migration period (current)
- 🔮 **Phase 4:** Remove deprecated code (future)

## Support

- **Documentation:** See `docs/architecture/DETAILED_ARCHITECTURE.md`
- **Environment Setup:** See `services/api-gateway/ENVIRONMENT_SETUP.md`
- **Setup Guide:** See `docs/setup/SETUP_AND_RUN_GUIDE.md`

---

**Last Updated:** January 2025

