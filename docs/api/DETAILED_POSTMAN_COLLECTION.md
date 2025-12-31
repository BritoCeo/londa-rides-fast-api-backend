# 📋 Detailed Postman Collection Guide

## Overview

The **Londa Rides Detailed API Collection** is a comprehensive Postman collection with enhanced test scripts, pre-request scripts, and detailed documentation for all API endpoints.

## 📁 Collection Files

### 1. **Londa_Rides_Detailed_API_Collection.postman_collection.json**
   - **Enhanced version** with comprehensive test scripts
   - Pre-request scripts for dynamic data generation
   - Detailed documentation for each endpoint
   - Performance validation
   - Enhanced error handling

### 2. **Londa_Rides_Local_Testing.postman_collection.json**
   - **Original collection** (still available)
   - Basic test scripts
   - Standard documentation

## 🎯 Key Features

### ✅ Comprehensive Test Scripts

Every endpoint includes:

1. **Response Validation**
   - Verifies response is JSON (not HTML)
   - Checks Content-Type header
   - Validates response structure

2. **Status Code Verification**
   - Success cases (200, 201)
   - Error cases (400, 401, 404, 500)
   - Proper error response format

3. **Data Validation**
   - Required fields presence
   - Data type checking
   - Business logic validation

4. **Performance Checks**
   - Response time validation (< 10 seconds)
   - Performance monitoring

5. **Variable Management**
   - Automatic token extraction
   - ID saving (user_id, driver_id, ride_id)
   - Session info management

### 🔄 Pre-request Scripts

Automatically included for:
- **Registration endpoints**: Generates unique test phone numbers
- **Dynamic data**: Timestamp-based test data
- **Variable initialization**: Sets up required variables

### 📚 Enhanced Documentation

Each endpoint includes:
- **Description**: What the endpoint does
- **Request examples**: Sample request bodies
- **Response examples**: Success and error responses
- **Authentication**: Whether auth is required
- **Notes**: Important information and tips

## 🚀 Usage

### Import Collection

1. Open Postman
2. Click **Import**
3. Select `Londa_Rides_Detailed_API_Collection.postman_collection.json`
4. Collection will be imported with all enhancements

### Run Tests

#### Option 1: Using Newman (CLI)

```bash
# Test User Authentication APIs
npm run test:postman:auth

# Test with HTML report
npm run test:postman:auth:report

# Test full collection
npm run test:postman
```

#### Option 2: Using Postman UI

1. Select a folder or request
2. Click **Run** button
3. View test results in the **Test Results** tab

### Collection Structure

```
Londa Rides - Detailed API Testing Collection
├── 1. Health & Status (2 requests)
│   ├── Health Check
│   └── API Test
├── 2. User Authentication (6 requests)
│   ├── Register User (Send OTP)
│   ├── Verify OTP (Login)
│   ├── Request Email OTP
│   ├── Verify Email OTP
│   ├── Create User Account
│   └── Get Logged In User Data
├── 3. User Ride Management (6 requests)
├── 4. Driver Authentication (5 requests)
├── 5. Driver Ride Management (8 requests)
├── 6. Driver Subscription (6 requests)
├── 7. Parent Subscription (7 requests)
├── 8. Payment Management (4 requests)
├── 9. Profile & Settings (2 requests)
└── 10. Analytics & Reports (5 requests)
```

## 🔧 Test Script Examples

### Standard Test Script

Every endpoint includes:

```javascript
// Response Validation
pm.test("Response is JSON", function () {
    pm.response.to.be.json;
    pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
});

pm.test("Response is not HTML", function () {
    var body = pm.response.text();
    pm.expect(body).to.not.include('<!DOCTYPE html>');
    pm.expect(body).to.not.include('<html>');
});

// Response Structure
pm.test("Response has standard format", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success');
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData).to.have.property('timestamp');
});

// Performance
pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(10000);
});
```

### Enhanced Test Script (Authentication)

```javascript
// Success Case
if (pm.response.code === 200 || pm.response.code === 201) {
    pm.test("Login successful", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData.success).to.be.true;
    });

    // Auto-save token
    pm.test("Access token is present", function () {
        var jsonData = pm.response.json();
        if (jsonData.accessToken) {
            pm.collectionVariables.set("auth_token", jsonData.accessToken);
            console.log("✅ Auth token saved");
        }
    });
}
```

### Pre-request Script Example

```javascript
// Generate unique phone number for testing
var timestamp = Date.now();
var lastDigits = timestamp.toString().slice(-4);
pm.collectionVariables.set("test_phone", "+26481" + lastDigits);
console.log("📱 Using test phone: " + pm.collectionVariables.get("test_phone"));
```

## 📊 Collection Variables

| Variable | Description | Auto-populated |
|----------|-------------|----------------|
| `base_url` | API Gateway URL | No |
| `api_base` | API base path | No |
| `auth_token` | JWT token | Yes (after login) |
| `user_id` | User ID | Yes (after login) |
| `driver_id` | Driver ID | Yes (after driver login) |
| `ride_id` | Ride ID | Yes (after ride request) |
| `session_info` | OTP session info | Yes (after registration) |
| `test_phone` | Test phone number | Yes (pre-request) |
| `test_email` | Test email | No |

## 🔄 Regenerating the Collection

If you need to regenerate the detailed collection:

```bash
node generate-detailed-postman-collection.js
```

This will:
- Read the original collection
- Enhance all requests with detailed test scripts
- Add pre-request scripts where needed
- Improve documentation
- Generate the detailed collection

## 📝 Best Practices

### 1. Run Tests in Order

Some endpoints depend on previous ones:
- Registration → OTP Verification → Authenticated Requests
- Ride Request → Ride Acceptance → Ride Completion

### 2. Check Variable Values

Before running authenticated requests:
- Verify `auth_token` is set
- Check `user_id` or `driver_id` is populated
- Ensure `session_info` is available for OTP flows

### 3. Review Test Results

- Check all test assertions pass
- Review response times
- Verify data extraction worked
- Check console logs for warnings

### 4. Use Environment Variables

For different environments:
- Create Postman environments
- Set `base_url` per environment
- Use environment-specific test data

## 🐛 Troubleshooting

### Tests Failing

1. **Check server status**: Ensure main server is running
2. **Verify authentication**: Check if `auth_token` is set
3. **Review response**: Check actual response vs expected
4. **Check variables**: Ensure required variables are populated

### Variable Not Populating

1. Check test script execution
2. Verify response structure matches expected
3. Review console logs for errors
4. Manually set variable if needed

### Performance Issues

1. Check response times in test results
2. Verify server is not overloaded
3. Review network conditions
4. Check for timeout settings

## 📚 Related Documentation

- [Newman Postman Testing Guide](../testing/NEWMAN_POSTMAN_TESTING.md)
- [API Documentation](./API_DOCUMENTATION.md)
- [Troubleshooting 503 Error](../testing/TROUBLESHOOTING_503_ERROR.md)

## 🔄 Updating the Collection

To update the detailed collection:

1. **Modify original collection** in Postman
2. **Export** the updated collection
3. **Run generator script**: `node generate-detailed-postman-collection.js`
4. **Import** the new detailed collection

Or manually enhance requests in Postman and export.

---

**Last Updated:** 2024
**Collection Version:** 3.0.0

