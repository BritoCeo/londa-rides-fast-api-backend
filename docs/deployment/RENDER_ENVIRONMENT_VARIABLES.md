# Render Environment Variables Reference

> **⚠️ IMPORTANT:** This document has been updated for the **Unified API Gateway** architecture. The previous microservices architecture (auth-service, user-service, driver-service, ride-service) has been consolidated into a single unified API gateway service.

This document lists all environment variables required for the unified API gateway in Render deployment.

## Quick Reference Table

| Service | Required Variables | Optional Variables |
|---------|-------------------|-------------------|
| **Unified API Gateway** | `NODE_ENV`, `PORT`, `FIREBASE_SERVICE_ACCOUNT_KEY`, `FIREBASE_PROJECT_ID`, `JWT_SECRET`, `JWT_REFRESH_SECRET`, `ACCESS_TOKEN_SECRET` | `LOG_LEVEL`, `SMTP_*`, `GOOGLE_MAPS_API_KEY`, `NYLAS_API_KEY`, `TWILIO_*`, `SOCKET_*` |

> **Note:** All functionality from the previous microservices has been consolidated into the unified API gateway. Only one service needs to be deployed.

---

## Unified API Gateway

**Service Name:** `api-gateway`  
**Port:** `8000`  
**Type:** Unified Monolithic API (all functionality consolidated)

### Required Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `NODE_ENV` | `uat` | Environment identifier: `dev`, `uat`, or `prd` |
| `PORT` | `8000` | Service port (must be 8000) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | `{...JSON content...}` | **REQUIRED** - Full JSON content (see below) |
| `FIREBASE_PROJECT_ID` | `londa-cd054` | **REQUIRED** - Your Firebase project ID |
| `JWT_SECRET` | `your-secret-key-here` | **REQUIRED** - Strong secret key for JWT signing (min 32 chars) |
| `JWT_REFRESH_SECRET` | `your-refresh-secret-key` | **REQUIRED** - Secret for refresh tokens |
| `ACCESS_TOKEN_SECRET` | `your-access-token-secret` | **REQUIRED** - Secret for access tokens |

### Optional Environment Variables

| Variable | Value | Default | Notes |
|----------|-------|---------|-------|
| `LOG_LEVEL` | `info` | `info` | Logging level: `debug`, `info`, `error` |
| `JWT_EXPIRES_IN` | `24h` | `24h` | JWT token expiration time |
| `SMTP_HOST` | `smtp.gmail.com` | `smtp.gmail.com` | SMTP server host |
| `SMTP_PORT` | `587` | `587` | SMTP server port |
| `SMTP_USER` | `your-email@gmail.com` | - | SMTP username |
| `SMTP_PASS` | `your-app-password` | - | SMTP password |
| `SMTP_FROM` | `noreply@londarides.com` | `noreply@londarides.com` | From email address |
| `EMAIL_ACTIVATION_SECRET` | `your-secret` | - | Secret for email verification |
| `CLIENT_URL` | `https://yourdomain.com` | - | Frontend URL for email links |
| `GOOGLE_MAPS_API_KEY` | `your-api-key` | - | Google Maps API key |
| `NYLAS_API_KEY` | `your-nylas-key` | - | Nylas API key (optional) |
| `USER_GRANT_ID` | `your-grant-id` | - | Nylas user grant ID (optional) |
| `TWILIO_ACCOUNT_SID` | `your-sid` | - | Twilio Account SID (optional) |
| `TWILIO_AUTH_TOKEN` | `your-token` | - | Twilio Auth Token (optional) |
| `TWILIO_PHONE_NUMBER` | `+1234567890` | - | Twilio phone number (optional) |
| `SOCKET_WS_URL` | `wss://socket.yourdomain.com` | - | WebSocket server URL (optional) |
| `SOCKET_SERVER_URL` | `https://socket.yourdomain.com` | - | Socket HTTP server URL (optional) |
| `SOCKET_API_SECRET` | `your-socket-secret` | `londa-socket-secret-2024` | Socket API secret (optional) |

