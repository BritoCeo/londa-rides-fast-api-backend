# Londa Rides Backend - Setup and Run Guide

## 📋 Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Firebase project with Firestore enabled
- Firebase service account key file

## 🚀 Quick Start

### Step 1: Install Dependencies

#### 1.1 Install Shared Package Dependencies
```bash
cd shared
npm install
npm run build
```

#### 1.2 Install Unified API Gateway Dependencies

**Unified API Gateway (All-in-One):**
```bash
cd ../services/api-gateway
npm install
```

> **Note:** The unified API gateway consolidates all functionality into a single service. Individual microservices (user-service, driver-service, auth-service, ride-service) are no longer needed for the unified architecture.

### Step 2: Environment Configuration

The unified API gateway uses environment-specific configuration files. The gateway has `.env.dev`, `.env.uat`, and `.env.prd` files for different environments.

**Important:** The unified API gateway runs on port **8000** and handles all API requests directly. No internal microservices are required.

#### Environment Files Structure

The unified API gateway has three environment files:
- `.env.dev` - Development environment
- `.env.uat` - User Acceptance Testing environment
- `.env.prd` - Production environment

The system automatically loads the appropriate file based on `NODE_ENV` environment variable.

#### Quick Setup

1. **Copy the environment template:**
   ```bash
   cd services/api-gateway
   cp env.template .env.dev
   ```

2. **Fill in the values** for your development environment (see `ENVIRONMENT_SETUP.md` for details)

3. **For other environments:**
   ```bash
   cp env.template .env.uat
   cp env.template .env.prd
   ```

For detailed environment configuration, see [ENVIRONMENT_SETUP.md](../../services/api-gateway/ENVIRONMENT_SETUP.md).

**Note:** In production, ensure `.env.prd` files are properly secured and not committed to version control.

### Step 3: Build Shared Package

The shared package must be built before running any service:

```bash
cd shared
npm run build
```

This creates the `dist/` directory with compiled TypeScript.

### Step 4: Run the Unified API Gateway

#### Option A: Run Unified API Gateway (Recommended)

**Single Command:**
```bash
# From root directory
npm run dev:unified

# Or from api-gateway directory
cd services/api-gateway
npm run dev
```

#### Option B: Run with Environment-Specific Configuration

```bash
# Development (default)
cd services/api-gateway
npm run dev:dev

# UAT
npm run dev:uat

# Production
npm run dev:prd
```

**Note:** The unified API gateway runs on port 8000 and handles all API requests directly. No additional services are required.

### Step 5: Verify the Unified API is Running

Check the health endpoint:

- **Unified API Gateway**: http://localhost:8000/health
- **Test Endpoint**: http://localhost:8000/test
- **API Base**: http://localhost:8000/api/v1

## 📝 Service Ports

**Architecture:** Unified monolithic API on single port

| Service | Port | Access | Notes |
|---------|------|--------|-------|
| **Unified API Gateway** | **8000** | **External** | **All API requests handled directly** |

**Important:** The unified API gateway consolidates all functionality into a single service running on port 8000. All API endpoints are handled directly by the gateway without proxying to internal microservices.

## 🔧 Development Commands

### Build Commands

**Shared Package:**
```bash
cd shared
npm run build
```

**Unified API Gateway:**
```bash
cd services/api-gateway
npm run build
```

### Run Commands

**Development (with hot reload):**
```bash
npm run dev          # Default: dev environment
npm run dev:dev      # Explicitly dev environment
npm run dev:uat      # UAT environment
npm run dev:prd      # Production environment
```

**Production:**
```bash
npm run build
npm start            # Uses NODE_ENV from environment
npm start:dev        # Explicitly dev environment
npm start:uat        # UAT environment
npm start:prd        # Production environment
```

## 🐛 Troubleshooting

### Issue: "Cannot find module '@londa-rides/shared'"

**Solution:**
1. Make sure you've built the shared package:
   ```bash
   cd shared
   npm run build
   ```

2. Verify the shared package is properly linked in service `package.json`:
   ```json
   "@londa-rides/shared": "file:../../shared"
   ```

### Issue: "Firestore initialization failed"

**Solution:**
1. Check that `FIREBASE_SERVICE_ACCOUNT_KEY` path is correct
2. Verify the service account key file exists
3. Ensure Firebase project ID is correct

### Issue: "Port already in use"

**Solution:**
1. Check which process is using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

2. Kill the process or change the port in `.env`

### Issue: "TypeScript compilation errors"

**Solution:**
1. Make sure all dependencies are installed
2. Rebuild the shared package
3. Check TypeScript version compatibility

## 📦 Production Deployment

### Build Unified API Gateway

```bash
# Build shared package
cd shared
npm run build

# Build unified API gateway
cd ../services/api-gateway
npm run build
```

### Run in Production

```bash
# Option 1: Set NODE_ENV and run
export NODE_ENV=prd  # or 'uat' for UAT environment

# Run unified API gateway
cd services/api-gateway
npm start:prd

# Option 2: Use root script (recommended)
npm run dev:unified  # For development
# Or set NODE_ENV=prd before running
```

## 🧪 Testing

### Run Tests

```bash
# Shared package tests
cd shared
npm test

# Service-specific tests (when implemented)
cd services/user-service
npm test
```

## 📚 Next Steps

1. **Configure Firebase**: Set up your Firestore database
2. **Set Environment Variables**: Update `.env.dev` file with your actual values (see `services/api-gateway/ENVIRONMENT_SETUP.md`)
3. **Run Unified API**: Start the unified API gateway in development mode
4. **Test API**: Use the unified API at http://localhost:8000/api/v1
5. **Check Documentation**: See `docs/api/API_DOCUMENTATION.md` for API endpoints

## 🔗 Useful Links

- API Documentation: `docs/api/API_DOCUMENTATION.md`
- Architecture Docs: `docs/architecture/ARCHITECTURE.md`
- Environment Configuration: `docs/setup/ENVIRONMENT_CONFIG.md`
- Cleanup Guide: `docs/guides/CLEANUP_GUIDE.md`

---

**Need Help?** Check the troubleshooting section or review the architecture documentation.

