# Scripts Directory

This directory contains utility scripts for the Londa Rides API.

## Available Scripts

### 1. create_test_drivers.py

Creates test drivers with location data in Firestore for development and testing.

**Purpose:**
- Populate Firestore with test drivers that have valid location data
- Test the nearby drivers functionality
- Development and debugging

**Usage:**
```bash
# Make sure you're in the project root with venv activated
python scripts/create_test_drivers.py
```

**What it creates:**
- 8 test drivers with locations around Windhoek, Namibia
- Drivers at various distances from city center (0.5km to 3.3km)
- Complete driver profiles with vehicle information
- Mix of online and offline drivers

**Output:**
```
📊 TEST DRIVERS CREATION SUMMARY
✅ Created: 8 drivers
📍 Total: 8 drivers with location data

📍 TEST DRIVER LOCATIONS (Windhoek area):
🟢 John Doe             | -22.5700, 17.0836 | online
🟢 Jane Smith           | -22.5650, 17.0800 | online
...
```

---

### 2. test_nearby_drivers.py

Tests the `/nearby-drivers` endpoint to verify proper functionality.

**Purpose:**
- Verify GeoPoint serialization works correctly
- Test distance calculation accuracy
- Validate radius filtering
- Check error handling

**Usage:**
```bash
# Set your authentication token
export TEST_AUTH_TOKEN="your_firebase_id_token_here"

# Run tests
python scripts/test_nearby_drivers.py
```

**Environment Variables:**
- `TEST_AUTH_TOKEN` - Firebase ID token for authentication (required)
- `API_BASE_URL` - API server URL (default: http://localhost:8000)

**What it tests:**
1. Default 5km radius search
2. Large radius (10km) search
3. Small radius (1km) search
4. Different search locations

**Expected Output:**
```
🧪 NEARBY DRIVERS ENDPOINT TEST SUITE
======================================================================
TEST 1: Windhoek City Center (Default 5km radius)
======================================================================
📍 Testing nearby drivers at (-22.57, 17.0836) with radius 5.0km
✅ SUCCESS!
📊 Found 6 drivers:
  1. John Doe
     Status: online
     Distance: 0.52 km
     Location: {'latitude': -22.57, 'longitude': 17.0836}
     ✅ Location properly serialized
...
```

---

## Prerequisites

Both scripts require:

1. **Python Environment**
   ```bash
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate      # Linux/Mac
   ```

2. **Firebase Configuration**
   - Firebase credentials file must be present
   - `GOOGLE_APPLICATION_CREDENTIALS` environment variable set
   - Or credentials configured in `.env` file

3. **API Server Running** (for test_nearby_drivers.py)
   ```bash
   python run.py
   ```

---

## Common Issues

### Issue: "Firebase not initialized"
**Solution:** Make sure your Firebase credentials are properly configured:
```bash
# Check if credentials file exists
ls firebase-credentials.json

# Or set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/firebase-credentials.json"
```

### Issue: "Could not connect to server"
**Solution:** Make sure the API server is running:
```bash
# In a separate terminal
python run.py
```

### Issue: "No TEST_AUTH_TOKEN environment variable found"
**Solution:** Get a valid token and set it:
```bash
# Get token from your mobile app or use Postman to call:
# POST /api/v1/send-otp
# POST /api/v1/verify-otp
# Then set the token:
export TEST_AUTH_TOKEN="your_token_here"
```

---

## Development Tips

### Creating More Test Data

Modify `create_test_drivers.py` to add more test drivers:

```python
test_drivers = [
    {
        "id": "test_driver_9",
        "name": "Your Name",
        "location": firestore.GeoPoint(-22.5800, 17.0900),
        "status": "online",
        # ... other fields
    }
]
```

### Testing Different Scenarios

Modify `test_nearby_drivers.py` to test specific scenarios:

```python
# Test with very small radius
test_nearby_drivers(
    latitude=-22.5700,
    longitude=17.0836,
    radius=0.5,  # Only 500 meters
    token=token
)

# Test at edge of coverage
test_nearby_drivers(
    latitude=-22.6000,
    longitude=17.0836,
    radius=5.0,
    token=token
)
```

---

## Related Documentation

- [NEARBY_DRIVERS_FIX_SUMMARY.md](../NEARBY_DRIVERS_FIX_SUMMARY.md) - Complete fix documentation
- [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) - API reference
- [FIRESTORE_INDEXES.md](../FIRESTORE_INDEXES.md) - Database indexes

---

**Last Updated:** January 4, 2026