### FIREBASE_SERVICE_ACCOUNT_KEY Setup

**IMPORTANT**: This must be the **entire JSON content** of your service account key file, NOT a file path.

#### Steps to Set FIREBASE_SERVICE_ACCOUNT_KEY:

1. **Open your Firebase service account key file** (`service-account-key.json`)
2. **Copy the entire JSON content** (everything from `{` to `}`)
3. **In Render Dashboard:**
   - Go to `api-gateway` → Environment tab
   - Find or create `FIREBASE_SERVICE_ACCOUNT_KEY`
   - Paste the entire JSON content as the value
   - Make sure it's a single-line JSON string (or properly escaped)

#### Example Format:

The value should look like this (all on one line or properly formatted):
```json
{"type":"service_account","project_id":"londa-cd054","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
```

#### Common Mistakes to Avoid:

- ❌ **DON'T** set it to: `../../server/service-account-key.json` (file path)
- ❌ **DON'T** set it to: `./service-account-key.json` (file path)
- ✅ **DO** set it to: The entire JSON object content

### JWT_SECRET Setup

1. Generate a strong secret key (minimum 32 characters recommended)
2. Example: `openssl rand -base64 32` or use a password generator
3. Set this value in Render dashboard for `api-gateway`
4. **Important**: Use a different secret for production!

---

## ⚠️ DEPRECATED: Individual Microservices

> **Note:** The following services (auth-service, user-service, driver-service, ride-service) have been **deprecated** and consolidated into the unified API gateway. This section is kept for reference only.

### Auth Service (DEPRECATED)

**Service Name:** `auth-service`  
**Port:** `8001`  
**Status:** ⚠️ **DEPRECATED** - Use unified API gateway instead

### Required Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `NODE_ENV` | `uat` | Environment identifier |
| `PORT` | `8001` | Service port (must be 8001) |
| `JWT_SECRET` | `your-secret-key-here` | **REQUIRED** - Strong secret key for JWT signing |

### Optional Environment Variables

| Variable | Value | Default | Notes |
|----------|-------|---------|-------|
| `JWT_EXPIRES_IN` | `24h` | `24h` | JWT token expiration time |
| `LOG_LEVEL` | `info` | `info` | Logging level: `debug`, `info`, `error` |

### JWT_SECRET Setup

1. Generate a strong secret key (minimum 32 characters recommended)
2. Example: `openssl rand -base64 32` or use a password generator
3. Set this value in Render dashboard for `auth-service`
4. **Important**: Use a different secret for production!

---

### User Service (DEPRECATED)

**Service Name:** `user-service`  
**Port:** `8002`  
**Status:** ⚠️ **DEPRECATED** - Use unified API gateway instead

### Required Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `NODE_ENV` | `uat` | Environment identifier |
| `PORT` | `8002` | Service port (must be 8002) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | `{...JSON content...}` | **REQUIRED** - Full JSON content (see below) |
| `FIREBASE_PROJECT_ID` | `londa-cd054` | **REQUIRED** - Your Firebase project ID |

### Optional Environment Variables

| Variable | Value | Default | Notes |
|----------|-------|---------|-------|
| `LOG_LEVEL` | `info` | `info` | Logging level: `debug`, `info`, `error` |

### FIREBASE_SERVICE_ACCOUNT_KEY Setup

**IMPORTANT**: This must be the **entire JSON content** of your service account key file, NOT a file path.

#### Steps to Set FIREBASE_SERVICE_ACCOUNT_KEY:

1. **Open your Firebase service account key file** (`service-account-key.json`)
2. **Copy the entire JSON content** (everything from `{` to `}`)
3. **In Render Dashboard:**
   - Go to `user-service` → Environment tab
   - Find or create `FIREBASE_SERVICE_ACCOUNT_KEY`
   - Paste the entire JSON content as the value
   - Make sure it's a single-line JSON string (or properly escaped)

#### Example Format:

