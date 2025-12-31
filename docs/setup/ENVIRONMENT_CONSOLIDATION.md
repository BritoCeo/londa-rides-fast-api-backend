# Environment Configuration Consolidation

## Overview

This document describes the consolidation of environment variables from the previous microservices architecture into the unified API gateway.

## What Was Consolidated

### Previous Architecture (Microservices)

Environment variables were distributed across multiple services:

- **API Gateway** (`services/api-gateway/.env.*`): Gateway-specific variables
- **Auth Service** (`services/auth-service/.env.*`): JWT secrets, auth configuration
- **User Service** (`services/user-service/.env.*`): Firebase configuration
- **Driver Service** (`services/driver-service/.env.*`): Firebase configuration
- **Ride Service** (`services/ride-service/.env.*`): Firebase configuration

### New Architecture (Unified API Gateway)

All environment variables are now consolidated in a single location:

- **Unified API Gateway** (`services/api-gateway/.env.dev`, `.env.uat`, `.env.prd`): All variables in one place

## Environment Files Created

### 1. `.env.dev` (Development)
- **Location**: `services/api-gateway/.env.dev`
- **Purpose**: Local development environment
- **Key Features**:
  - Uses file path for `FIREBASE_SERVICE_ACCOUNT_KEY` (local development)
  - Debug logging enabled
  - Development-friendly defaults

### 2. `.env.uat` (User Acceptance Testing)
- **Location**: `services/api-gateway/.env.uat`
- **Purpose**: UAT/staging environment
- **Key Features**:
  - Uses full JSON content for `FIREBASE_SERVICE_ACCOUNT_KEY` (cloud deployment)
  - Info-level logging
  - UAT-specific URLs and secrets

### 3. `.env.prd` (Production)
- **Location**: `services/api-gateway/.env.prd`
- **Purpose**: Production environment
- **Key Features**:
  - Uses full JSON content for `FIREBASE_SERVICE_ACCOUNT_KEY` (cloud deployment)
  - Error-level logging (minimal logging)
  - Production-specific URLs and secrets
  - **WARNING**: Contains production secrets - never commit to version control!

### 4. `env.template` (Template)
- **Location**: `services/api-gateway/env.template`
- **Purpose**: Template for creating new environment files
- **Status**: ✅ Safe to commit to version control (no secrets)

## Variables Consolidated

### Core Configuration
- `NODE_ENV` - Environment identifier (dev/uat/prd)
- `PORT` - Service port (always 8000 for unified API)
- `LOG_LEVEL` - Logging level (debug/info/error)

### Firebase Configuration
- `FIREBASE_PROJECT_ID` - Firebase project ID
- `FIREBASE_SERVICE_ACCOUNT_KEY` - Service account key (file path for dev, JSON content for cloud)

### JWT Authentication
- `JWT_SECRET` - JWT signing secret
- `JWT_REFRESH_SECRET` - Refresh token secret
- `ACCESS_TOKEN_SECRET` - Access token secret
- `JWT_EXPIRES_IN` - Token expiration time

### Email Configuration
- `SMTP_HOST` - SMTP server host
- `SMTP_PORT` - SMTP server port
- `SMTP_USER` - SMTP username
- `SMTP_PASS` - SMTP password
- `SMTP_FROM` - From email address
- `EMAIL_ACTIVATION_SECRET` - Email verification secret
- `CLIENT_URL` - Frontend URL for email links

### Optional Services
- `TWILIO_ACCOUNT_SID` - Twilio Account SID (SMS)
- `TWILIO_AUTH_TOKEN` - Twilio Auth Token (SMS)
- `TWILIO_PHONE_NUMBER` - Twilio phone number (SMS)
- `GOOGLE_MAPS_API_KEY` - Google Maps API key
- `NYLAS_API_KEY` - Nylas API key (calendar integration)
- `USER_GRANT_ID` - Nylas user grant ID
- `SOCKET_WS_URL` - WebSocket server URL
- `SOCKET_SERVER_URL` - Socket HTTP server URL
- `SOCKET_API_SECRET` - Socket API authentication secret

## Variables Removed (No Longer Needed)

These variables were specific to the microservices architecture and are no longer needed:

