# 🧪 Newman Postman Testing Guide

## Overview

This guide explains how to use **Newman** (Postman CLI) to automatically test the Londa Rides APIs from the command line. Newman allows you to run Postman collections programmatically, making it perfect for CI/CD pipelines and automated testing.

## 📋 Prerequisites

1. **Node.js** installed (v14 or higher)
2. **Newman** installed (automatically installed with `npm install`)
3. **API Gateway** running on `http://localhost:8000`
4. **Main Server** running on port 3001 (or configured via `MAIN_SERVER_URL`)

## 🚀 Quick Start

### 1. Install Dependencies

From the root `backend/` directory:

```bash
npm install
```

This will install Newman as a dev dependency.

### 2. Ensure Services Are Running

Before running tests, make sure your services are running:

```bash
# Option 1: Run all services
npm run dev:all

# Option 2: Run only required services
npm run dev:main    # Main server (port 3001)
npm run dev:gateway # API Gateway (port 8000)
```

### 3. Run Tests

```bash
# Test User Authentication APIs only
npm run test:postman:auth

# Test with HTML report
npm run test:postman:auth:report

# Test full Postman collection
npm run test:postman
```

## 📚 Available Test Commands

### User Authentication Tests

```bash
npm run test:postman:auth
```

**What it does:**
- Runs only the "2. User Authentication" folder from the Postman collection
- Tests 6 authentication endpoints:
  1. Register User (Send OTP)
  2. Verify OTP (Login)
  3. Request Email OTP
  4. Verify Email OTP
  5. Create User Account
  6. Get Logged In User Data

**Output:**
- Colored CLI output with test results
- Summary of passed/failed tests
- Automatic variable extraction (auth_token, session_info, user_id)

### Generate HTML Report

```bash
npm run test:postman:auth:report
```

**What it does:**
- Runs the same tests as above
- Generates an HTML report at `test-results/postman-auth-report.html`
- Includes detailed test results, request/response data, and timing information

### Full Collection Tests

```bash
npm run test:postman
```

**What it does:**
- Runs the entire Postman collection
- Tests all API endpoints across all folders
- Useful for comprehensive integration testing

## 🔧 Configuration

### Collection Variables

The test scripts automatically configure the following collection variables:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `base_url` | `http://localhost:8000` | API Gateway base URL |
| `api_base` | `http://localhost:8000/api/v1` | API base path |
| `auth_token` | (empty) | JWT token (auto-populated after login) |
| `user_id` | (empty) | User ID (auto-populated after login) |
| `session_info` | (empty) | Session info for OTP verification |

### Customizing Base URL

To test against a different server, edit the collection variables in:
- `test-postman-auth.js` (line ~30)
- `test-postman.js` (line ~30)

Or set environment variables:

```bash
# Windows PowerShell
$env:API_BASE_URL="http://your-server:8000"
npm run test:postman:auth

# Linux/Mac
export API_BASE_URL="http://your-server:8000"
npm run test:postman:auth
```

## 📊 Understanding Test Results

### Successful Test Run

```
🚀 Starting Newman Test Run for User Authentication APIs

📋 Collection: Londa_Rides_Local_Testing.postman_collection.json
📁 Folder: 2. User Authentication
🌐 Base URL: http://localhost:8000

============================================================
📊 Test Summary
============================================================

✅ Total Requests: 6
   ✓ Passed: 6
   ✗ Failed: 0

🧪 Total Tests: 24
   ✓ Passed: 24
   ✗ Failed: 0

============================================================
✅ All tests passed!
```

### Failed Test Run

```
============================================================
📊 Test Summary
============================================================

✅ Total Requests: 6
   ✓ Passed: 5
   ✗ Failed: 1

🧪 Total Tests: 24
   ✓ Passed: 22
   ✗ Failed: 2

❌ Failed Assertions:

   Request: Verify OTP (Login)
   Assertion: Response is JSON
   Error: Expected response to be JSON

============================================================
❌ Tests completed with failures
```

## 🧪 Test Scripts in Postman Collection

Each endpoint in the Postman collection includes test scripts that verify:

1. **Response Format**
   - Response is JSON (not HTML)
   - Content-Type header is `application/json`
   - Response body doesn't contain HTML tags

2. **Success Cases**
   - Response has `success: true`
   - Required fields are present
   - Status codes are correct (200, 201)

3. **Error Cases**
   - Error responses are also JSON format
   - Error messages are present
   - Status codes match error type

4. **Variable Extraction**
   - `auth_token` extracted from login responses
   - `user_id` extracted from user data
   - `session_info` extracted from registration

## 📁 File Structure

