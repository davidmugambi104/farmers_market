from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import register_user, login_user, get_current_user
from services.exceptions import InvalidUsage
from utils.validators import validate_user_registration, validate_user_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    errors = validate_user_registration(data)
    if errors:
        raise InvalidUsage('Validation failed', status_code=400, payload=errors)
    
    try:
        user = register_user(data)
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
    except Exception as e:
        raise InvalidUsage(str(e), status_code=400)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    errors = validate_user_login(data)
    if errors:
        raise InvalidUsage('Validation failed', status_code=400, payload=errors)
    
    try:
        user = login_user(data)
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'farm_name': user.farm_name
            }
        }), 200
    except Exception as e:
        raise InvalidUsage(str(e), status_code=401)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = get_current_user(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'farm_name': user.farm_name
    }), 200