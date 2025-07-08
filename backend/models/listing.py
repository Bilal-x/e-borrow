from . import db
from datetime import datetime

class Listing(db.Model):
    __tablename__ = 'listings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    price_per_week = db.Column(db.Float, nullable=True)
    price_per_month = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('ListingImage', backref='listing', lazy=True, cascade='all, delete-orphan')
    features = db.relationship('ListingFeature', backref='listing', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='listing', lazy=True)
    reviews = db.relationship('Review', backref='listing', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price_per_day': self.price_per_day,
            'price_per_week': self.price_per_week,
            'price_per_month': self.price_per_month,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_available': self.is_available,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'owner_image': self.owner.profile_image if self.owner else None,
            'images': [img.image_url for img in self.images],
            'features': [feature.name for feature in self.features],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'avg_rating': self.get_average_rating()
        }
    
    def get_average_rating(self):
        if not self.reviews:
            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)


class ListingImage(db.Model):
    __tablename__ = 'listing_images'
    
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ListingFeature(db.Model):
    __tablename__ = 'listing_features'
    
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)