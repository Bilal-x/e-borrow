from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api
from ..models import db
from ..models.user import User
from ..models.listing import Listing, ListingImage, ListingFeature
import os
from werkzeug.utils import secure_filename
from ..config import Config

@api.route('/listings', methods=['GET'])
def get_listings():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category = request.args.get('category')
    location = request.args.get('location')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Build query
    query = Listing.query
    
    # Apply filters
    if category:
        query = query.filter(Listing.category == category)
    if location:
        query = query.filter(Listing.location.ilike(f'%{location}%'))
    if min_price is not None:
        query = query.filter(Listing.price_per_day >= min_price)
    if max_price is not None:
        query = query.filter(Listing.price_per_day <= max_price)
    if search:
        query = query.filter(Listing.title.ilike(f'%{search}%') | Listing.description.ilike(f'%{search}%'))
    
    # Apply sorting
    if sort_by == 'price':
        if sort_order == 'asc':
            query = query.order_by(Listing.price_per_day.asc())
        else:
            query = query.order_by(Listing.price_per_day.desc())
    elif sort_by == 'created_at':
        if sort_order == 'asc':
            query = query.order_by(Listing.created_at.asc())
        else:
            query = query.order_by(Listing.created_at.desc())
    
    # Execute query with pagination
    listings = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'listings': [listing.to_dict() for listing in listings.items],
        'total': listings.total,
        'pages': listings.pages,
        'current_page': listings.page
    }), 200

@api.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    # Find listing by ID
    listing = Listing.query.get(listing_id)
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    return jsonify({'listing': listing.to_dict()}), 200

@api.route('/listings', methods=['POST'])
@jwt_required()
def create_listing():
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    
    # Get data from request
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'category', 'price_per_day', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new listing
    new_listing = Listing(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        price_per_day=data['price_per_day'],
        location=data['location'],
        owner_id=current_user_id
    )
    
    # Add optional fields if provided
    if 'price_per_week' in data:
        new_listing.price_per_week = data['price_per_week']
    if 'price_per_month' in data:
        new_listing.price_per_month = data['price_per_month']
    if 'latitude' in data:
        new_listing.latitude = data['latitude']
    if 'longitude' in data:
        new_listing.longitude = data['longitude']
    
    # Save to database
    db.session.add(new_listing)
    db.session.commit()
    
    # Add images if provided
    if 'images' in data and isinstance(data['images'], list):
        for image_url in data['images']:
            image = ListingImage(
                listing_id=new_listing.id,
                image_url=image_url,
                is_primary=len(new_listing.images) == 0  # First image is primary
            )
            db.session.add(image)
    
    # Add features if provided
    if 'features' in data and isinstance(data['features'], list):
        for feature_data in data['features']:
            if isinstance(feature_data, dict):
                feature = ListingFeature(
                    listing_id=new_listing.id,
                    name=feature_data.get('name'),
                    icon=feature_data.get('icon')
                )
                db.session.add(feature)
            elif isinstance(feature_data, str):
                feature = ListingFeature(
                    listing_id=new_listing.id,
                    name=feature_data
                )
                db.session.add(feature)
    
    # Commit changes
    db.session.commit()
    
    return jsonify({
        'message': 'Listing created successfully',
        'listing': new_listing.to_dict()
    }), 201

@api.route('/listings/<int:listing_id>', methods=['PUT'])
@jwt_required()
def update_listing(listing_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find listing by ID
    listing = Listing.query.get(listing_id)
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Check if user is owner or admin
    if listing.owner_id != current_user_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get data from request
    data = request.get_json()
    
    # Update listing fields
    if 'title' in data:
        listing.title = data['title']
    if 'description' in data:
        listing.description = data['description']
    if 'category' in data:
        listing.category = data['category']
    if 'price_per_day' in data:
        listing.price_per_day = data['price_per_day']
    if 'price_per_week' in data:
        listing.price_per_week = data['price_per_week']
    if 'price_per_month' in data:
        listing.price_per_month = data['price_per_month']
    if 'location' in data:
        listing.location = data['location']
    if 'latitude' in data:
        listing.latitude = data['latitude']
    if 'longitude' in data:
        listing.longitude = data['longitude']
    if 'is_available' in data:
        listing.is_available = data['is_available']
    
    # Update images if provided
    if 'images' in data and isinstance(data['images'], list):
        # Remove existing images
        for image in listing.images:
            db.session.delete(image)
        
        # Add new images
        for image_url in data['images']:
            image = ListingImage(
                listing_id=listing.id,
                image_url=image_url,
                is_primary=len(listing.images) == 0  # First image is primary
            )
            db.session.add(image)
    
    # Update features if provided
    if 'features' in data and isinstance(data['features'], list):
        # Remove existing features
        for feature in listing.features:
            db.session.delete(feature)
        
        # Add new features
        for feature_data in data['features']:
            if isinstance(feature_data, dict):
                feature = ListingFeature(
                    listing_id=listing.id,
                    name=feature_data.get('name'),
                    icon=feature_data.get('icon')
                )
                db.session.add(feature)
            elif isinstance(feature_data, str):
                feature = ListingFeature(
                    listing_id=listing.id,
                    name=feature_data
                )
                db.session.add(feature)
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'message': 'Listing updated successfully',
        'listing': listing.to_dict()
    }), 200

@api.route('/listings/<int:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find listing by ID
    listing = Listing.query.get(listing_id)
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Check if user is owner or admin
    if listing.owner_id != current_user_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Delete listing
    db.session.delete(listing)
    db.session.commit()
    
    return jsonify({'message': 'Listing deleted successfully'}), 200

@api.route('/listings/categories', methods=['GET'])
def get_categories():
    # Get all unique categories
    categories = db.session.query(Listing.category).distinct().all()
    
    return jsonify({
        'categories': [category[0] for category in categories]
    }), 200

@api.route('/listings/locations', methods=['GET'])
def get_locations():
    # Get all unique locations
    locations = db.session.query(Listing.location).distinct().all()
    
    return jsonify({
        'locations': [location[0] for location in locations]
    }), 200

@api.route('/users/<int:user_id>/listings', methods=['GET'])
def get_user_listings(user_id):
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    # Query listings by user ID
    listings = Listing.query.filter_by(owner_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'listings': [listing.to_dict() for listing in listings.items],
        'total': listings.total,
        'pages': listings.pages,
        'current_page': listings.page
    }), 200