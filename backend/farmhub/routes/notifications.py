from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.notification_service import (
    get_notifications,
    mark_all_as_read,
    mark_as_read,
    get_unread_count
)
from services.exceptions import NotFoundError, InvalidUsage

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_user_notifications():
    """
    Get all notifications for the current user
    ---
    tags:
      - Notifications
    responses:
      200:
        description: List of notifications
        schema:
          type: array
          items:
            $ref: '#/definitions/Notification'
    """
    user_id = get_jwt_identity()
    notifications = get_notifications(user_id)
    return jsonify([n.to_dict() for n in notifications]), 200

@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_user_unread_count():
    """
    Get unread notification count
    ---
    tags:
      - Notifications
    responses:
      200:
        description: Unread count
        schema:
          type: object
          properties:
            count:
              type: integer
    """
    user_id = get_jwt_identity()
    count = get_unread_count(user_id)
    return jsonify({'count': count}), 200

@notifications_bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_notifications_read():
    """
    Mark all notifications as read
    ---
    tags:
      - Notifications
    responses:
      200:
        description: All notifications marked as read
    """
    user_id = get_jwt_identity()
    mark_all_as_read(user_id)
    return jsonify({'message': 'All notifications marked as read'}), 200

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_single_notification_read(notification_id):
    """
    Mark a single notification as read
    ---
    tags:
      - Notifications
    parameters:
      - name: notification_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Notification marked as read
      404:
        description: Notification not found
    """
    user_id = get_jwt_identity()
    try:
        mark_as_read(user_id, notification_id)
        return jsonify({'message': 'Notification marked as read'}), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)