```
backend/
├── test-postman-auth.js          # User Authentication test runner
├── test-postman.js               # Full collection test runner
├── Londa_Rides_Local_Testing.postman_collection.json
└── test-results/                 # Generated HTML reports (created automatically)
    └── postman-auth-report.html
```

## 🔍 Troubleshooting

### Issue: "Collection file not found"

**Solution:**
- Ensure you're running commands from the `backend/` directory
- Verify `Londa_Rides_Local_Testing.postman_collection.json` exists in the root

### Issue: "503 Service Unavailable" Errors

**Symptoms:**
- All API requests return `503 Service Unavailable`
- Tests show "Error response is JSON" (tests pass but APIs fail)
- Response body contains: `"Service unavailable"`

**Cause:**
The API Gateway is running but cannot connect to the main server on port 3001.

**Solution:**
1. **Start the main server** (required):
   ```bash
   # Option 1: Start all services (recommended)
   npm run dev:all
   
   # Option 2: Start main server only
   cd server
   npm run dev:3001
   ```

2. **Verify main server is running:**
   ```bash
   # Check if port 3001 is responding
   curl http://localhost:3001/test
   
   # Or check if port is in use
   netstat -ano | findstr :3001  # Windows
   lsof -i :3001                 # Linux/Mac
   ```

3. **Verify API Gateway is running:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Run tests again:**
   ```bash
   npm run test:postman:auth
   ```

**Note:** The test script now automatically checks if the main server is running before executing tests. If it's not running, you'll see a clear error message with instructions.

### Issue: "Connection refused" or "ECONNREFUSED"

**Solution:**
1. Check if API Gateway is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check if Main Server is running:
   ```bash
   # Check if port 3001 is in use
   netstat -ano | findstr :3001  # Windows
   lsof -i :3001                 # Linux/Mac
   ```

3. Start required services:
   ```bash
   npm run dev:all
   ```

### Issue: "Tests failing with 401 Unauthorized"

**Solution:**
- The test flow requires sequential execution:
  1. First: Register User (Send OTP) → saves `session_info`
  2. Second: Verify OTP (Login) → saves `auth_token`
  3. Then: Other authenticated endpoints can run

- Ensure tests run in order (Newman runs them sequentially by default)

### Issue: "OTP verification failing"

**Solution:**
- Check if OTP service is configured correctly
- For development, OTP might be a fixed value (e.g., "123456")
- Check server logs for OTP generation errors

### Issue: "HTML report not generated"

**Solution:**
- Ensure the `test-results/` directory exists or can be created
- Check file permissions
- Verify the path in the command is correct

## 🎯 Best Practices

### 1. Run Tests in Order

Newman runs requests sequentially, which is important for authentication flows:
- Registration → OTP Verification → Authenticated Requests

### 2. Use Environment Variables

For different environments (dev, staging, prod), use environment variables:

```javascript
// In test script
const baseUrl = process.env.API_BASE_URL || 'http://localhost:8000';
```

### 3. Check Test Results Regularly

- Review HTML reports for detailed request/response data
- Monitor test execution time
- Track flaky tests

### 4. Integrate with CI/CD

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run Postman Tests
  run: |
    npm install
    npm run dev:all &
    sleep 10  # Wait for services to start
    npm run test:postman:auth
```

## 📝 Adding New Tests

### Add Test Scripts to Postman Collection

1. Open Postman collection in Postman app
2. Select the request
3. Go to "Tests" tab
4. Add test scripts:

```javascript
// Verify response is JSON
pm.test("Response is JSON", function () {
    pm.response.to.be.json;
    pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
});

// Verify success response
if (pm.response.code === 200) {
    pm.test("Request successful", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('success');
        pm.expect(jsonData.success).to.be.true;
    });
}
```

5. Save the collection
6. Run tests with Newman

### Create New Test Script

To test a specific folder, create a new script similar to `test-postman-auth.js`:

```javascript
const newmanOptions = {
  collection: collectionPath,
  folder: 'Your Folder Name',  // Change this
  // ... rest of configuration
};
```

Then add to `package.json`:

```json
{
  "scripts": {
    "test:postman:your-folder": "node test-postman-your-folder.js"
  }
}
```

## 🔗 Related Documentation

- [Postman Collection README](../api/POSTMAN_COLLECTION_README.md)
- [Testing README](./README.md)
- [API Documentation](../api/API_DOCUMENTATION.md)
- [Quick Start Guide](../setup/QUICK_START.md)

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review server logs for errors
3. Verify all services are running
4. Check Postman collection for test script errors

---

**Last Updated:** 2024
**Newman Version:** 6.1.0+

