# Unified API Gateway - Environment Configuration Guide

## Overview

The unified API gateway consolidates all environment variables from the previous microservices architecture into a single configuration. This guide explains how to set up environment variables for the unified API gateway.

> **📚 For detailed step-by-step setup instructions for each environment variable, see the [Complete Environment Variables Setup Guide](./COMPLETE_ENV_SETUP_GUIDE.md).**

## Quick Start

1. **Copy the template:**
   ```bash
   cd services/api-gateway
   cp .env.example .env.dev
   ```

2. **Fill in the values** for your development environment

3. **For other environments:**
   ```bash
   cp .env.example .env.uat
   cp .env.example .env.prd
   ```

## Environment Files

The unified API gateway supports environment-specific configuration files:

- `.env.dev` - Development environment
- `.env.uat` - User Acceptance Testing environment  
- `.env.prd` - Production environment

The system automatically loads the appropriate file based on `NODE_ENV`:
- `NODE_ENV=dev` → loads `.env.dev`
- `NODE_ENV=uat` → loads `.env.uat`
- `NODE_ENV=prd` → loads `.env.prd`

## Required Environment Variables

### Core Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NODE_ENV` | ✅ Yes | `dev` | Environment identifier: `dev`, `uat`, or `prd` |
| `PORT` | ✅ Yes | `8000` | API Gateway port (must be 8000) |
| `LOG_LEVEL` | ❌ No | `info` | Logging level: `debug`, `info`, `error` |

