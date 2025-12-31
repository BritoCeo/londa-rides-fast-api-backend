# 🚗 Londa Rides API - FastAPI Backend

FastAPI backend application for **Londa Rides CC**, a ride-sharing platform designed to provide safe and affordable transportation options to students, working-class individuals, and parents in Namibia.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Setup](#-setup)
- [Firebase Configuration](#-firebase-configuration)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [Development](#-development)
- [Additional Resources](#-additional-resources)

---

## ✨ Features

- 🚀 **FastAPI** with async/await support for high performance
- 🔐 **Firebase Authentication** - OTP-based phone/email verification
- 💾 **Firestore Database** - NoSQL cloud database for data persistence
- 📍 **Google Maps Integration** - Geocoding, distance calculation, and route optimization
- 🔔 **Firebase Cloud Messaging (FCM)** - Push notifications for drivers and riders
- 📝 **Automatic API Documentation** - Swagger/OpenAPI with interactive docs
- ✅ **Input Validation** - Pydantic models for request/response validation
- 🎯 **Clean Architecture** - Layered design (Routes → Services → Repositories)
- 🛡️ **Comprehensive Error Handling** - Centralized exception handling
- ⚙️ **Environment-based Configuration** - Secure configuration management
- 🔒 **JWT Authentication** - Firebase ID token verification
- 📊 **Analytics & Reporting** - User and driver analytics endpoints

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python 3.9+)
- **Database:** Google Cloud Firestore
- **Authentication:** Firebase Authentication
- **Push Notifications:** Firebase Cloud Messaging (FCM)
- **Maps & Location:** Google Maps Platform API
- **Validation:** Pydantic
- **Logging:** Structured JSON logging
- **API Documentation:** OpenAPI/Swagger

---

## 📁 Project Structure

```
londa-apis/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── api.py             # API router aggregation
│   │       └── endpoints/
│   │           └── health.py      # Health check endpoints
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   ├── exceptions.py          # Exception handlers
│   │   ├── firebase.py            # Firebase initialization
│   │   ├── security.py            # Authentication & authorization
│   │   ├── responses.py           # Response utilities
│   │   ├── serializers.py         # Firestore serialization
│   │   └── logging.py            # Logging configuration
│   ├── users/                     # User authentication & profiles
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   └── schemas.py
│   ├── drivers/                    # Driver authentication & profiles
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   └── schemas.py
│   ├── rides/                      # Ride management
│   │   ├── router.py              # User ride endpoints
│   │   ├── driver_router.py       # Driver ride endpoints
│   │   ├── service.py
│   │   ├── driver_service.py
│   │   ├── repository.py
│   │   └── schemas.py
│   ├── subscriptions/
│   │   ├── driver/                 # Driver subscription management
│   │   └── parent/                 # Parent subscription management
│   ├── payments/                   # Payment processing
│   ├── analytics/                  # Analytics & reporting
│   ├── maps/                       # Google Maps integration
│   └── notifications/              # FCM push notifications
├── postmancollection/              # Postman API collection
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in git)
├── firebase-credentials.json       # Firebase service account (not in git)
├── API_DOCUMENTATION.md           # Complete API documentation
├── FIRESTORE_INDEXES.md           # Required Firestore indexes
├── AUTHENTICATION_FLOW_EXPLAINED.md
├── QUICK_START.md
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Firebase project with Firestore enabled
- Google Maps Platform API key
- Firebase service account credentials

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd londa-apis
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy template (if exists) or create .env file
   # See Environment Variables section below
   ```

5. **Configure Firebase:**
   - Download Firebase service account JSON from Firebase Console
   - Place as `firebase-credentials.json` in project root
   - Or set `FIREBASE_CREDENTIALS_PATH` in `.env`

6. **Create Firestore indexes:**
   - See `FIRESTORE_INDEXES.md` for required composite indexes
   - Create indexes via Firebase Console or CLI

7. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Verify installation:**
   - Health check: http://localhost:8000/api/v1/health
   - API docs: http://localhost:8000/docs

For detailed setup instructions, see [QUICK_START.md](QUICK_START.md).

---

## 🔥 Firebase Configuration

### Required Setup

1. **Firebase Project:**
   - Create a Firebase project at https://console.firebase.google.com
   - Enable Firestore Database
   - Enable Firebase Authentication (Phone & Email providers)

2. **Service Account:**
   - Go to Project Settings > Service Accounts
   - Generate new private key
   - Download JSON file
   - Place in project root as `firebase-credentials.json`

3. **Firestore Indexes:**
   - Create composite indexes as documented in `FIRESTORE_INDEXES.md`
   - Required for queries with multiple filters/ordering

4. **Firebase Cloud Messaging:**
   - Enable FCM in Firebase Console
   - Service account credentials are used automatically

### Firebase Collections

- `users` - User profiles
- `drivers` - Driver profiles
- `rides` - Ride requests and status
- `driver_subscriptions` - Driver subscription records
- `parent_subscriptions` - Parent subscription records
- `subscription_payments` - Driver subscription payments
- `payments` - Ride payments
- `otp_sessions` - OTP verification sessions

---

## 📚 API Documentation

### Interactive Documentation

Once the server is running:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Complete API Documentation

See **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** for:
- Complete endpoint reference
- Request/response examples
- Authentication flow
- Error codes
- Field descriptions

### Postman Collection

Import `postmancollection/Londa_Rides_API_Collection_Complete.postman_collection.json` into Postman for:
- Pre-configured requests
- Auto-saved authentication tokens
- Environment variables
- Test scripts

---

## 🔐 Authentication

### Authentication Flow

1. **User/Driver Registration:**
   ```
   POST /api/v1/registration
   POST /api/v1/driver/send-otp
   ```
   - Sends OTP to phone number
   - Returns `sessionInfo` for verification

2. **OTP Verification:**
   ```
   POST /api/v1/verify-otp
   POST /api/v1/driver/verify-otp
   ```
   - Verifies OTP code
   - Returns `accessToken` (Firebase custom token)

3. **Account Creation:**
   ```
   POST /api/v1/create-account
   POST /api/v1/driver/create-account
   ```
   - Completes user/driver profile
   - Requires `Authorization: Bearer <token>` header

4. **Using the Token:**
   - Exchange custom token for ID token using Firebase SDK (client-side)
   - Include ID token in requests: `Authorization: Bearer <id_token>`

For detailed authentication flow, see [AUTHENTICATION_FLOW_EXPLAINED.md](AUTHENTICATION_FLOW_EXPLAINED.md).

---

## 🛣️ API Endpoints

### Base URL
- **Development:** `http://localhost:8000/api/v1`
- **Production:** `https://api.londarides.com/api/v1`

### Endpoint Categories

#### 1. User Authentication & Profile
- `POST /registration` - Send OTP
- `POST /verify-otp` - Verify OTP and login
- `POST /create-account` - Create user account
- `GET /me` - Get current user profile
- `PUT /update-profile` - Update user profile
- `POST /update-location` - Update user location

#### 2. Ride Management (User)
- `POST /request-ride` - Request a ride
- `GET /nearby-drivers` - Find nearby drivers
- `POST /cancel-ride` - Cancel a ride
- `PUT /rate-ride` - Rate a completed ride
- `GET /ride-status/{ride_id}` - Get ride status
- `GET /get-rides` - Get user ride history

#### 3. Driver Authentication & Profile
- `POST /driver/send-otp` - Send driver OTP
- `POST /driver/verify-otp` - Verify driver OTP
- `POST /driver/login` - Driver login
- `POST /driver/create-account` - Create driver account
- `GET /driver/me` - Get driver profile
- `PUT /driver/update-status` - Update driver status
- `POST /driver/update-location` - Update driver location

#### 4. Driver Ride Management
- `GET /driver/available-rides` - Get pending ride requests
- `POST /driver/accept-ride` - Accept a ride
- `POST /driver/decline-ride` - Decline a ride
- `POST /driver/start-ride` - Start ride (pickup)
- `POST /driver/complete-ride` - Complete ride (dropoff)
- `GET /driver/get-rides` - Get driver ride history

#### 5. Subscriptions
- **Driver:** Create, get status, update, process payment, history
- **Parent:** Subscribe, get status, update, cancel, usage stats, children profiles

#### 6. Payments
- `POST /payment/calculate-fare` - Calculate ride fare
- `POST /payment/process` - Process ride payment
- `GET /payment/history` - Get payment history

#### 7. Analytics
- User ride analytics, performance metrics
- Driver earnings, ride analytics, performance metrics

#### 8. Health Check
- `GET /health` - Health check
- `GET /test` - API test endpoint

**See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete endpoint reference.**

---

## ⚙️ Environment Variables

Create a `.env` file in the project root with the following variables:

### Required

```env
# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=londa-cd054

# Google Maps
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Optional

```env
# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256

# SMTP (for email OTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=noreply@londarides.com

# Business Constants
DRIVER_SUBSCRIPTION_AMOUNT=150.00
PARENT_SUBSCRIPTION_AMOUNT=1000.00
DEFAULT_RIDE_FARE=13.00

# Logging
LOG_LEVEL=INFO
```

**Note:** Never commit `.env` or `firebase-credentials.json` to version control.

---

## 🏃 Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Custom Timeout

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 2
```

---

## 💻 Development

### Code Structure

The project follows a **layered architecture**:

- **Routes** (`router.py`) - HTTP endpoints, request/response handling
- **Services** (`service.py`) - Business logic, validation
- **Repositories** (`repository.py`) - Database operations, Firestore queries

### Adding New Endpoints

1. Create schema in `schemas.py` (Pydantic models)
2. Add repository methods in `repository.py`
3. Add service methods in `service.py`
4. Add route handlers in `router.py`
5. Include router in `app/api/v1/api.py`

### Code Formatting

```bash
black app/
```

### Type Checking

```bash
mypy app/
```

### Running Tests

```bash
pytest
```

---

## 📖 Additional Resources

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[FIRESTORE_INDEXES.md](FIRESTORE_INDEXES.md)** - Required database indexes
- **[AUTHENTICATION_FLOW_EXPLAINED.md](AUTHENTICATION_FLOW_EXPLAINED.md)** - Auth flow details
- **[QUICK_START.md](QUICK_START.md)** - Quick setup guide

---

## 🏗️ Architecture Principles

- **SOLID Principles** - Single responsibility, dependency injection
- **RESTful Design** - Resource-based URLs, proper HTTP methods
- **Event-Driven** - No WebSockets; uses FCM for real-time notifications
- **Database as Source of Truth** - Firestore is the single source of truth
- **Horizontal Scaling** - No in-memory state; stateless design
- **Security First** - Token verification, input validation, CORS

---

## 📝 License

[Your License Here]

---

## 🤝 Contributing

[Your Contributing Guidelines Here]

---

## 📞 Support

For issues or questions:
- Check the [API Documentation](API_DOCUMENTATION.md)
- Review [Firestore Indexes](FIRESTORE_INDEXES.md)
- See [Authentication Flow](AUTHENTICATION_FLOW_EXPLAINED.md)

---

**Version:** 1.0.0  
**Last Updated:** December 31, 2024  
**Maintained by:** Londa Rides Development Team
