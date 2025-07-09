from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.settings_service import (
    get_user_settings,
    update_user_settings,
    change_password
)
from services.exceptions import NotFoundError, AuthError, InvalidUsage
from utils.validators import validate_password_change

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('', methods=['GET'])
@jwt_required()
def get_settings():
    """
    Get user settings
    ---
    tags:
      - Settings
    responses:
      200:
        description: User settings
        schema:
          $ref: '#/definitions/UserSettings'
    """
    user_id = get_jwt_identity()
    settings = get_user_settings(user_id)
    return jsonify(settings.to_dict()), 200

@settings_bp.route('', methods=['PUT'])
@jwt_required()
def update_settings():
    """
    Update user settings
    ---
    tags:
      - Settings
    parameters:
      - in: body
        name: settings
        description: Updated settings
        schema:
          $ref: '#/definitions/UserSettingsUpdate'
    responses:
      200:
        description: Updated settings
        schema:
          $ref: '#/definitions/UserSettings'
      400:
        description: Invalid input
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        settings = update_user_settings(user_id, data)
        return jsonify(settings.to_dict()), 200
    except Exception as e:
        raise InvalidUsage(str(e), status_code=400)

@settings_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_user_password():
    """
    Change user password
    ---
    tags:
      - Settings
    parameters:
      - in: body
        name: passwords
        description: Password change data
        schema:
          $ref: '#/definitions/PasswordChange'
    responses:
      200:
        description: Password changed
      400:
        description: Invalid input
      401:
        description: Invalid current password
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate input
    errors = validate_password_change(data)
    if errors:
        raise InvalidUsage('Validation failed', status_code=400, payload=errors)
    
    try:
        change_password(
            user_id, 
            data['current_password'], 
            data['new_password']
        )
        return jsonify({'message': 'Password changed successfully'}), 200
    except AuthError as e:
        raise InvalidUsage(str(e), status_code=401)