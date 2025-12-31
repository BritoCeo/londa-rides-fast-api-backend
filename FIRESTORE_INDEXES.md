# 🔥 Firestore Indexes Required

## Overview

Firestore requires composite indexes for queries that filter and order by different fields. This document lists all required indexes for the Londa API.

---

## Required Indexes

### 1. Rides Collection - User Rides Query

**Query:** Get rides for a user, ordered by creation date (descending)

**Fields:**
- `userId` (Ascending)
- `createdAt` (Descending)

**Collection:** `rides`

**Index Creation:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `londa-cd054`
3. Navigate to Firestore Database → Indexes
4. Click "Create Index"
5. Set:
   - Collection ID: `rides`
   - Fields:
     - Field: `userId`, Order: Ascending
     - Field: `createdAt`, Order: Descending
6. Click "Create"

**Or use the direct link from the error message** (when it appears in logs)

---

### 2. Rides Collection - Driver Rides Query

**Query:** Get rides for a driver, ordered by creation date (descending)

**Fields:**
- `driverId` (Ascending)
- `createdAt` (Descending)

**Collection:** `rides`

**Index Creation:**
1. Go to Firebase Console → Firestore → Indexes
2. Click "Create Index"
3. Set:
   - Collection ID: `rides`
   - Fields:
     - Field: `driverId`, Order: Ascending
     - Field: `createdAt`, Order: Descending
4. Click "Create"

---

### 3. Rides Collection - Pending Rides Query

**Query:** Get pending rides, ordered by creation date (descending)

**Fields:**
- `status` (Ascending)
- `createdAt` (Descending)

**Collection:** `rides`

**Index Creation:**
1. Go to Firebase Console → Firestore → Indexes
2. Click "Create Index"
3. Set:
   - Collection ID: `rides`
   - Fields:
     - Field: `status`, Order: Ascending
     - Field: `createdAt`, Order: Descending
4. Click "Create"

---

## Quick Index Creation

### Using Firebase Console

1. **Navigate to Firestore Indexes:**
   ```
   Firebase Console → Firestore Database → Indexes → Create Index
   ```

2. **For each index above:**
   - Select collection
   - Add fields with correct order
   - Click "Create"

### Using Firebase CLI (Alternative)

If you have `firebase-tools` installed:

```bash
firebase init firestore
# Then edit firestore.indexes.json and add:
{
  "indexes": [
    {
      "collectionGroup": "rides",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "userId",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "createdAt",
          "order": "DESCENDING"
        }
      ]
    },
    {
      "collectionGroup": "rides",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "driverId",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "createdAt",
          "order": "DESCENDING"
        }
      ]
    },
    {
      "collectionGroup": "rides",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "status",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "createdAt",
          "order": "DESCENDING"
        }
      ]
    }
  ],
  "fieldOverrides": []
}
```

Then deploy:
```bash
firebase deploy --only firestore:indexes
```

---

## Index Status

Indexes can take a few minutes to build, especially if you have existing data. You'll see the status in Firebase Console:

- ⏳ **Building** - Index is being created
- ✅ **Enabled** - Index is ready to use
- ❌ **Error** - Check error message and fix

---

## Error Messages

If you see an error like:
```
The query requires an index. You can create it here: https://...
```

1. Click the link in the error message (easiest way)
2. Or follow the manual steps above
3. Wait for the index to build
4. Retry your query

---

## Best Practices

1. **Create indexes before deploying to production**
   - Test all queries in development
   - Create required indexes early

2. **Monitor index usage**
   - Check Firebase Console for index performance
   - Remove unused indexes to save costs

3. **Index building time**
   - Small collections: Seconds
   - Large collections: Minutes to hours
   - Plan accordingly

---

## Current Status

**Required Indexes:**
- [ ] `rides` - userId (ASC) + createdAt (DESC)
- [ ] `rides` - driverId (ASC) + createdAt (DESC)
- [ ] `rides` - status (ASC) + createdAt (DESC)

**Note:** Create these indexes in Firebase Console before using the corresponding endpoints.

---

**Last Updated:** 2025-12-31

