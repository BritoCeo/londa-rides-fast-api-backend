# Complete Environment Variables Setup Guide

## Overview

This comprehensive guide provides step-by-step instructions for setting up all environment variables required for the Londa Rides Unified API Gateway. This guide complements the [Environment Setup Unified Guide](./ENVIRONMENT_SETUP_UNIFIED.md) by providing detailed setup instructions for each variable.

## Quick Reference Table

| Variable | Required | Priority | Setup Guide |
|----------|----------|-----------|-------------|
| `NODE_ENV` | ✅ Yes | Critical | [Core Configuration](#core-configuration) |
| `PORT` | ✅ Yes | Critical | [Core Configuration](#core-configuration) |
| `FIREBASE_PROJECT_ID` | ✅ Yes | Critical | [Firebase Setup](#firebase-setup) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | ✅ Yes | Critical | [Firebase Setup](#firebase-setup) |
| `JWT_SECRET` | ✅ Yes | Critical | [JWT Secrets Setup](#jwt-secrets-setup) |
| `JWT_REFRESH_SECRET` | ✅ Yes | Critical | [JWT Secrets Setup](#jwt-secrets-setup) |
| `ACCESS_TOKEN_SECRET` | ✅ Yes | Critical | [JWT Secrets Setup](#jwt-secrets-setup) |
| `EMAIL_ACTIVATION_SECRET` | ✅ Yes | Critical | [Email Configuration](#email-configuration-smtp) |
| `SMTP_USER` | ✅ Yes | Critical | [Email Configuration](#email-configuration-smtp) |
| `SMTP_PASS` | ✅ Yes | Critical | [Email Configuration](#email-configuration-smtp) |
| `CLIENT_URL` | ✅ Yes | Critical | [Email Configuration](#email-configuration-smtp) |
| `GOOGLE_MAPS_API_KEY` | ⚠️ Important | High | [Google Maps API](#google-maps-api-setup) |
| `NYLAS_API_KEY` | ❌ Optional | Medium | [Nylas Integration](#nylas-integration-setup) |
| `USER_GRANT_ID` | ❌ Optional | Medium | [Nylas Integration](#nylas-integration-setup) |
| `TWILIO_ACCOUNT_SID` | ❌ Optional | Low | [Twilio SMS Setup](#twilio-sms-setup) |
| `TWILIO_AUTH_TOKEN` | ❌ Optional | Low | [Twilio SMS Setup](#twilio-sms-setup) |
| `TWILIO_PHONE_NUMBER` | ❌ Optional | Low | [Twilio SMS Setup](#twilio-sms-setup) |
| `SOCKET_WS_URL` | ❌ Optional | Low | [Socket.io Configuration](#socketio-configuration) |
| `SOCKET_SERVER_URL` | ❌ Optional | Low | [Socket.io Configuration](#socketio-configuration) |
| `SOCKET_API_SECRET` | ❌ Optional | Low | [Socket.io Configuration](#socketio-configuration) |

---

## Core Configuration

### NODE_ENV

**Required:** Yes  
**Default:** `dev`  
**Values:** `dev`, `uat`, `prd`

#### Setup Steps

1. **For Development:**
   ```bash
   NODE_ENV=dev
   ```

2. **For UAT/Staging:**
   ```bash
   NODE_ENV=uat
   ```

3. **For Production:**
   ```bash
   NODE_ENV=prd
   ```

#### Verification

The application automatically loads the corresponding `.env.{NODE_ENV}` file. Check your logs to confirm the correct environment is loaded.

---

### PORT

**Required:** Yes  
**Default:** `8000`  
**Fixed Value:** Must be `8000` for the unified API gateway

#### Setup Steps

Simply set:
```bash
PORT=8000
```

#### Verification

After starting the server, check that it's listening on port 8000:
```bash
curl http://localhost:8000/health
```

---

## JWT Secrets Setup

The application requires three separate JWT secrets for different token types. **Never reuse the same secret for multiple variables.**

### JWT_SECRET

**Required:** Yes  
**Purpose:** Signs and verifies main JWT authentication tokens  
**Minimum Length:** 32 characters

#### Setup Steps

1. **Generate a secure secret:**
   ```bash
   openssl rand -base64 32
   ```

2. **Copy the output** (it will look like: `aBc123XyZ...`)

3. **Add to your `.env.dev` file:**
   ```bash
   JWT_SECRET=your-generated-secret-here-minimum-32-characters
   ```

4. **Generate different secrets for each environment:**
   - Development: Use a simple but secure secret
   - UAT: Use a strong production-like secret
   - Production: Use a very strong, randomly generated secret

#### Security Best Practices

- ✅ Use different secrets for each environment
- ✅ Minimum 32 characters
- ✅ Use cryptographically secure random generation
- ✅ Rotate secrets periodically in production
- ❌ Never commit secrets to version control
- ❌ Never reuse secrets across environments

#### Verification

Test authentication endpoints:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'
```

If JWT_SECRET is missing or invalid, you'll get authentication errors.

---

### JWT_REFRESH_SECRET

**Required:** Yes  
**Purpose:** Signs and verifies refresh tokens (used for token renewal)  
**Minimum Length:** 32 characters

#### Setup Steps

1. **Generate a secure secret:**
   ```bash
   openssl rand -base64 32
   ```

2. **Add to your `.env.dev` file:**
   ```bash
   JWT_REFRESH_SECRET=your-generated-refresh-secret-here
   ```

3. **Important:** This must be different from `JWT_SECRET` and `ACCESS_TOKEN_SECRET`

#### Verification

Test refresh token endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refreshToken": "your-refresh-token"}'
```

---

### ACCESS_TOKEN_SECRET

**Required:** Yes  
**Purpose:** Signs and verifies access tokens for user authentication  
**Minimum Length:** 32 characters

#### Setup Steps

1. **Generate a secure secret:**
   ```bash
   openssl rand -base64 32
   ```

2. **Add to your `.env.dev` file:**
   ```bash
   ACCESS_TOKEN_SECRET=your-generated-access-token-secret-here
   ```

3. **Important:** This must be different from both `JWT_SECRET` and `JWT_REFRESH_SECRET`

#### Quick Setup Script

You can generate all three secrets at once:

```bash
# Generate all JWT secrets
echo "JWT_SECRET=$(openssl rand -base64 32)"
echo "JWT_REFRESH_SECRET=$(openssl rand -base64 32)"
echo "ACCESS_TOKEN_SECRET=$(openssl rand -base64 32)"
```

Copy the output to your `.env.dev` file.

---

## Email Configuration (SMTP)

Email functionality requires SMTP credentials and configuration for sending verification emails, ride confirmations, and password resets.

### SMTP_USER

**Required:** Yes  
**Purpose:** SMTP server username (usually your email address)

#### Setup Steps

1. **Choose an email account** for sending emails (e.g., `noreply@londarides.com`)

2. **For Gmail:**
   - Use your full Gmail address: `your-email@gmail.com`
   - You'll need to create an App Password (see `SMTP_PASS` below)

3. **For other providers:**
   - Use the email address associated with your SMTP account

4. **Add to your `.env.dev` file:**
   ```bash
   SMTP_USER=your-email@gmail.com
   ```

---

### SMTP_PASS

**Required:** Yes  
**Purpose:** SMTP server password or app password

#### Setup Steps for Gmail

1. **Enable 2-Step Verification:**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification if not already enabled

2. **Generate App Password:**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" as the app
   - Select "Other (Custom name)" as the device
   - Enter "Londa Rides API" as the name
   - Click "Generate"
   - **Copy the 16-character password** (spaces will be removed automatically)

3. **Add to your `.env.dev` file:**
   ```bash
   SMTP_PASS=your-16-character-app-password
   ```

#### Setup Steps for Other SMTP Providers

**SendGrid:**
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your-sendgrid-api-key
```

**Mailgun:**
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=your-mailgun-username
SMTP_PASS=your-mailgun-password
```

**Custom SMTP:**
```bash
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USER=your-username
SMTP_PASS=your-password
```

#### Verification

Test email sending by registering a new user or requesting a password reset. Check your email inbox for the verification email.

---

### CLIENT_URL

**Required:** Yes  
**Purpose:** Frontend URL used in email verification and password reset links

#### Setup Steps

1. **For Development:**
   ```bash
   CLIENT_URL=http://localhost:3000
   ```
   (Replace `3000` with your frontend development port)

2. **For UAT:**
   ```bash
   CLIENT_URL=https://uat.londarides.com
   ```

3. **For Production:**
   ```bash
   CLIENT_URL=https://londarides.com
   ```

#### Important Notes

- Must include the protocol (`http://` or `https://`)
- Must not include trailing slash
- This URL is embedded in email links, so it must be accessible to users

#### Verification

Check that email verification links work by:
1. Registering a new user
2. Opening the verification email
3. Clicking the verification link
4. Verifying it redirects to your frontend correctly

---

### EMAIL_ACTIVATION_SECRET

**Required:** Yes  
**Purpose:** Secret key for signing email verification tokens  
**Minimum Length:** 32 characters recommended

#### Setup Steps

1. **Generate a secure secret:**
   ```bash
   openssl rand -base64 32
   ```

2. **Add to your `.env.dev` file:**
   ```bash
   EMAIL_ACTIVATION_SECRET=your-generated-email-activation-secret
   ```

3. **Use different secrets for each environment**

#### Verification

Email verification tokens should work correctly. If tokens are invalid, check that this secret matches between token generation and verification.

---

### SMTP_HOST and SMTP_PORT

**Required:** No (have defaults)  
**Defaults:** `smtp.gmail.com` and `587`

#### Setup Steps

**For Gmail (default):**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**For other providers:**
- Check your email provider's SMTP settings
- Common ports: `587` (TLS), `465` (SSL), `25` (unencrypted, not recommended)

---

### SMTP_FROM

**Required:** No (has default)  
**Default:** `noreply@londarides.com`

#### Setup Steps

Set the "From" address for all emails:
```bash
SMTP_FROM=noreply@londarides.com
```

**Important:** Some email providers require the `SMTP_FROM` address to match your `SMTP_USER` address.

---

## Firebase Setup

Firebase is used for database (Firestore) and authentication. You need a Firebase project and service account credentials.

### FIREBASE_PROJECT_ID

**Required:** Yes  
**Purpose:** Identifies your Firebase project

#### Setup Steps

1. **Go to [Firebase Console](https://console.firebase.google.com/)**

2. **Create or select a project:**
   - Click "Add project" or select existing project
   - Note the Project ID (e.g., `londa-cd054`)

3. **Find your Project ID:**
   - Go to Project Settings (gear icon)
   - The Project ID is displayed at the top

4. **Add to your `.env.dev` file:**
   ```bash
   FIREBASE_PROJECT_ID=londa-cd054
   ```

#### Verification

The Project ID should match the `project_id` in your service account key JSON file.

---

### FIREBASE_SERVICE_ACCOUNT_KEY

**Required:** Yes  
**Purpose:** Credentials for Firebase Admin SDK to access Firestore

#### Setup Steps

1. **Go to Firebase Console:**
   - Navigate to [Firebase Console](https://console.firebase.google.com/)
   - Select your project

2. **Open Project Settings:**
   - Click the gear icon next to "Project Overview"
   - Select "Project settings"

3. **Go to Service Accounts tab:**
   - Click on "Service accounts" tab
   - You'll see "Firebase Admin SDK"

4. **Generate New Private Key:**
   - Click "Generate new private key"
   - Confirm the dialog
   - A JSON file will be downloaded (e.g., `londa-cd054-firebase-adminsdk-xxxxx.json`)

5. **For Local Development:**
   - Save the JSON file in a secure location (e.g., `server/service-account-key.json`)
   - **Important:** Add this file to `.gitignore` to prevent committing it
   - Set the path in your `.env.dev`:
     ```bash
     FIREBASE_SERVICE_ACCOUNT_KEY=../../server/service-account-key.json
     ```

6. **For Cloud Deployment (Render, etc.):**
   - Open the downloaded JSON file
   - Copy the **entire JSON content** (from `{` to `}`)
   - In your hosting platform's environment variables, set:
     ```bash
     FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"londa-cd054",...}
     ```
   - Paste the entire JSON as a single-line string (or formatted, the system will parse it)

#### Security Best Practices

- ✅ Never commit service account keys to version control
- ✅ Restrict service account permissions to minimum required
- ✅ Use different service accounts for different environments
- ✅ Rotate keys periodically
- ✅ In cloud: Always use JSON content (not file paths)

#### Verification

1. **Check Firestore connection:**
   ```bash
   # Start the API
   npm run dev
   
   # Check logs for:
   # "🔥 Firestore initialized successfully with service account key"
   ```

2. **Test database operations:**
   - Try creating a user via the registration endpoint
   - Check Firebase Console to see if data is written

#### Troubleshooting

**Error: "FIREBASE_SERVICE_ACCOUNT_KEY contains a file path"**
- **Solution:** In cloud environments, you must use JSON content, not file paths. Copy the entire JSON content from your service account key file.

**Error: "Failed to parse FIREBASE_SERVICE_ACCOUNT_KEY as JSON"**
- **Solution:** Ensure the JSON is valid. Remove any extra spaces or newlines if pasting as a single line.

**Error: "Permission denied"**
- **Solution:** Check that your service account has the necessary Firestore permissions in Firebase Console.

---

## Google Maps API Setup

Google Maps API is used for geocoding, directions, distance calculations, and fare estimation.

### GOOGLE_MAPS_API_KEY

**Required:** No (has fallback, but recommended)  
**Purpose:** Enables accurate maps, geocoding, and directions

#### Setup Steps

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**

2. **Create or select a project:**
   - Create a new project or select your existing Firebase project
   - Note: You can use the same project as Firebase

3. **Enable Required APIs:**
   - Go to "APIs & Services" → "Library"
   - Enable the following APIs:
     - **Maps JavaScript API**
     - **Geocoding API**
     - **Distance Matrix API**
     - **Directions API**
     - **Places API**

4. **Create API Key:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the generated API key

5. **Restrict API Key (Recommended for Security):**
   - Click on the API key to edit it
   - Under "API restrictions":
     - Select "Restrict key"
     - Choose the APIs you enabled above
   - Under "Application restrictions":
     - For server-side: Select "IP addresses" and add your server IPs
     - For client-side: Select "HTTP referrers" and add your domains

6. **Add to your `.env.dev` file:**
   ```bash
   GOOGLE_MAPS_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### Cost Considerations

- Google Maps API has usage-based pricing
- Set up billing alerts in Google Cloud Console
- Monitor usage in "APIs & Services" → "Dashboard"
- Consider implementing caching to reduce API calls

#### Verification

Test the geocoding functionality:
```bash
curl -X GET "http://localhost:8000/api/v1/maps/geocode?address=Windhoek, Namibia"
```

If the API key is missing, the system will use fallback calculations (less accurate).

#### Additional Resources

See [Google Maps API Setup Guide](./GOOGLE_MAPS_SETUP.md) for detailed usage examples.

---

## Nylas Integration Setup

Nylas is used for calendar integration features (optional).

### NYLAS_API_KEY

**Required:** No (only if using calendar features)  
**Purpose:** Authenticates with Nylas API for calendar integration

#### Setup Steps

1. **Create Nylas Account:**
   - Go to [Nylas Dashboard](https://dashboard.nylas.com/)
   - Sign up for an account

2. **Create an Application:**
   - Click "Create Application"
   - Enter application name (e.g., "Londa Rides")
   - Select your region (e.g., "EU" for European servers)

3. **Get API Key:**
   - In your application dashboard, find "API Keys"
   - Copy the "Client ID" or "API Key"
   - Note: You may also need a "Client Secret"

4. **Add to your `.env.dev` file:**
   ```bash
   NYLAS_API_KEY=your-nylas-api-key-here
   ```

#### Verification

Check that Nylas is initialized in application logs. If the API key is invalid, you'll see errors when trying to use calendar features.

---

### USER_GRANT_ID

**Required:** No (only if using calendar features)  
**Purpose:** Identifies a specific user's calendar grant in Nylas

#### Setup Steps

1. **Create a User Grant:**
   - This is typically done programmatically when a user connects their calendar
   - The grant ID is returned after OAuth authentication

2. **For Testing:**
   - You can create a test grant through the Nylas dashboard
   - Or use the Nylas API to create a grant

3. **Add to your `.env.dev` file:**
   ```bash
   USER_GRANT_ID=your-nylas-grant-id-here
   ```

#### Important Notes

- Grant IDs are user-specific
- Each user connecting their calendar will have a different grant ID
- In production, grant IDs should be stored per user in your database, not in environment variables

---

## Twilio SMS Setup

Twilio is used for SMS/OTP functionality (optional, email can be used instead).

### TWILIO_ACCOUNT_SID

**Required:** No (only if using SMS features)  
**Purpose:** Identifies your Twilio account

#### Setup Steps

1. **Create Twilio Account:**
   - Go to [Twilio Console](https://console.twilio.com/)
   - Sign up for an account (free trial available)

2. **Get Account SID:**
   - After logging in, your Account SID is displayed on the dashboard
   - It looks like: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Add to your `.env.dev` file:**
   ```bash
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### TWILIO_AUTH_TOKEN

**Required:** No (only if using SMS features)  
**Purpose:** Authenticates API requests to Twilio

#### Setup Steps

1. **Get Auth Token:**
   - In Twilio Console, go to "Account" → "Auth Token"
   - Click "View" to reveal your auth token
   - Copy the token

2. **Add to your `.env.dev` file:**
   ```bash
   TWILIO_AUTH_TOKEN=your-twilio-auth-token-here
   ```

#### Security

- Keep your auth token secret
- Never commit it to version control
- Regenerate it if compromised

---

### TWILIO_PHONE_NUMBER

**Required:** No (only if using SMS features)  
**Purpose:** The phone number that sends SMS messages

#### Setup Steps

1. **Get a Twilio Phone Number:**
   - In Twilio Console, go to "Phone Numbers" → "Manage" → "Buy a number"
   - Select your country/region
   - Choose a number with SMS capability
   - Complete the purchase (free trial includes a number)

2. **Copy the Phone Number:**
   - Format: `+1234567890` (with country code)

3. **Add to your `.env.dev` file:**
   ```bash
   TWILIO_PHONE_NUMBER=+1234567890
   ```

#### Verification

Test SMS sending by triggering an OTP request. Check your phone for the SMS message.

---

## Socket.io Configuration

Socket.io is used for real-time communication (optional, has defaults).

### SOCKET_WS_URL

**Required:** No (has default)  
**Default:** `ws://localhost:9090`  
**Purpose:** WebSocket URL for Socket.io client connections

#### Setup Steps

**For Development:**
```bash
SOCKET_WS_URL=ws://localhost:9090
```

**For UAT:**
```bash
SOCKET_WS_URL=wss://socket-uat.londarides.com
```

**For Production:**
```bash
SOCKET_WS_URL=wss://socket.londarides.com
```

**Note:** Use `ws://` for HTTP and `wss://` for HTTPS.

---

### SOCKET_SERVER_URL

**Required:** No (has default)  
**Default:** `http://localhost:3001`  
**Purpose:** HTTP URL for Socket.io server API endpoints

#### Setup Steps

**For Development:**
```bash
SOCKET_SERVER_URL=http://localhost:3001
```

**For UAT:**
```bash
SOCKET_SERVER_URL=https://socket-uat.londarides.com
```

**For Production:**
```bash
SOCKET_SERVER_URL=https://socket.londarides.com
```

---

### SOCKET_API_SECRET

**Required:** No (has default)  
**Default:** `londa-socket-secret-2024`  
**Purpose:** Secret for authenticating Socket.io API routes

#### Setup Steps

1. **Generate a secure secret:**
   ```bash
   openssl rand -base64 32
   ```

2. **Add to your `.env.dev` file:**
   ```bash
   SOCKET_API_SECRET=your-socket-api-secret-here
   ```

3. **Use different secrets for each environment**

#### Security

- Change the default secret in production
- Use strong, randomly generated secrets
- Keep it secret and never commit to version control

---

## Environment-Specific Setup Examples

### Development Environment (.env.dev)

```bash
# Core
NODE_ENV=dev
PORT=8000
LOG_LEVEL=debug

# Firebase
FIREBASE_PROJECT_ID=londa-cd054
FIREBASE_SERVICE_ACCOUNT_KEY=../../server/service-account-key.json

# JWT Secrets
JWT_SECRET=dev-jwt-secret-minimum-32-characters-long-here
JWT_REFRESH_SECRET=dev-refresh-secret-minimum-32-characters
ACCESS_TOKEN_SECRET=dev-access-token-secret-minimum-32-chars

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=dev@londarides.com
SMTP_PASS=your-gmail-app-password
SMTP_FROM=noreply@londarides.com
EMAIL_ACTIVATION_SECRET=dev-email-activation-secret
CLIENT_URL=http://localhost:3000

# Google Maps (optional but recommended)
GOOGLE_MAPS_API_KEY=your-dev-google-maps-key

# Socket.io (optional)
SOCKET_WS_URL=ws://localhost:9090
SOCKET_SERVER_URL=http://localhost:3001
SOCKET_API_SECRET=dev-socket-secret
```

### UAT Environment (.env.uat)

```bash
# Core
NODE_ENV=uat
PORT=8000
LOG_LEVEL=info

# Firebase
FIREBASE_PROJECT_ID=londa-cd054
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"londa-cd054",...}

# JWT Secrets (use strong secrets)
JWT_SECRET=uat-strong-jwt-secret-minimum-32-characters
JWT_REFRESH_SECRET=uat-strong-refresh-secret-minimum-32-chars
ACCESS_TOKEN_SECRET=uat-strong-access-token-secret-32-chars

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=uat@londarides.com
SMTP_PASS=uat-gmail-app-password
SMTP_FROM=noreply@londarides.com
EMAIL_ACTIVATION_SECRET=uat-email-activation-secret
CLIENT_URL=https://uat.londarides.com

# Google Maps
GOOGLE_MAPS_API_KEY=uat-google-maps-key

# Socket.io
SOCKET_WS_URL=wss://socket-uat.londarides.com
SOCKET_SERVER_URL=https://socket-uat.londarides.com
SOCKET_API_SECRET=uat-socket-secret
```

### Production Environment (.env.prd)

```bash
# Core
NODE_ENV=prd
PORT=8000
LOG_LEVEL=error

# Firebase
FIREBASE_PROJECT_ID=londa-cd054
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"londa-cd054",...}

# JWT Secrets (use very strong, randomly generated secrets)
JWT_SECRET=prd-very-strong-randomly-generated-secret-32-chars-min
JWT_REFRESH_SECRET=prd-very-strong-randomly-generated-refresh-secret
ACCESS_TOKEN_SECRET=prd-very-strong-randomly-generated-access-secret

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=prd@londarides.com
SMTP_PASS=prd-gmail-app-password
SMTP_FROM=noreply@londarides.com
EMAIL_ACTIVATION_SECRET=prd-very-strong-email-activation-secret
CLIENT_URL=https://londarides.com

# Google Maps
GOOGLE_MAPS_API_KEY=prd-google-maps-key

# Socket.io
SOCKET_WS_URL=wss://socket.londarides.com
SOCKET_SERVER_URL=https://socket.londarides.com
SOCKET_API_SECRET=prd-very-strong-socket-secret
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "JWT_SECRET not set" or Authentication Fails

**Symptoms:**
- Authentication endpoints return errors
- Tokens are rejected

**Solution:**
1. Verify `JWT_SECRET` is set in your `.env.{NODE_ENV}` file
2. Ensure it's at least 32 characters
3. Check for typos or extra spaces
4. Restart the server after adding the variable

---

#### Issue: Email Not Sending

**Symptoms:**
- Registration emails don't arrive
- Password reset emails don't arrive

**Solution:**
1. **Check SMTP credentials:**
   - Verify `SMTP_USER` and `SMTP_PASS` are correct
   - For Gmail, ensure you're using an App Password (not your regular password)

2. **Check Gmail App Password:**
   - Ensure 2-Step Verification is enabled
   - Generate a new App Password if needed

3. **Check SMTP settings:**
   - Verify `SMTP_HOST` and `SMTP_PORT` are correct
   - Try `SMTP_PORT=465` with `secure: true` if 587 doesn't work

4. **Check logs:**
   - Look for SMTP connection errors in server logs
   - Check for authentication failures

---

#### Issue: Firebase Connection Fails

**Symptoms:**
- Database operations fail
- "Firestore initialization failed" in logs

**Solution:**
1. **For Local Development:**
   - Verify the file path in `FIREBASE_SERVICE_ACCOUNT_KEY` is correct
   - Ensure the JSON file exists and is readable
   - Check file permissions

2. **For Cloud Deployment:**
   - Ensure `FIREBASE_SERVICE_ACCOUNT_KEY` contains the full JSON content
   - Verify the JSON is valid (no syntax errors)
   - Check that it's not a file path in cloud environments

3. **Check Project ID:**
   - Verify `FIREBASE_PROJECT_ID` matches your Firebase project
   - Ensure it matches the `project_id` in your service account key

---

#### Issue: Google Maps API Errors

**Symptoms:**
- Geocoding fails
- Distance calculations are inaccurate

**Solution:**
1. **Verify API Key:**
   - Check that `GOOGLE_MAPS_API_KEY` is set correctly
   - Ensure there are no extra spaces

2. **Check API Restrictions:**
   - Verify the API key has the required APIs enabled
   - Check IP/domain restrictions if applicable

3. **Check Billing:**
   - Ensure billing is enabled in Google Cloud Console
   - Check for quota exceeded errors

4. **Fallback Mode:**
   - If API key is missing, the system uses fallback calculations
   - These are less accurate but functional

---

#### Issue: Port 8000 Already in Use

**Symptoms:**
- Server fails to start
- "EADDRINUSE" error

**Solution:**
1. **Find the process using port 8000:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

2. **Stop the conflicting process:**
   - Kill the process using the PID from above
   - Or change the port (not recommended, must be 8000)

---

### Verification Checklist

Use this checklist to verify your environment setup:

- [ ] `NODE_ENV` is set correctly (`dev`, `uat`, or `prd`)
- [ ] `PORT` is set to `8000`
- [ ] `FIREBASE_PROJECT_ID` matches your Firebase project
- [ ] `FIREBASE_SERVICE_ACCOUNT_KEY` is configured (file path for local, JSON for cloud)
- [ ] `JWT_SECRET` is at least 32 characters
- [ ] `JWT_REFRESH_SECRET` is at least 32 characters and different from `JWT_SECRET`
- [ ] `ACCESS_TOKEN_SECRET` is at least 32 characters and different from other secrets
- [ ] `SMTP_USER` is set to a valid email address
- [ ] `SMTP_PASS` is set (App Password for Gmail)
- [ ] `CLIENT_URL` is set to your frontend URL
- [ ] `EMAIL_ACTIVATION_SECRET` is set
- [ ] `GOOGLE_MAPS_API_KEY` is set (optional but recommended)
- [ ] Server starts without errors
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] Authentication works (test registration/login)
- [ ] Email sending works (test registration)
- [ ] Database operations work (check Firebase Console)

---

## Start Commands Reference

This section provides a complete reference for all available start commands in the Londa Rides backend.

### Quick Start (Recommended)

**For Development:**
```bash
# From root directory (backend/)
npm run dev:all
```

This starts the unified API gateway in development mode using `.env.dev`.

---

### Unified API Gateway Commands

The unified API gateway is the main entry point for all API requests. All commands should be run from the **root directory** (`backend/`).

#### Development Mode (with hot reload)

```bash
# Start in development mode (uses .env.dev)
npm run dev:all

# Or explicitly specify dev environment
npm run dev:all:dev

# Alternative: Directly from api-gateway directory
cd services/api-gateway
npm run dev
npm run dev:dev
```

#### UAT/Staging Mode

```bash
# Start in UAT mode (uses .env.uat)
npm run dev:all:uat

# Or from api-gateway directory
cd services/api-gateway
npm run dev:uat
```

#### Production Mode

```bash
# Start in production mode (uses .env.prd)
npm run dev:all:prd

# Or from api-gateway directory
cd services/api-gateway
npm run dev:prd
```

#### Production Build & Start (Compiled)

```bash
# Build first
cd services/api-gateway
npm run build

# Then start (uses .env.dev by default)
npm start

# Or specify environment
npm run start:dev    # Uses .env.dev
npm run start:uat     # Uses .env.uat
npm run start:prd     # Uses .env.prd
```

---

### Root Directory Commands

All commands below should be run from the **`backend/`** directory.

#### Installation & Build

```bash
# Install all dependencies (root + shared + all services)
npm run install:all

# Build shared package (required before running services)
npm run build:shared

# Build all services
npm run build:all

# Clean build artifacts
npm run clean
```

#### Development Commands

```bash
# Start unified API gateway (recommended)
npm run dev:all
npm run dev:unified
npm run dev:all:dev      # Explicitly dev environment
npm run dev:all:uat      # UAT environment
npm run dev:all:prd      # Production environment
```

#### Legacy Microservices Commands (Not Recommended)

These commands are for the old microservices architecture. Use `dev:all` instead.

```bash
# Individual services (legacy - not needed with unified gateway)
npm run dev:user         # User service (port 8002)
npm run dev:driver       # Driver service (port 8003)
npm run dev:auth         # Auth service (port 8001)
npm run dev:ride         # Ride service (port 8004)
npm run dev:gateway      # API Gateway (port 8000)
npm run dev:main         # Legacy main server (port 3001)

# Run all legacy services concurrently
npm run dev:all:legacy
```

#### UAT Commands

```bash
# Start unified API gateway in UAT mode
npm run uat:all

# Legacy individual UAT services
npm run uat:user
npm run uat:driver
npm run uat:auth
npm run uat:ride
npm run uat:gateway
npm run uat:all:legacy
```

---

### API Gateway Service Commands

Run these from `services/api-gateway/` directory:

#### Development (TypeScript with hot reload)

```bash
cd services/api-gateway

# Development mode (auto-detects .env.dev)
npm run dev
npm run dev:dev          # Explicitly dev
npm run dev:uat          # UAT environment
npm run dev:prd          # Production environment
```

#### Production (Compiled JavaScript)

```bash
cd services/api-gateway

# Build TypeScript to JavaScript
npm run build

# Start compiled version
npm start                 # Default environment
npm run start:dev         # Dev environment
npm run start:uat         # UAT environment
npm run start:prd         # Production environment
```

---

### Socket Server Commands

The Socket.io server runs separately for real-time communication. Run from `socket/` directory:

```bash
cd socket

# Development mode (with nodemon auto-reload)
npm run dev

# Production mode
npm start

# Clean version (alternative implementation)
npm run dev:clean
npm run start:clean
```

**Socket Server Defaults:**
- HTTP Server: `http://localhost:3001`
- WebSocket: `ws://localhost:9090`

---

### Legacy Server Commands

The legacy server in `server/` directory. Run from `server/` directory:

```bash
cd server

# Development mode
npm run dev               # Default port
npm run dev:3001         # Port 3001
npm run dev:4000         # Port 4000

# Production mode
npm run build            # Build first
npm start                 # Default port
npm run start:3001       # Port 3001
npm run start:4000       # Port 4000
```

---

### Command Summary Table

| Command | Location | Environment | Description |
|---------|----------|-------------|-------------|
| `npm run dev:all` | Root | dev | Start API gateway + Socket server (recommended) |
| `npm run dev:all:dev` | Root | dev | Start API gateway (explicit dev) |
| `npm run dev:all:uat` | Root | uat | Start API gateway (UAT) |
| `npm run dev:all:prd` | Root | prd | Start API gateway (production) |
| `npm run dev:socket` | Root | - | Start Socket server only |
| `npm run dev` | api-gateway/ | dev | Start API gateway (development) |
| `npm run dev:uat` | api-gateway/ | uat | Start API gateway (UAT) |
| `npm run dev:prd` | api-gateway/ | prd | Start API gateway (production) |
| `npm start` | api-gateway/ | dev | Start compiled API gateway |
| `npm run start:uat` | api-gateway/ | uat | Start compiled API gateway (UAT) |
| `npm run start:prd` | api-gateway/ | prd | Start compiled API gateway (production) |
| `npm run dev` | socket/ | - | Start Socket.io server (development) |
| `npm start` | socket/ | - | Start Socket.io server (production) |

---

### Environment File Loading

The system automatically loads the correct environment file based on `NODE_ENV`:

- `NODE_ENV=dev` → loads `.env.dev`
- `NODE_ENV=uat` → loads `.env.uat`
- `NODE_ENV=prd` → loads `.env.prd`

**Important:** Make sure the corresponding `.env.{NODE_ENV}` file exists in `services/api-gateway/` directory.

---

### Typical Development Workflow

1. **Install dependencies:**
   ```bash
   npm run install:all
   ```

2. **Build shared package:**
   ```bash
   npm run build:shared
   ```

3. **Start API gateway and Socket server:**
   ```bash
   npm run dev:all
   ```

   This command starts both the API Gateway (port 8000) and Socket Server (port 9090) concurrently.

4. **Start Socket server individually (optional):**
   ```bash
   npm run dev:socket
   # or
   cd socket
   npm run dev
   ```

---

### Ports Reference

| Service | Port | Environment Variable |
|---------|------|---------------------|
| Unified API Gateway | 8000 | `PORT=8000` (fixed) |
| Socket HTTP Server | 3001 | `SOCKET_SERVER_URL` |
| Socket WebSocket | 9090 | `SOCKET_WS_URL` |
| Legacy Server | 3001/4000 | `PORT` |

---

### Troubleshooting Start Commands

#### Issue: "Cannot find module"

**Solution:**
```bash
# Install all dependencies
npm run install:all

# Build shared package
npm run build:shared
```

#### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Kill the process or stop the conflicting service
```

#### Issue: "Environment file not found"

**Solution:**
- Ensure `.env.dev`, `.env.uat`, or `.env.prd` exists in `services/api-gateway/`
- Check that `NODE_ENV` matches the file name
- Copy from `env.template` if needed:
  ```bash
  cd services/api-gateway
  cp env.template .env.dev
  ```

---

## Testing Your Configuration

### Step 1: Start the Server

```bash
cd services/api-gateway
npm run dev
```

### Step 2: Check Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### Step 3: Test Authentication

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+264811234567",
    "password": "TestPassword123!",
    "userType": "user"
  }'
```

### Step 4: Check Email

- Check the email inbox for `test@example.com`
- Verify the verification email was sent
- Check that the verification link includes your `CLIENT_URL`

### Step 5: Test Database

- Go to [Firebase Console](https://console.firebase.google.com/)
- Navigate to Firestore Database
- Verify that the test user was created

---

## Additional Resources

- [Environment Setup Unified Guide](./ENVIRONMENT_SETUP_UNIFIED.md) - Quick reference
- [Google Maps API Setup](./GOOGLE_MAPS_SETUP.md) - Detailed Google Maps setup
- [Firebase Migration Guide](./firebase-migration-guide.md) - Firebase setup details
- [Render Deployment Guide](../deployment/RENDER_DEPLOYMENT_GUIDE.md) - Cloud deployment

---

## Security Reminders

1. **Never commit `.env` files to version control**
2. **Use different secrets for each environment**
3. **Rotate secrets periodically in production**
4. **Restrict API keys to specific domains/IPs**
5. **Use strong, randomly generated secrets (minimum 32 characters)**
6. **Keep service account keys secure**
7. **Monitor API usage and set up billing alerts**
8. **Use environment variables in hosting platforms (not hardcoded values)**

---

## Need Help?

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review server logs for error messages
3. Verify all required variables are set
4. Test each component individually
5. Check the [Additional Resources](#additional-resources) section

