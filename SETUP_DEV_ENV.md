# Development Environment Setup Guide

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` with your API keys:**
   - See sections below for where to get each key

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Firebase credentials:**
   - Download service account JSON from Firebase Console
   - Place it in project root as `firebase-credentials.json`
   - Or update `FIREBASE_CREDENTIALS_PATH` in `.env`

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## Required API Keys & Configuration

### 1. Firebase Configuration

**Firebase Service Account:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (`londa-cd054`)
3. Go to **Project Settings** > **Service Accounts**
4. Click **Generate New Private Key**
5. Save the JSON file as `firebase-credentials.json` in project root
6. Update `.env`: `FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json`

**FCM Server Key:**
1. In Firebase Console, go to **Project Settings** > **Cloud Messaging**
2. Copy the **Server Key** (starts with `AAAA...`)
3. Update `.env`: `FCM_SERVER_KEY=AAAAxxxxxxx:APA91bH...`

**Firebase Project ID:**
- Already set: `FIREBASE_PROJECT_ID=londa-cd054`

---

### 2. Google Maps Platform API

**Get API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Go to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **API Key**
5. Copy the API key

**Enable Required APIs:**
- Maps JavaScript API
- Geocoding API
- Directions API
- Distance Matrix API
- Places API (optional, for autocomplete)

**Update `.env`:**
```
GOOGLE_MAPS_API_KEY=your-api-key-here
```

**Security (Recommended):**
- Restrict API key to specific APIs
- Add IP restrictions for production
- Set up billing alerts

---

### 3. SMTP Email Configuration

**For Gmail:**
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google Account Settings](https://myaccount.google.com/)
3. Navigate to **Security** > **2-Step Verification** > **App Passwords**
4. Generate an App Password for "Mail"
5. Use this password (not your regular Gmail password)

**Update `.env`:**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password-here
SMTP_FROM=noreply@londarides.com
```

**Email Activation Secret:**
- Generate a random base64 string for email verification
- Can use: `openssl rand -base64 32`
- Update `.env`: `EMAIL_ACTIVATION_SECRET=your-generated-secret`

---

### 4. Nylas API (Optional)

**For Calendar Integration:**
1. Sign up at [Nylas](https://www.nylas.com/)
2. Get your API key from the dashboard
3. Update `.env`: `NYLAS_API_KEY=your-nylas-key`

**Note:** This is optional and only needed if implementing calendar features.

---

## Environment Variables Reference

### Required for Development:
- ✅ `FIREBASE_CREDENTIALS_PATH` - Path to Firebase service account JSON
- ✅ `FCM_SERVER_KEY` - Firebase Cloud Messaging server key
- ✅ `GOOGLE_MAPS_API_KEY` - Google Maps Platform API key
- ✅ `SMTP_USER` - Email account for sending OTPs
- ✅ `SMTP_PASS` - Email app password
- ✅ `SECRET_KEY` - Secret key for JWT tokens (change in production)

### Optional:
- `NYLAS_API_KEY` - For calendar integration
- `EMAIL_ACTIVATION_SECRET` - For email verification

### Already Configured:
- `FIREBASE_PROJECT_ID` - Set to `londa-cd054`
- `SMTP_HOST` - Set to Gmail SMTP
- `SMTP_PORT` - Set to 587
- Business constants (subscription amounts, ride fare)

---

## Verification

After setting up, verify your configuration:

1. **Check Firebase:**
   ```bash
   python -c "from app.core.firebase import initialize_firebase; initialize_firebase(); print('Firebase OK')"
   ```

2. **Check Google Maps:**
   ```bash
   python -c "from app.core.config import settings; print(f'Maps API Key: {settings.GOOGLE_MAPS_API_KEY[:20]}...')"
   ```

3. **Start Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Test Health Endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## Troubleshooting

### Firebase Issues:
- **Error: "Firebase not initialized"**
  - Check `FIREBASE_CREDENTIALS_PATH` points to valid JSON file
  - Verify file has correct permissions

### Google Maps Issues:
- **Error: "API key not valid"**
  - Verify API key is correct
  - Check that required APIs are enabled
  - Verify billing is enabled on Google Cloud project

### SMTP Issues:
- **Error: "Authentication failed"**
  - Use App Password, not regular password
  - Verify 2FA is enabled
  - Check SMTP settings are correct

### FCM Issues:
- **Error: "Invalid FCM server key"**
  - Verify key from Firebase Console > Cloud Messaging
  - Check key format (should start with `AAAA`)

---

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control
- Use different keys for development and production
- Rotate API keys periodically
- Restrict API keys to specific IPs/domains in production
- Use strong `SECRET_KEY` in production

---

## Next Steps

1. ✅ Set up all API keys
2. ✅ Verify Firebase connection
3. ✅ Test email sending
4. ✅ Test Google Maps integration
5. ✅ Run the API server
6. ✅ Test endpoints with Postman collection

