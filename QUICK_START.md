# 🚀 Quick Start - Development Environment

## Step 1: Create .env File

```bash
# Copy the template to .env
cp env.dev.template .env
```

Or on Windows PowerShell:
```powershell
Copy-Item env.dev.template .env
```

## Step 2: Update API Keys in .env

The `.env` file is already populated with development values. You only need to update:

### Required Updates:

1. **FCM Server Key** (if not already set):
   ```
   FCM_SERVER_KEY=your-fcm-server-key-here
   ```
   Get from: Firebase Console > Project Settings > Cloud Messaging > Server Key

2. **Firebase Credentials** (if not already set):
   - Download service account JSON from Firebase Console
   - Place as `firebase-credentials.json` in project root
   - Or update path: `FIREBASE_CREDENTIALS_PATH=./path/to/your/file.json`

### Already Configured (from your config):
- ✅ Google Maps API Key: `AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs`
- ✅ SMTP Settings: Gmail configured
- ✅ Email Activation Secret: Set
- ✅ Nylas API Key: Set
- ✅ Business Constants: All set

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the run script:
```bash
python run.py
```

## Step 5: Verify

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **API Test:**
   ```bash
   curl http://localhost:8000/test
   ```

3. **OpenAPI Docs:**
   - Visit: http://localhost:8000/docs

## 📋 All Environment Variables

The `.env` file includes:

### ✅ Already Set (from config.py):
- `GOOGLE_MAPS_API_KEY` - Google Maps API
- `SMTP_USER` - Gmail account
- `SMTP_PASS` - Gmail app password
- `SMTP_FROM` - Email sender
- `EMAIL_ACTIVATION_SECRET` - Email verification
- `NYLAS_API_KEY` - Nylas calendar API
- `FIREBASE_PROJECT_ID` - Firebase project
- Business constants (subscription amounts, ride fare)

### ⚠️ Need to Set:
- `FCM_SERVER_KEY` - Get from Firebase Console
- `FIREBASE_CREDENTIALS_PATH` - Path to service account JSON

### 🔧 Optional to Change:
- `SECRET_KEY` - Change for production
- `DEBUG` - Set to `False` for production
- `BACKEND_CORS_ORIGINS` - Add your frontend URLs

## 🔐 Quick API Usage Examples

### User Registration & Authentication

```bash
# 1. Send OTP
curl -X POST http://localhost:8000/api/v1/registration \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530"}'

# 2. Verify OTP & Get Token
curl -X POST http://localhost:8000/api/v1/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+264813442530", "otp": "123456", "sessionInfo": "session_xxx"}'

# 3. Create Account (with token)
curl -X POST http://localhost:8000/api/v1/create-account \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ID_TOKEN" \
  -d '{"phone_number": "+264813442530", "name": "John Doe", "userType": "student"}'
```

### Driver Subscription (No driver_id in body!)

```bash
# Create subscription - driver_id extracted from token
curl -X POST http://localhost:8000/api/v1/driver/subscription \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_DRIVER_TOKEN" \
  -d '{"payment_method": "cash"}'

# Process payment - driver_id extracted from token
curl -X POST http://localhost:8000/api/v1/driver/subscription/payment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_DRIVER_TOKEN" \
  -d '{"payment_method": "cash", "amount": 150.00}'
```

**⚠️ Important:** 
- `user_id` and `driver_id` are automatically extracted from authentication tokens
- Do NOT include them in request bodies
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference

## 📚 Full Documentation

See `SETUP_DEV_ENV.md` for detailed setup instructions.

## ✅ Verification Checklist

- [ ] `.env` file created from template
- [ ] FCM Server Key added
- [ ] Firebase credentials file downloaded and placed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] API docs accessible at `/docs`