The value should look like this (all on one line or properly formatted):
```json
{"type":"service_account","project_id":"londa-cd054","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
```

#### Common Mistakes to Avoid:

- ❌ **DON'T** set it to: `../../server/service-account-key.json` (file path)
- ❌ **DON'T** set it to: `./service-account-key.json` (file path)
- ✅ **DO** set it to: The entire JSON object content

---

### Driver Service (DEPRECATED)

**Service Name:** `driver-service`  
**Port:** `8003`  
**Status:** ⚠️ **DEPRECATED** - Use unified API gateway instead

### Required Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `NODE_ENV` | `uat` | Environment identifier |
| `PORT` | `8003` | Service port (must be 8003) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | `{...JSON content...}` | **REQUIRED** - Full JSON content (same as User Service) |
| `FIREBASE_PROJECT_ID` | `londa-cd054` | **REQUIRED** - Your Firebase project ID |

### Optional Environment Variables

| Variable | Value | Default | Notes |
|----------|-------|---------|-------|
| `LOG_LEVEL` | `info` | `info` | Logging level: `debug`, `info`, `error` |

### FIREBASE_SERVICE_ACCOUNT_KEY Setup

Same as User Service - use the entire JSON content of your Firebase service account key file.

---

### Ride Service (DEPRECATED)

**Service Name:** `ride-service`  
**Port:** `8004`  
**Status:** ⚠️ **DEPRECATED** - Use unified API gateway instead

### Required Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `NODE_ENV` | `uat` | Environment identifier |
| `PORT` | `8004` | Service port (must be 8004) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | `{...JSON content...}` | **REQUIRED** - Full JSON content (same as User Service) |
| `FIREBASE_PROJECT_ID` | `londa-cd054` | **REQUIRED** - Your Firebase project ID |

### Optional Environment Variables

| Variable | Value | Default | Notes |
|----------|-------|---------|-------|
| `LOG_LEVEL` | `info` | `info` | Logging level: `debug`, `info`, `error` |

### FIREBASE_SERVICE_ACCOUNT_KEY Setup

Same as User Service - use the entire JSON content of your Firebase service account key file.

---

## How to Set Environment Variables in Render

### Method 1: Using Blueprint (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Navigate to your Blueprint
3. Before clicking "Apply", you can set environment variables for each service
4. Click on each service to expand and set variables
5. Click "Apply" to deploy

### Method 2: After Deployment

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on the service (e.g., `user-service`)
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Enter variable name and value
6. Click **Save Changes**
7. Service will automatically redeploy

---

## Environment Variables Checklist

Use this checklist to ensure all variables are set for the **Unified API Gateway**:

### Unified API Gateway (Required)
- [ ] `NODE_ENV` = `uat`
- [ ] `PORT` = `8000`
- [ ] `FIREBASE_SERVICE_ACCOUNT_KEY` = `[full JSON content]` ⚠️ **REQUIRED**
- [ ] `FIREBASE_PROJECT_ID` = `londa-cd054` ⚠️ **REQUIRED**
- [ ] `JWT_SECRET` = `[your-secret-key]` ⚠️ **REQUIRED** (min 32 chars)
- [ ] `JWT_REFRESH_SECRET` = `[your-refresh-secret]` ⚠️ **REQUIRED**
- [ ] `ACCESS_TOKEN_SECRET` = `[your-access-token-secret]` ⚠️ **REQUIRED**

