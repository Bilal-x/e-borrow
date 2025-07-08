from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api
from ..models import db
from ..models.user import User
from ..models.listing import Listing
from ..models.booking import Booking
from ..models.review import Review

@api.route('/reviews', methods=['GET'])
def get_reviews():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    listing_id = request.args.get('listing_id', type=int)
    reviewer_id = request.args.get('reviewer_id', type=int)
    reviewee_id = request.args.get('reviewee_id', type=int)
    
    # Build query
    query = Review.query
    
    # Apply filters
    if listing_id:
        query = query.filter_by(listing_id=listing_id)
    if reviewer_id:
        query = query.filter_by(reviewer_id=reviewer_id)
    if reviewee_id:
        query = query.filter_by(reviewee_id=reviewee_id)
    
    # Execute query with pagination
    reviews = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'current_page': reviews.page
    }), 200

@api.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    # Find review by ID
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    return jsonify({'review': review.to_dict()}), 200

@api.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    
    # Get data from request
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['listing_id', 'reviewee_id', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Find listing by ID
    listing = Listing.query.get(data['listing_id'])
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Find reviewee by ID
    reviewee = User.query.get(data['reviewee_id'])
    
    if not reviewee:
        return jsonify({'error': 'Reviewee not found'}), 404
    
    # Validate rating
    if not isinstance(data['rating'], int) or data['rating'] < 1 or data['rating'] > 5:
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
    
    # Check if booking exists (if booking_id is provided)
    if 'booking_id' in data:
        booking = Booking.query.get(data['booking_id'])
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user is the renter of this booking
        if booking.renter_id != current_user_id:
            return jsonify({'error': 'You can only review bookings you made'}), 403
        
        # Check if booking is completed
        if booking.status != 'completed':
            return jsonify({'error': 'You can only review completed bookings'}), 400
    
    # Check if user is reviewing themselves
    if current_user_id == data['reviewee_id']:
        return jsonify({'error': 'You cannot review yourself'}), 400
    
    # Check if user has already reviewed this listing for this reviewee
    existing_review = Review.query.filter_by(
        listing_id=data['listing_id'],
        reviewer_id=current_user_id,
        reviewee_id=data['reviewee_id']
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this listing for this user'}), 400
    
    # Create new review
    new_review = Review(
        listing_id=data['listing_id'],
        reviewer_id=current_user_id,
        reviewee_id=data['reviewee_id'],
        rating=data['rating']
    )
    
    # Add optional fields if provided
    if 'booking_id' in data:
        new_review.booking_id = data['booking_id']
    if 'comment' in data:
        new_review.comment = data['comment']
    
    # Save to database
    db.session.add(new_review)
    db.session.commit()
    
    return jsonify({
        'message': 'Review created successfully',
        'review': new_review.to_dict()
    }), 201

@api.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find review by ID
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    # Check if user is authorized to update this review
    if not current_user.is_admin and current_user_id != review.reviewer_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get data from request
    data = request.get_json()
    
    # Update review fields
    if 'rating' in data:
        if not isinstance(data['rating'], int) or data['rating'] < 1 or data['rating'] > 5:
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        review.rating = data['rating']
    
    if 'comment' in data:
        review.comment = data['comment']
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'message': 'Review updated successfully',
        'review': review.to_dict()
    }), 200

@api.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find review by ID
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    # Check if user is authorized to delete this review
    if not current_user.is_admin and current_user_id != review.reviewer_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Delete review
    db.session.delete(review)
    db.session.commit()
    
    return jsonify({'message': 'Review deleted successfully'}), 200

@api.route('/listings/<int:listing_id>/reviews', methods=['GET'])
def get_listing_reviews(listing_id):
    # Find listing by ID
    listing = Listing.query.get(listing_id)
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query reviews by listing ID
    reviews = Review.query.filter_by(listing_id=listing_id).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'current_page': reviews.page
    }), 200

@api.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    # Find user by ID
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    review_type = request.args.get('type', 'received')  # 'received' or 'given'
    
    # Query reviews by user ID
    if review_type == 'received':
        reviews = Review.query.filter_by(reviewee_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    else:
        reviews = Review.query.filter_by(reviewer_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reviews': [review.to_dict() for review in reviews.items],
        'total': reviews.total,
        'pages': reviews.pages,
        'current_page': reviews.page
    }), 200