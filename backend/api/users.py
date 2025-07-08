from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api
from backend.models import db
from backend.models.user import User

@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    # Check if user is admin
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query users with pagination
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    }), 200

@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only allow access to own profile or if admin
    if current_user_id != user_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Find user by ID
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@api.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only allow updating own profile or if admin
    if current_user_id != user_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Find user by ID
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get data from request
    data = request.get_json()
    
    # Update user fields
    if 'name' in data:
        user.name = data['name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'address' in data:
        user.address = data['address']
    if 'city' in data:
        user.city = data['city']
    if 'state' in data:
        user.state = data['state']
    if 'profile_image' in data:
        user.profile_image = data['profile_image']
    
    # Only admin can update these fields
    if current_user.is_admin:
        if 'is_verified' in data:
            user.is_verified = data['is_verified']
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
    
    # Update password if provided
    if 'password' in data:
        user.set_password(data['password'])
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only allow deleting own account or if admin
    if current_user_id != user_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Find user by ID
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200