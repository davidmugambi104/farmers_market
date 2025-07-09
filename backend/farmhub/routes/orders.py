from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.order_service import (
    get_orders, 
    create_order, 
    get_order, 
    update_order_status
)
from services.exceptions import NotFoundError, InvalidUsage
from utils.validators import validate_order_data

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_all_orders():
    """
    Get all orders for the current user
    ---
    tags:
      - Orders
    responses:
      200:
        description: List of orders
        schema:
          type: array
          items:
            $ref: '#/definitions/Order'
    """
    user_id = get_jwt_identity()
    orders = get_orders(user_id)
    return jsonify([o.to_dict() for o in orders]), 200

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_new_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    parameters:
      - in: body
        name: order
        description: Order data
        schema:
          $ref: '#/definitions/OrderCreate'
    responses:
      201:
        description: Order created
        schema:
          $ref: '#/definitions/Order'
      400:
        description: Invalid input data
    """
    data = request.get_json()
    customer_id = get_jwt_identity()
    
    # Validate input
    errors = validate_order_data(data)
    if errors:
        raise InvalidUsage('Validation failed', status_code=400, payload=errors)
    
    try:
        order = create_order(customer_id, data)
        return jsonify(order.to_dict()), 201
    except Exception as e:
        raise InvalidUsage(str(e), status_code=400)

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_single_order(order_id):
    """
    Get a single order by ID
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Order data
        schema:
          $ref: '#/definitions/Order'
      404:
        description: Order not found
    """
    user_id = get_jwt_identity()
    try:
        order = get_order(user_id, order_id)
        return jsonify(order.to_dict()), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)

@orders_bp.route('/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_order(order_id):
    """
    Update order status
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
      - in: body
        name: status
        description: New status
        schema:
          type: object
          properties:
            status:
              type: string
    responses:
      200:
        description: Updated order
        schema:
          $ref: '#/definitions/Order'
      400:
        description: Invalid status
      404:
        description: Order not found
    """
    data = request.get_json()
    status = data.get('status')
    user_id = get_jwt_identity()
    
    if not status:
        raise InvalidUsage('Status is required', status_code=400)
    
    try:
        order = update_order_status(user_id, order_id, status)
        return jsonify(order.to_dict()), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=400)