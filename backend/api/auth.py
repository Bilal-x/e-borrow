from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import api
from ..models import db
from ..models.user import User

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    # Add optional fields if provided
    if 'phone' in data:
        new_user.phone = data['phone']
    if 'address' in data:
        new_user.address = data['address']
    if 'city' in data:
        new_user.city = data['city']
    if 'state' in data:
        new_user.state = data['state']
    
    # Save to database
    db.session.add(new_user)
    db.session.commit()
    
    # Generate access token
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': new_user.to_dict(),
        'access_token': access_token
    }), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200

@api.route('/auth/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Find admin user
    admin = User.query.filter_by(email=data['username'], is_admin=True).first()
    
    # Check if admin exists and password is correct
    if not admin or not admin.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate access token
    access_token = create_access_token(identity=admin.id)
    
    return jsonify({
        'message': 'Admin login successful',
        'user': admin.to_dict(),
        'access_token': access_token,
        'is_admin': True
    }), 200

@api.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    
    # Find user by ID
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': user.to_dict(),
        'is_admin': user.is_admin
    }), 200