### Unified API Gateway (Optional)
- [ ] `LOG_LEVEL` = `info` (optional)
- [ ] `JWT_EXPIRES_IN` = `24h` (optional)
- [ ] `SMTP_HOST` = `smtp.gmail.com` (optional)
- [ ] `SMTP_PORT` = `587` (optional)
- [ ] `SMTP_USER` = `your-email@gmail.com` (optional)
- [ ] `SMTP_PASS` = `your-app-password` (optional)
- [ ] `SMTP_FROM` = `noreply@londarides.com` (optional)
- [ ] `EMAIL_ACTIVATION_SECRET` = `your-secret` (optional)
- [ ] `CLIENT_URL` = `https://yourdomain.com` (optional)
- [ ] `GOOGLE_MAPS_API_KEY` = `your-api-key` (optional)
- [ ] `NYLAS_API_KEY` = `your-nylas-key` (optional)
- [ ] `TWILIO_ACCOUNT_SID` = `your-sid` (optional)
- [ ] `TWILIO_AUTH_TOKEN` = `your-token` (optional)
- [ ] `TWILIO_PHONE_NUMBER` = `+1234567890` (optional)
- [ ] `SOCKET_WS_URL` = `wss://socket.yourdomain.com` (optional)
- [ ] `SOCKET_SERVER_URL` = `https://socket.yourdomain.com` (optional)
- [ ] `SOCKET_API_SECRET` = `your-socket-secret` (optional)

---

## Common Issues and Solutions

### Issue: "FIREBASE_SERVICE_ACCOUNT_KEY contains a file path"

**Error Message:**
```
❌ FIREBASE_SERVICE_ACCOUNT_KEY contains a file path, but file paths are not supported in cloud environments
```

**Solution:**
- The variable is set to a file path (e.g., `../../server/service-account-key.json`)
- You need to set it to the **entire JSON content** of the file
- Open your `service-account-key.json` file and copy all content
- Paste it as the value in Render

### Issue: "Port X is already in use"

**Error Message:**
```
Port 8000 is already in use
```

**Solution:**
- Check that each service has the correct `PORT` value set
- Ensure services are deployed separately (not via `npm run uat:all`)
- Verify `render.yaml` startCommand is being used

### Issue: "JWT_SECRET not set"

**Solution:**
- Generate a strong secret: `openssl rand -base64 32`
- Set it in `auth-service` environment variables
- Ensure it's at least 32 characters long

---

## Security Best Practices

1. **Never commit** environment variables to Git
2. **Use Render Secrets** for sensitive values (JWT_SECRET, Firebase keys)
3. **Rotate secrets** regularly, especially in production
4. **Use different secrets** for UAT and Production environments
5. **Limit access** to Render dashboard to authorized personnel only

---

## Testing Your Configuration

After setting all environment variables:

1. **Check service logs** in Render dashboard
2. **Test health endpoints:**
   - API Gateway: `https://api-gateway-xxxx.onrender.com/health`
   - Auth Service: `https://auth-service-xxxx.onrender.com/health`
   - User Service: `https://user-service-xxxx.onrender.com/health`
   - Driver Service: `https://driver-service-xxxx.onrender.com/health`
   - Ride Service: `https://ride-service-xxxx.onrender.com/health`

3. **Verify no errors** in logs related to:
   - Firebase initialization
   - Port conflicts
   - Missing environment variables

---

## Summary

**Critical Variables to Set for Unified API Gateway:**

1. **Core Configuration**: `NODE_ENV`, `PORT` (must be 8000)
2. **Firebase**: `FIREBASE_SERVICE_ACCOUNT_KEY` (full JSON content, not file path), `FIREBASE_PROJECT_ID`
3. **JWT Authentication**: `JWT_SECRET`, `JWT_REFRESH_SECRET`, `ACCESS_TOKEN_SECRET` (generate strong secrets with `openssl rand -base64 32`)
4. **Optional**: SMTP, Google Maps, Nylas, Twilio, Socket.io configuration

**No Longer Needed:**
- ❌ `USER_SERVICE_URL`, `DRIVER_SERVICE_URL`, `AUTH_SERVICE_URL`, `RIDE_SERVICE_URL` (microservice URLs)
- ❌ `USE_MICROSERVICES` flag
- ❌ Individual service environment variables (consolidated into unified gateway)

For detailed deployment instructions, see [RENDER_DEPLOYMENT_GUIDE.md](./RENDER_DEPLOYMENT_GUIDE.md).

For environment setup details, see [services/api-gateway/ENVIRONMENT_SETUP.md](../../services/api-gateway/ENVIRONMENT_SETUP.md).

