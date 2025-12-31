# Firebase Setup - Configuration Complete

## ✅ What Has Been Configured

### 1. Firebase Service Account Credentials
- **File Created**: `firebase-credentials.json`
- **Project ID**: `londa-cd054`
- **Service Account Email**: `firebase-adminsdk-fbsvc@londa-cd054.iam.gserviceaccount.com`
- **Client ID**: `115430436189396451267`
- **Key ID**: `c8e121dc979fd1ba40766d12cdc81b3853490597`

### 2. FCM Configuration
- **Sender ID**: `183357466741`
- **Web Push Certificate Key Pair**: `BEArJz5i6X4emJBl6nZwgYjupJEIVQhaWb8xY5eEQ-cmh4kzFH-9HNM1FH8go8NBgMyEHTUHal55Dq95iwS46tY`

## ⚠️ Important Notes

### Private Key Issue
The private key provided appears to be incomplete. Firebase service account private keys are typically:
- RSA private keys in PEM format
- 2000+ characters when base64 encoded
- Format: `-----BEGIN PRIVATE KEY-----\n[long base64 string]\n-----END PRIVATE KEY-----\n`

**Action Required:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `londa-cd054`
3. Go to **Project Settings** > **Service Accounts**
4. Click **"Generate new private key"**
5. Download the complete JSON file
6. Replace `firebase-credentials.json` with the downloaded file

### FCM Server Key
The **FCM Server Key** is different from the Web Push Certificate. You need to get it separately:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `londa-cd054`
3. Go to **Project Settings** > **Cloud Messaging** tab
4. Find **"Server key"** (starts with `AAAA...`)
5. Copy the entire key
6. Add to `.env` file:
   ```
   FCM_SERVER_KEY=AAAAxxxxxxx:APA91bH...
   ```

## 📝 Update .env File

Add/update these values in your `.env` file:

```env
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=londa-cd054

# FCM Configuration (get from Firebase Console > Cloud Messaging)
FCM_SERVER_KEY=your-fcm-server-key-here
```

## ✅ Verification Steps

1. **Test Firebase Connection:**
   ```bash
   python -c "from app.core.firebase import initialize_firebase; initialize_firebase(); print('✅ Firebase initialized successfully')"
   ```

2. **If you get an error about the private key:**
   - Download the complete service account JSON from Firebase Console
   - Replace `firebase-credentials.json` with the downloaded file

3. **Test FCM (after adding server key):**
   - The FCM server key is used for sending push notifications
   - It will be tested when you send your first notification

## 🔐 Security Reminders

- ✅ `firebase-credentials.json` is in `.gitignore` (won't be committed)
- ✅ Never commit service account keys to version control
- ✅ Use different keys for development and production
- ✅ Rotate keys periodically

## 📚 Next Steps

1. ✅ Download complete Firebase service account JSON (if private key is incomplete)
2. ✅ Get FCM Server Key from Firebase Console
3. ✅ Update `.env` with FCM_SERVER_KEY
4. ✅ Test Firebase connection
5. ✅ Start the API server

## 🆘 Troubleshooting

### Error: "Invalid private key"
- **Solution**: Download the complete service account JSON from Firebase Console

### Error: "FCM server key not found"
- **Solution**: Get the FCM Server Key from Firebase Console > Cloud Messaging > Server Key

### Error: "Permission denied"
- **Solution**: Ensure the service account has Firestore permissions enabled

