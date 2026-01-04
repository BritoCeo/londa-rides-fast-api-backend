"""
Script to create test drivers with location data in Firestore

This script creates test drivers with:
- Valid location data (GeoPoint with Windhoek coordinates)
- Online status
- Complete profile information
- Active subscription status

Usage:
    python scripts/create_test_drivers.py
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from firebase_admin import firestore
from app.core.firebase import get_firestore, initialize_firebase
from app.core.logging import logger


def create_test_drivers():
    """Create test drivers with location data"""
    
    # Initialize Firebase
    initialize_firebase()
    db = get_firestore()
    
    # Test driver data - Windhoek area coordinates
    test_drivers = [
        {
            "id": "test_driver_1",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "+264811234567",
            "status": "online",
            "location": firestore.GeoPoint(-22.5700, 17.0836),  # Windhoek city center
            "license_number": "DL123456",
            "vehicle_model": "Toyota Corolla",
            "vehicle_plate": "N12345W",
            "vehicle_color": "Silver",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_2",
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone_number": "+264811234568",
            "status": "online",
            "location": firestore.GeoPoint(-22.5650, 17.0800),  # ~0.5km north
            "license_number": "DL123457",
            "vehicle_model": "Honda Civic",
            "vehicle_plate": "N12346W",
            "vehicle_color": "Blue",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_3",
            "name": "Michael Johnson",
            "email": "michael.j@example.com",
            "phone_number": "+264811234569",
            "status": "online",
            "location": firestore.GeoPoint(-22.5750, 17.0870),  # ~0.7km south-east
            "license_number": "DL123458",
            "vehicle_model": "Nissan Almera",
            "vehicle_plate": "N12347W",
            "vehicle_color": "White",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_4",
            "name": "Sarah Williams",
            "email": "sarah.w@example.com",
            "phone_number": "+264811234570",
            "status": "online",
            "location": firestore.GeoPoint(-22.5600, 17.0900),  # ~1.5km north-east
            "license_number": "DL123459",
            "vehicle_model": "Volkswagen Polo",
            "vehicle_plate": "N12348W",
            "vehicle_color": "Red",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_5",
            "name": "David Brown",
            "email": "david.b@example.com",
            "phone_number": "+264811234571",
            "status": "online",
            "location": firestore.GeoPoint(-22.5800, 17.0750),  # ~1.5km south-west
            "license_number": "DL123460",
            "vehicle_model": "Toyota Yaris",
            "vehicle_plate": "N12349W",
            "vehicle_color": "Black",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_6",
            "name": "Emma Davis",
            "email": "emma.d@example.com",
            "phone_number": "+264811234572",
            "status": "online",
            "location": firestore.GeoPoint(-22.5500, 17.0836),  # ~2.2km north
            "license_number": "DL123461",
            "vehicle_model": "Hyundai i20",
            "vehicle_plate": "N12350W",
            "vehicle_color": "Grey",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_7",
            "name": "James Wilson",
            "email": "james.w@example.com",
            "phone_number": "+264811234573",
            "status": "offline",  # One offline driver for testing
            "location": firestore.GeoPoint(-22.5700, 17.0950),  # ~1.2km east
            "license_number": "DL123462",
            "vehicle_model": "Mazda 3",
            "vehicle_plate": "N12351W",
            "vehicle_color": "Green",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
        {
            "id": "test_driver_8",
            "name": "Olivia Martinez",
            "email": "olivia.m@example.com",
            "phone_number": "+264811234574",
            "status": "online",
            "location": firestore.GeoPoint(-22.6000, 17.0836),  # ~3.3km south (outside 5km default radius from some points)
            "license_number": "DL123463",
            "vehicle_model": "Kia Rio",
            "vehicle_plate": "N12352W",
            "vehicle_color": "Yellow",
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
        },
    ]
    
    # Create drivers in Firestore
    drivers_collection = db.collection("drivers")
    created_count = 0
    updated_count = 0
    
    for driver_data in test_drivers:
        try:
            driver_id = driver_data["id"]
            doc_ref = drivers_collection.document(driver_id)
            
            # Check if driver already exists
            doc = doc_ref.get()
            if doc.exists:
                # Update existing driver
                doc_ref.update({
                    "location": driver_data["location"],
                    "status": driver_data["status"],
                    "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
                    "updatedAt": firestore.SERVER_TIMESTAMP,
                })
                updated_count += 1
                logger.info(f"✅ Updated test driver: {driver_data['name']} ({driver_id})")
            else:
                # Create new driver
                doc_ref.set(driver_data)
                created_count += 1
                logger.info(f"✅ Created test driver: {driver_data['name']} ({driver_id})")
                
        except Exception as e:
            logger.error(f"❌ Error creating/updating driver {driver_data['name']}: {str(e)}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST DRIVERS CREATION SUMMARY")
    print("="*60)
    print(f"✅ Created: {created_count} drivers")
    print(f"🔄 Updated: {updated_count} drivers")
    print(f"📍 Total: {created_count + updated_count} drivers with location data")
    print("="*60)
    
    # Print location info
    print("\n📍 TEST DRIVER LOCATIONS (Windhoek area):")
    print("-" * 60)
    for driver in test_drivers:
        lat = driver["location"].latitude
        lng = driver["location"].longitude
        status = driver["status"]
        status_emoji = "🟢" if status == "online" else "🔴"
        print(f"{status_emoji} {driver['name']:<20} | {lat:>9.4f}, {lng:>9.4f} | {status}")
    print("-" * 60)
    
    print("\n💡 TIP: Use coordinates around -22.5700, 17.0836 (Windhoek) to test nearby drivers")
    print("💡 Default search radius is 5km")
    print("\n✅ Test drivers created successfully!")


if __name__ == "__main__":
    try:
        create_test_drivers()
    except Exception as e:
        logger.error(f"Failed to create test drivers: {str(e)}", exc_info=True)
        sys.exit(1)