- ❌ `USER_SERVICE_URL` - User service URL (consolidated)
- ❌ `DRIVER_SERVICE_URL` - Driver service URL (consolidated)
- ❌ `AUTH_SERVICE_URL` - Auth service URL (consolidated)
- ❌ `RIDE_SERVICE_URL` - Ride service URL (consolidated)
- ❌ `USE_MICROSERVICES` - Microservices flag (no longer applicable)
- ❌ `MAIN_SERVER_URL` - Legacy main server URL (deprecated)

## Environment File Loading

The unified API gateway automatically loads the appropriate environment file based on `NODE_ENV`:

```typescript
// services/api-gateway/src/server.ts
const env = process.env.NODE_ENV || 'dev';
const envFile = `.env.${env}`;
const envPath = path.resolve(__dirname, '..', envFile);

// Load environment-specific file
require('dotenv').config({ path: envPath });
require('dotenv').config(); // Fallback to .env
```

### Loading Order

1. Load `.env.{NODE_ENV}` (e.g., `.env.dev`, `.env.uat`, `.env.prd`)
2. Fallback to `.env` if environment-specific file doesn't exist
3. System environment variables override file values

## Migration Steps

If you're migrating from the old microservices architecture:

1. **Copy values from old .env files:**
   - From `services/auth-service/.env.*` → JWT variables
   - From `services/user-service/.env.*` → Firebase variables
   - From `services/driver-service/.env.*` → Firebase variables (same as user-service)
   - From `services/ride-service/.env.*` → Firebase variables (same as user-service)

2. **Consolidate into unified .env files:**
   - Copy all variables to `services/api-gateway/.env.dev`
   - Copy all variables to `services/api-gateway/.env.uat`
   - Copy all variables to `services/api-gateway/.env.prd`

3. **Update Firebase Service Account Key:**
   - **For dev**: Keep file path (e.g., `../../server/service-account-key.json`)
   - **For uat/prd**: Use full JSON content (not file path)

4. **Generate new secrets:**
   - Use `openssl rand -base64 32` to generate strong secrets
   - Use different secrets for each environment

5. **Remove old .env files** (optional, after migration is complete)

## Security Best Practices

1. **Never commit .env files to version control**
   - `.env.dev`, `.env.uat`, `.env.prd` should be in `.gitignore`
   - Only commit `env.template` (no secrets)

2. **Use strong secrets in production**
   - Minimum 32 characters for JWT secrets
   - Recommended 64+ characters for production
   - Use different secrets for each environment

3. **For cloud deployment:**
   - Use environment variables in your hosting platform (Render, Heroku, etc.)
   - Never hardcode secrets in code
   - Use secrets management services for production

4. **Firebase Service Account:**
   - In local dev: File paths are acceptable
   - In cloud: Always use full JSON content (not file paths)
   - Restrict service account permissions to minimum required

## Verification

To verify your environment configuration:

1. **Check file exists:**
   ```bash
   ls services/api-gateway/.env.dev
   ```

2. **Test environment loading:**
   ```bash
   cd services/api-gateway
   NODE_ENV=dev npm run dev
   ```

3. **Check logs for environment variables:**
   - Look for "Starting Unified API Gateway" message
   - Verify PORT is 8000
   - Check for any missing variable warnings

## Troubleshooting

### Issue: "Environment variable not found"

**Solution:**
1. Check that `.env.{NODE_ENV}` file exists
2. Verify variable name matches exactly (case-sensitive)
3. Ensure no extra spaces around `=` sign
4. Check that `NODE_ENV` is set correctly

### Issue: "FIREBASE_SERVICE_ACCOUNT_KEY contains a file path"

**Error:** Cloud environments don't support file paths.

**Solution:**
- For local dev: Use file path (e.g., `../../server/service-account-key.json`)
- For cloud: Use full JSON content (paste entire JSON object)

### Issue: "JWT_SECRET not set"

**Solution:**
1. Generate a secret: `openssl rand -base64 32`
2. Add to `.env.{NODE_ENV}` file
3. Ensure it's at least 32 characters

## Related Documentation

- [Environment Setup Guide](./ENVIRONMENT_SETUP.md) - Detailed setup instructions
- [Migration Guide](../../docs/MIGRATION_TO_UNIFIED_API.md) - Migration from microservices
- [Render Environment Variables](../../docs/deployment/RENDER_ENVIRONMENT_VARIABLES.md) - Cloud deployment variables

---

**Last Updated:** January 2025  
**Status:** ✅ Complete

