from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.message_service import (
    get_conversations,
    get_conversation,
    send_message,
    mark_as_read
)
from services.exceptions import NotFoundError, InvalidUsage

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_user_conversations():
    """
    Get all conversations for the current user
    ---
    tags:
      - Messages
    responses:
      200:
        description: List of conversations
        schema:
          type: array
          items:
            $ref: '#/definitions/Conversation'
    """
    user_id = get_jwt_identity()
    conversations = get_conversations(user_id)
    return jsonify([c.to_dict() for c in conversations]), 200

@messages_bp.route('/conversations/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_single_conversation(other_user_id):
    """
    Get conversation with another user
    ---
    tags:
      - Messages
    parameters:
      - name: other_user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Conversation messages
        schema:
          type: array
          items:
            $ref: '#/definitions/Message'
      404:
        description: Conversation not found
    """
    user_id = get_jwt_identity()
    try:
        conversation = get_conversation(user_id, other_user_id)
        return jsonify([m.to_dict() for m in conversation]), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)

@messages_bp.route('/conversations/<int:other_user_id>', methods=['POST'])
@jwt_required()
def send_new_message(other_user_id):
    """
    Send a message to another user
    ---
    tags:
      - Messages
    parameters:
      - name: other_user_id
        in: path
        type: integer
        required: true
      - in: body
        name: message
        description: Message content
        schema:
          type: object
          properties:
            content:
              type: string
    responses:
      201:
        description: Message sent
        schema:
          $ref: '#/definitions/Message'
      400:
        description: Invalid input
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')
    
    if not content or len(content.strip()) == 0:
        raise InvalidUsage('Message content is required', status_code=400)
    
    try:
        message = send_message(user_id, other_user_id, content)
        return jsonify(message.to_dict()), 201
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)

@messages_bp.route('/conversations/<int:other_user_id>/read', methods=['POST'])
@jwt_required()
def mark_conversation_read(other_user_id):
    """
    Mark conversation as read
    ---
    tags:
      - Messages
    parameters:
      - name: other_user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Messages marked as read
      404:
        description: Conversation not found
    """
    user_id = get_jwt_identity()
    try:
        mark_as_read(user_id, other_user_id)
        return jsonify({'message': 'Messages marked as read'}), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)