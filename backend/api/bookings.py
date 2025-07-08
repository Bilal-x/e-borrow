from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api
from ..models import db
from ..models.user import User
from ..models.listing import Listing
from ..models.booking import Booking
from datetime import datetime

@api.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    # Build query
    if current_user.is_admin:
        # Admin can see all bookings
        query = Booking.query
    else:
        # Regular users can only see their own bookings
        query = Booking.query.filter(
            (Booking.renter_id == current_user_id) | 
            (Listing.owner_id == current_user_id)
        ).join(Listing)
    
    # Apply status filter if provided
    if status:
        query = query.filter(Booking.status == status)
    
    # Execute query with pagination
    bookings = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'bookings': [booking.to_dict() for booking in bookings.items],
        'total': bookings.total,
        'pages': bookings.pages,
        'current_page': bookings.page
    }), 200

@api.route('/bookings/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find booking by ID
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check if user is authorized to view this booking
    listing = Listing.query.get(booking.listing_id)
    if not current_user.is_admin and current_user_id != booking.renter_id and current_user_id != listing.owner_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    return jsonify({'booking': booking.to_dict()}), 200

@api.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    
    # Get data from request
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['listing_id', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Find listing by ID
    listing = Listing.query.get(data['listing_id'])
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Check if listing is available
    if not listing.is_available:
        return jsonify({'error': 'Listing is not available for booking'}), 400
    
    # Check if user is trying to book their own listing
    if listing.owner_id == current_user_id:
        return jsonify({'error': 'You cannot book your own listing'}), 400
    
    # Parse dates
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Check if end date is after start date
    if end_date <= start_date:
        return jsonify({'error': 'End date must be after start date'}), 400
    
    # Check for booking conflicts
    conflicting_bookings = Booking.query.filter(
        Booking.listing_id == listing.id,
        Booking.status.in_(['pending', 'confirmed']),
        Booking.start_date <= end_date,
        Booking.end_date >= start_date
    ).all()
    
    if conflicting_bookings:
        return jsonify({'error': 'Listing is already booked for the selected dates'}), 400
    
    # Calculate total price
    days = (end_date - start_date).days
    total_price = 0
    
    if days >= 30 and listing.price_per_month:
        months = days // 30
        remaining_days = days % 30
        total_price = (months * listing.price_per_month) + (remaining_days * listing.price_per_day)
    elif days >= 7 and listing.price_per_week:
        weeks = days // 7
        remaining_days = days % 7
        total_price = (weeks * listing.price_per_week) + (remaining_days * listing.price_per_day)
    else:
        total_price = days * listing.price_per_day
    
    # Create new booking
    new_booking = Booking(
        listing_id=listing.id,
        renter_id=current_user_id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        status='pending',
        payment_status='pending'
    )
    
    # Save to database
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking': new_booking.to_dict()
    }), 201

@api.route('/bookings/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find booking by ID
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Get listing owner
    listing = Listing.query.get(booking.listing_id)
    
    # Check if user is authorized to update this booking
    if not current_user.is_admin and current_user_id != listing.owner_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get data from request
    data = request.get_json()
    
    # Validate status
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
    
    # Update booking status
    booking.status = data['status']
    
    # Update payment status if provided
    if 'payment_status' in data:
        valid_payment_statuses = ['pending', 'paid', 'refunded']
        if data['payment_status'] not in valid_payment_statuses:
            return jsonify({'error': f'Invalid payment status. Must be one of: {", ".join(valid_payment_statuses)}'}), 400
        
        booking.payment_status = data['payment_status']
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'message': 'Booking updated successfully',
        'booking': booking.to_dict()
    }), 200

@api.route('/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find booking by ID
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check if user is authorized to delete this booking
    if not current_user.is_admin and current_user_id != booking.renter_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Delete booking
    db.session.delete(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking deleted successfully'}), 200

@api.route('/users/<int:user_id>/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings(user_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Check if user is authorized to view these bookings
    if not current_user.is_admin and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    # Build query
    query = Booking.query.filter_by(renter_id=user_id)
    
    # Apply status filter if provided
    if status:
        query = query.filter(Booking.status == status)
    
    # Execute query with pagination
    bookings = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'bookings': [booking.to_dict() for booking in bookings.items],
        'total': bookings.total,
        'pages': bookings.pages,
        'current_page': bookings.page
    }), 200

@api.route('/listings/<int:listing_id>/bookings', methods=['GET'])
@jwt_required()
def get_listing_bookings(listing_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Find listing by ID
    listing = Listing.query.get(listing_id)
    
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    # Check if user is authorized to view these bookings
    if not current_user.is_admin and current_user_id != listing.owner_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    # Build query
    query = Booking.query.filter_by(listing_id=listing_id)
    
    # Apply status filter if provided
    if status:
        query = query.filter(Booking.status == status)
    
    # Execute query with pagination
    bookings = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'bookings': [booking.to_dict() for booking in bookings.items],
        'total': bookings.total,
        'pages': bookings.pages,
        'current_page': bookings.page
    }), 200