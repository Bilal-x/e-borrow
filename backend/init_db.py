from backend.app import create_app
from backend.models import db
from backend.models.user import User
from backend.models.listing import Listing, ListingImage, ListingFeature
from backend.models.booking import Booking
from backend.models.review import Review
from datetime import datetime, timedelta
import random

app = create_app()

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Creating admin user...")
        # Create admin user
        admin = User(
            name="Admin",
            email="admin@e-borrow.com",
            is_admin=True,
            is_verified=True,
            profile_image="https://randomuser.me/api/portraits/men/1.jpg"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        
        print("Creating regular users...")
        # Create regular users
        users = []
        user_data = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
                "phone": "9876543210",
                "address": "123 Main St",
                "city": "Kasargod",
                "state": "Kerala",
                "profile_image": "https://randomuser.me/api/portraits/men/32.jpg",
                "is_verified": True
            },
            {
                "name": "Sarah Wilson",
                "email": "sarah@example.com",
                "password": "password123",
                "phone": "8765432109",
                "address": "456 Oak Ave",
                "city": "Kochi",
                "state": "Kerala",
                "profile_image": "https://randomuser.me/api/portraits/women/44.jpg",
                "is_verified": True
            },
            {
                "name": "Mike Johnson",
                "email": "mike@example.com",
                "password": "password123",
                "phone": "7654321098",
                "address": "789 Pine Rd",
                "city": "Bangalore",
                "state": "Karnataka",
                "profile_image": "https://randomuser.me/api/portraits/men/67.jpg",
                "is_verified": True
            },
            {
                "name": "Emily Chen",
                "email": "emily@example.com",
                "password": "password123",
                "phone": "6543210987",
                "address": "101 Cedar Ln",
                "city": "Mumbai",
                "state": "Maharashtra",
                "profile_image": "https://randomuser.me/api/portraits/women/33.jpg",
                "is_verified": True
            },
            {
                "name": "Robert Brown",
                "email": "robert@example.com",
                "password": "password123",
                "phone": "5432109876",
                "address": "202 Maple Dr",
                "city": "Delhi",
                "state": "Delhi",
                "profile_image": "https://randomuser.me/api/portraits/men/22.jpg",
                "is_verified": False
            }
        ]
        
        for data in user_data:
            user = User(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                address=data["address"],
                city=data["city"],
                state=data["state"],
                profile_image=data["profile_image"],
                is_verified=data["is_verified"]
            )
            user.set_password(data["password"])
            db.session.add(user)
            users.append(user)
        
        # Commit to get user IDs
        db.session.commit()
        
        print("Creating listings...")
        # Create listings
        listings = []
        listing_data = [
            {
                "title": "Canon EOS R5",
                "description": "Professional mirrorless camera perfect for photography and videography. This Canon EOS R5 features a 45MP full-frame sensor, 8K video recording, and advanced autofocus system. Ideal for professional photographers, content creators, and enthusiasts.",
                "category": "Photography",
                "price_per_day": 500,
                "price_per_week": 3000,
                "price_per_month": 10000,
                "location": "Kasargod, Kerala",
                "owner_id": users[0].id,
                "features": [
                    {"name": "45MP Full-Frame Sensor", "icon": "camera"},
                    {"name": "8K Video Recording", "icon": "video"},
                    {"name": "20fps Burst Mode", "icon": "bolt"},
                    {"name": "Built-in WiFi & Bluetooth", "icon": "wifi"},
                    {"name": "Weather Sealed", "icon": "shield-alt"},
                    {"name": "Extended Battery Life", "icon": "battery-full"}
                ],
                "images": [
                    "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FtZXJhfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8Y2FtZXJhfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1581591524425-c7e0978865fc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGNhbWVyYXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
                ]
            },
            {
                "title": "Mountain Bike",
                "description": "High-quality mountain bike perfect for trails and off-road adventures. Features a lightweight aluminum frame, 27-speed Shimano gears, hydraulic disc brakes, and front suspension for a smooth ride on rough terrain.",
                "category": "Sports",
                "price_per_day": 200,
                "price_per_week": 1200,
                "price_per_month": 4000,
                "location": "Kochi, Kerala",
                "owner_id": users[1].id,
                "features": [
                    {"name": "Aluminum Frame", "icon": "bicycle"},
                    {"name": "27-Speed Shimano Gears", "icon": "cog"},
                    {"name": "Hydraulic Disc Brakes", "icon": "brake-warning"},
                    {"name": "Front Suspension", "icon": "compress"},
                    {"name": "29-inch Wheels", "icon": "circle"}
                ],
                "images": [
                    "https://images.unsplash.com/photo-1485965120184-e220f721d03e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmljeWNsZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1571068316344-75bc76f77890?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YmljeWNsZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YmljeWNsZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
                ]
            },
            {
                "title": "MacBook Pro",
                "description": "Latest model MacBook Pro with M2 chip, 16GB RAM, and 512GB SSD. Perfect for professionals, designers, and developers. Features a stunning Retina display, excellent battery life, and powerful performance for all your computing needs.",
                "category": "Electronics",
                "price_per_day": 800,
                "price_per_week": 5000,
                "price_per_month": 18000,
                "location": "Bangalore, Karnataka",
                "owner_id": users[2].id,
                "features": [
                    {"name": "M2 Chip", "icon": "microchip"},
                    {"name": "16GB RAM", "icon": "memory"},
                    {"name": "512GB SSD", "icon": "hdd"},
                    {"name": "Retina Display", "icon": "desktop"},
                    {"name": "10-hour Battery Life", "icon": "battery-full"},
                    {"name": "macOS Ventura", "icon": "apple"}
                ],
                "images": [
                    "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bWFjYm9va3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8bWFjYm9va3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bWFjYm9va3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
                ]
            },
            {
                "title": "Camping Tent",
                "description": "Spacious 4-person camping tent, perfect for outdoor adventures. Features waterproof material, easy setup, and excellent ventilation. Includes a rainfly, stakes, and carrying bag for convenient transport.",
                "category": "Outdoors",
                "price_per_day": 350,
                "price_per_week": 2000,
                "price_per_month": 7000,
                "location": "Mumbai, Maharashtra",
                "owner_id": users[3].id,
                "features": [
                    {"name": "4-Person Capacity", "icon": "users"},
                    {"name": "Waterproof", "icon": "tint"},
                    {"name": "Easy Setup", "icon": "clock"},
                    {"name": "Excellent Ventilation", "icon": "wind"},
                    {"name": "Includes Rainfly", "icon": "cloud-rain"},
                    {"name": "Carrying Bag", "icon": "suitcase"}
                ],
                "images": [
                    "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FtcGluZyUyMHRlbnR8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1563299796-17596ed6b017?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8Y2FtcGluZyUyMHRlbnR8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8Y2FtcGluZyUyMHRlbnR8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60"
                ]
            },
            {
                "title": "Power Drill",
                "description": "Professional-grade power drill with variable speed and multiple drill bits. Perfect for DIY projects, home repairs, and construction work. Includes a carrying case and rechargeable battery.",
                "category": "Tools",
                "price_per_day": 150,
                "price_per_week": 900,
                "price_per_month": 3000,
                "location": "Delhi, Delhi",
                "owner_id": users[4].id,
                "features": [
                    {"name": "Variable Speed", "icon": "tachometer-alt"},
                    {"name": "Multiple Drill Bits", "icon": "tools"},
                    {"name": "Rechargeable Battery", "icon": "battery-full"},
                    {"name": "Carrying Case", "icon": "briefcase"},
                    {"name": "LED Work Light", "icon": "lightbulb"}
                ],
                "images": [
                    "https://images.unsplash.com/photo-1504148455328-c376907d081c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cG93ZXIlMjBkcmlsbHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1616321507403-9e5d7b13c6c9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8cG93ZXIlMjBkcmlsbHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
                    "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cG93ZXIlMjBkcmlsbHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
                ]
            }
        ]
        
        for data in listing_data:
            listing = Listing(
                title=data["title"],
                description=data["description"],
                category=data["category"],
                price_per_day=data["price_per_day"],
                price_per_week=data["price_per_week"],
                price_per_month=data["price_per_month"],
                location=data["location"],
                owner_id=data["owner_id"]
            )
            db.session.add(listing)
            listings.append(listing)
        
        # Commit to get listing IDs
        db.session.commit()
        
        # Add images and features to listings
        for i, data in enumerate(listing_data):
            # Add images
            for j, image_url in enumerate(data["images"]):
                image = ListingImage(
                    listing_id=listings[i].id,
                    image_url=image_url,
                    is_primary=(j == 0)  # First image is primary
                )
                db.session.add(image)
            
            # Add features
            for feature_data in data["features"]:
                feature = ListingFeature(
                    listing_id=listings[i].id,
                    name=feature_data["name"],
                    icon=feature_data["icon"]
                )
                db.session.add(feature)
        
        print("Creating bookings...")
        # Create bookings
        bookings = []
        today = datetime.now().date()
        
        # Completed bookings
        for i in range(5):
            start_date = today - timedelta(days=random.randint(30, 60))
            end_date = start_date + timedelta(days=random.randint(3, 7))
            
            listing = random.choice(listings)
            renter = random.choice([user for user in users if user.id != listing.owner_id])
            
            days = (end_date - start_date).days
            total_price = days * listing.price_per_day
            
            booking = Booking(
                listing_id=listing.id,
                renter_id=renter.id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status="completed",
                payment_status="paid"
            )
            db.session.add(booking)
            bookings.append(booking)
        
        # Active bookings
        for i in range(3):
            start_date = today - timedelta(days=random.randint(1, 5))
            end_date = start_date + timedelta(days=random.randint(7, 14))
            
            listing = random.choice(listings)
            renter = random.choice([user for user in users if user.id != listing.owner_id])
            
            days = (end_date - start_date).days
            total_price = days * listing.price_per_day
            
            booking = Booking(
                listing_id=listing.id,
                renter_id=renter.id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status="confirmed",
                payment_status="paid"
            )
            db.session.add(booking)
            bookings.append(booking)
        
        # Upcoming bookings
        for i in range(3):
            start_date = today + timedelta(days=random.randint(5, 20))
            end_date = start_date + timedelta(days=random.randint(3, 10))
            
            listing = random.choice(listings)
            renter = random.choice([user for user in users if user.id != listing.owner_id])
            
            days = (end_date - start_date).days
            total_price = days * listing.price_per_day
            
            booking = Booking(
                listing_id=listing.id,
                renter_id=renter.id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status="confirmed",
                payment_status="paid"
            )
            db.session.add(booking)
            bookings.append(booking)
        
        # Pending bookings
        for i in range(2):
            start_date = today + timedelta(days=random.randint(10, 30))
            end_date = start_date + timedelta(days=random.randint(3, 7))
            
            listing = random.choice(listings)
            renter = random.choice([user for user in users if user.id != listing.owner_id])
            
            days = (end_date - start_date).days
            total_price = days * listing.price_per_day
            
            booking = Booking(
                listing_id=listing.id,
                renter_id=renter.id,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status="pending",
                payment_status="pending"
            )
            db.session.add(booking)
            bookings.append(booking)
        
        # Commit to get booking IDs
        db.session.commit()
        
        print("Creating reviews...")
        # Create reviews for completed bookings
        for booking in bookings:
            if booking.status == "completed":
                # Renter reviews listing owner
                listing = Listing.query.get(booking.listing_id)
                
                review = Review(
                    listing_id=booking.listing_id,
                    reviewer_id=booking.renter_id,
                    reviewee_id=listing.owner_id,
                    booking_id=booking.id,
                    rating=random.randint(3, 5),
                    comment=random.choice([
                        "Great experience! The item was in perfect condition and the owner was very helpful.",
                        "Excellent service and communication. Would definitely rent from this person again.",
                        "Item was as described and worked perfectly. Very satisfied with the rental.",
                        "Smooth transaction and the owner was very accommodating with pickup and return times.",
                        "Very professional and friendly. The item was clean and well-maintained."
                    ])
                )
                db.session.add(review)
                
                # Owner reviews renter
                review = Review(
                    listing_id=booking.listing_id,
                    reviewer_id=listing.owner_id,
                    reviewee_id=booking.renter_id,
                    booking_id=booking.id,
                    rating=random.randint(4, 5),
                    comment=random.choice([
                        "Great renter! Took good care of my item and returned it on time.",
                        "Very responsible and respectful. Would rent to this person again.",
                        "Excellent communication and punctuality. Item was returned in perfect condition.",
                        "A pleasure to deal with. Very trustworthy renter.",
                        "Responsible renter who treated my item with care. Highly recommended!"
                    ])
                )
                db.session.add(review)
        
        # Commit all changes
        db.session.commit()
        
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()