### Firebase Configuration

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `FIREBASE_PROJECT_ID` | ✅ Yes | Your Firebase project ID (e.g., `londa-cd054`) | [Firebase Setup](./COMPLETE_ENV_SETUP_GUIDE.md#firebase-setup) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | ⚠️ Conditional | Service account credentials | [Firebase Setup](./COMPLETE_ENV_SETUP_GUIDE.md#firebase-setup) |

**Quick Setup:**

**For Local Development:**
- Set to the path of your service account JSON file:
  ```
  FIREBASE_SERVICE_ACCOUNT_KEY=../../server/service-account-key.json
  ```

**For Cloud Deployment (Render, etc.):**
- Set to the **entire JSON content** of your service account key file
- Copy the entire JSON object (from `{` to `}`)
- Paste it as the value (can be single-line or formatted)

> **📖 For detailed Firebase project setup, service account key creation, and troubleshooting, see [Firebase Setup](./COMPLETE_ENV_SETUP_GUIDE.md#firebase-setup).**

### JWT Authentication

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `JWT_SECRET` | ✅ Yes | Secret key for JWT signing (min 32 chars) | [JWT Secrets Setup](./COMPLETE_ENV_SETUP_GUIDE.md#jwt-secrets-setup) |
| `JWT_REFRESH_SECRET` | ✅ Yes | Secret key for refresh tokens | [JWT Secrets Setup](./COMPLETE_ENV_SETUP_GUIDE.md#jwt-secrets-setup) |
| `ACCESS_TOKEN_SECRET` | ✅ Yes | Secret key for access tokens | [JWT Secrets Setup](./COMPLETE_ENV_SETUP_GUIDE.md#jwt-secrets-setup) |
| `JWT_EXPIRES_IN` | ❌ No | Token expiration time (default: `24h`) | - |

**Quick Generate Secrets:**
```bash
# Generate JWT_SECRET
openssl rand -base64 32

# Generate JWT_REFRESH_SECRET
openssl rand -base64 32

# Generate ACCESS_TOKEN_SECRET
openssl rand -base64 32
```

> **📖 For detailed setup instructions, security best practices, and verification steps, see [JWT Secrets Setup](./COMPLETE_ENV_SETUP_GUIDE.md#jwt-secrets-setup).**

### Email Configuration (SMTP)

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `SMTP_HOST` | ❌ No | SMTP server host (default: `smtp.gmail.com`) | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |
| `SMTP_PORT` | ❌ No | SMTP server port (default: `587`) | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |
| `SMTP_USER` | ✅ Yes | SMTP username/email | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |
| `SMTP_PASS` | ✅ Yes | SMTP password or app password | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |
| `SMTP_FROM` | ❌ No | From email address (default: `noreply@londarides.com`) | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |
| `EMAIL_ACTIVATION_SECRET` | ✅ Yes | Secret for email verification tokens | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |
| `CLIENT_URL` | ✅ Yes | Frontend URL for email links (e.g., `http://localhost:3000`) | [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) |

> **📖 For detailed Gmail App Password setup, other SMTP providers, and troubleshooting, see [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp).**

### SMS/Twilio Configuration (Optional)

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `TWILIO_ACCOUNT_SID` | ❌ No | Twilio Account SID | [Twilio SMS Setup](./COMPLETE_ENV_SETUP_GUIDE.md#twilio-sms-setup) |
| `TWILIO_AUTH_TOKEN` | ❌ No | Twilio Auth Token | [Twilio SMS Setup](./COMPLETE_ENV_SETUP_GUIDE.md#twilio-sms-setup) |
| `TWILIO_PHONE_NUMBER` | ❌ No | Twilio phone number | [Twilio SMS Setup](./COMPLETE_ENV_SETUP_GUIDE.md#twilio-sms-setup) |

> **📖 For detailed Twilio account setup and phone number configuration, see [Twilio SMS Setup](./COMPLETE_ENV_SETUP_GUIDE.md#twilio-sms-setup).**

### Google Maps API

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `GOOGLE_MAPS_API_KEY` | ❌ No | Google Maps API key for geocoding and directions | [Google Maps API Setup](./COMPLETE_ENV_SETUP_GUIDE.md#google-maps-api-setup) |

> **📖 For detailed Google Maps API setup, API enablement, and cost optimization, see [Google Maps API Setup](./COMPLETE_ENV_SETUP_GUIDE.md#google-maps-api-setup) or [Google Maps Setup Guide](./GOOGLE_MAPS_SETUP.md).**

### Nylas Configuration (Optional)

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `NYLAS_API_KEY` | ❌ No | Nylas API key for calendar integration | [Nylas Integration](./COMPLETE_ENV_SETUP_GUIDE.md#nylas-integration-setup) |
| `USER_GRANT_ID` | ❌ No | Nylas user grant ID | [Nylas Integration](./COMPLETE_ENV_SETUP_GUIDE.md#nylas-integration-setup) |

> **📖 For detailed Nylas account setup and grant ID configuration, see [Nylas Integration Setup](./COMPLETE_ENV_SETUP_GUIDE.md#nylas-integration-setup).**

### Socket.IO Configuration

| Variable | Required | Description | Setup Guide |
|----------|----------|-------------|-------------|
| `SOCKET_WS_URL` | ❌ No | WebSocket server URL (default: `ws://localhost:9090`) | [Socket.io Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#socketio-configuration) |
| `SOCKET_SERVER_URL` | ❌ No | Socket HTTP server URL (default: `http://localhost:3001`) | [Socket.io Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#socketio-configuration) |
| `SOCKET_API_SECRET` | ❌ No | Secret for socket route authentication (default: `londa-socket-secret-2024`) | [Socket.io Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#socketio-configuration) |

> **📖 For detailed Socket.io configuration and security best practices, see [Socket.io Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#socketio-configuration).**

## Environment-Specific Examples

### Development (.env.dev)

```bash
NODE_ENV=dev
PORT=8000
LOG_LEVEL=debug

FIREBASE_PROJECT_ID=londa-cd054
FIREBASE_SERVICE_ACCOUNT_KEY=../../server/service-account-key.json

JWT_SECRET=dev-jwt-secret-key-minimum-32-characters-long
JWT_REFRESH_SECRET=dev-refresh-secret-key-minimum-32-characters
ACCESS_TOKEN_SECRET=dev-access-token-secret-minimum-32-characters

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=dev@londarides.com
SMTP_PASS=dev-app-password
SMTP_FROM=noreply@londarides.com
EMAIL_ACTIVATION_SECRET=dev-email-secret
CLIENT_URL=http://localhost:3000

GOOGLE_MAPS_API_KEY=dev-google-maps-key
SOCKET_WS_URL=ws://localhost:9090
SOCKET_SERVER_URL=http://localhost:3001
```

### UAT (.env.uat)

```bash
NODE_ENV=uat
PORT=8000
LOG_LEVEL=info

FIREBASE_PROJECT_ID=londa-cd054
# For UAT, use full JSON content or path to UAT service account key
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}

JWT_SECRET=uat-jwt-secret-key-strong-and-secure-minimum-32-chars
JWT_REFRESH_SECRET=uat-refresh-secret-key-strong-and-secure
ACCESS_TOKEN_SECRET=uat-access-token-secret-strong-and-secure

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=uat@londarides.com
SMTP_PASS=uat-app-password
SMTP_FROM=noreply@londarides.com
EMAIL_ACTIVATION_SECRET=uat-email-secret
CLIENT_URL=https://uat.londarides.com

GOOGLE_MAPS_API_KEY=uat-google-maps-key
SOCKET_WS_URL=wss://socket-uat.londarides.com
SOCKET_SERVER_URL=https://socket-uat.londarides.com
```

### Production (.env.prd)

```bash
NODE_ENV=prd
PORT=8000
LOG_LEVEL=error

FIREBASE_PROJECT_ID=londa-cd054
# For production, ALWAYS use full JSON content (never file paths)
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}

JWT_SECRET=prd-jwt-secret-key-very-strong-and-secure-minimum-32-chars
JWT_REFRESH_SECRET=prd-refresh-secret-key-very-strong-and-secure
ACCESS_TOKEN_SECRET=prd-access-token-secret-very-strong-and-secure

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=prd@londarides.com
SMTP_PASS=prd-app-password
SMTP_FROM=noreply@londarides.com
EMAIL_ACTIVATION_SECRET=prd-email-secret
CLIENT_URL=https://londarides.com

GOOGLE_MAPS_API_KEY=prd-google-maps-key
SOCKET_WS_URL=wss://socket.londarides.com
SOCKET_SERVER_URL=https://socket.londarides.com
```

## Security Best Practices

1. **Never commit `.env` files to version control**
   - Add `.env*` to `.gitignore`
   - Only commit `.env.example` as a template

2. **Use strong secrets**
   - Minimum 32 characters for JWT secrets
   - Use different secrets for each environment
   - Rotate secrets regularly in production

3. **For cloud deployment:**
   - Use environment variables in your hosting platform (Render, Heroku, etc.)
   - Never hardcode secrets in code
   - Use secrets management services for production

4. **Firebase Service Account:**
   - In cloud: Use full JSON content (not file paths)
   - In local: File paths are acceptable
   - Restrict service account permissions to minimum required

## Migration from Microservices

If you're migrating from the old microservices architecture:

1. **Consolidate variables** from:
   - `server/.env.*`
   - `services/auth-service/.env.*`
   - `services/user-service/.env.*`
   - `services/driver-service/.env.*`
   - `services/ride-service/.env.*`

2. **Remove microservice-specific variables:**
   - `USER_SERVICE_URL`
   - `DRIVER_SERVICE_URL`
   - `AUTH_SERVICE_URL`
   - `RIDE_SERVICE_URL`
   - `USE_MICROSERVICES`

3. **Keep unified variables:**
   - All Firebase variables
   - All JWT variables
   - All SMTP variables
   - All API keys

## Troubleshooting

### Issue: "FIREBASE_SERVICE_ACCOUNT_KEY contains a file path"

**Error:** The system expects JSON content in cloud environments.

**Solution:** 
- For local: Use file path (e.g., `../../server/service-account-key.json`)
- For cloud: Use full JSON content

### Issue: "JWT_SECRET not set"

**Error:** JWT authentication fails.

**Solution:**
- Generate a secret: `openssl rand -base64 32`
- Set it in your `.env.*` file
- Ensure it's at least 32 characters

### Issue: "Port 8000 is already in use"

**Solution:**
- Check if another service is running on port 8000
- Ensure `PORT=8000` is set correctly
- Stop any conflicting services

## Testing Your Configuration

After setting up environment variables:

1. **Start the unified API:**
   ```bash
   cd services/api-gateway
   npm run dev
   ```

2. **Check health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Check logs** for any initialization errors

4. **Test authentication:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/register \
     -H "Content-Type: application/json" \
     -d '{"phone_number": "+264811234567"}'
   ```

## Additional Resources

- **[Complete Environment Variables Setup Guide](./COMPLETE_ENV_SETUP_GUIDE.md)** - Detailed step-by-step setup for all environment variables
- [Firebase Setup Guide](./firebase-migration-guide.md)
- [Google Maps API Setup](./GOOGLE_MAPS_SETUP.md)
- [Render Deployment Guide](../deployment/RENDER_DEPLOYMENT_GUIDE.md)

## Quick Links to Detailed Setup

- [JWT Secrets Setup](./COMPLETE_ENV_SETUP_GUIDE.md#jwt-secrets-setup) - Generate and configure JWT secrets
- [Email Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#email-configuration-smtp) - Gmail App Password and SMTP setup
- [Firebase Setup](./COMPLETE_ENV_SETUP_GUIDE.md#firebase-setup) - Service account key and project configuration
- [Google Maps API Setup](./COMPLETE_ENV_SETUP_GUIDE.md#google-maps-api-setup) - API key creation and configuration
- [Nylas Integration](./COMPLETE_ENV_SETUP_GUIDE.md#nylas-integration-setup) - Calendar integration setup
- [Twilio SMS Setup](./COMPLETE_ENV_SETUP_GUIDE.md#twilio-sms-setup) - SMS/OTP functionality setup
- [Socket.io Configuration](./COMPLETE_ENV_SETUP_GUIDE.md#socketio-configuration) - Real-time communication setup
- [Troubleshooting](./COMPLETE_ENV_SETUP_GUIDE.md#troubleshooting) - Common issues and solutions

