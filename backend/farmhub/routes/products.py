from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.product_service import (
    get_products, 
    create_product, 
    get_product, 
    update_product, 
    delete_product
)
from services.exceptions import NotFoundError, InvalidUsage
from utils.validators import validate_product_data
from utils.security import farmer_required

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
@jwt_required()
def get_all_products():
    """
    Get all products for the current farmer
    ---
    tags:
      - Products
    responses:
      200:
        description: List of products
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
    """
    farmer_id = get_jwt_identity()
    products = get_products(farmer_id)
    return jsonify([p.to_dict() for p in products]), 200

@products_bp.route('', methods=['POST'])
@jwt_required()
@farmer_required
def add_product():
    """
    Create a new product
    ---
    tags:
      - Products
    parameters:
      - in: body
        name: product
        description: Product data
        schema:
          $ref: '#/definitions/ProductCreate'
    responses:
      201:
        description: Product created
        schema:
          $ref: '#/definitions/Product'
      400:
        description: Invalid input data
    """
    data = request.get_json()
    farmer_id = get_jwt_identity()
    
    # Validate input
    errors = validate_product_data(data)
    if errors:
        raise InvalidUsage('Validation failed', status_code=400, payload=errors)
    
    try:
        product = create_product(farmer_id, data)
        return jsonify(product.to_dict()), 201
    except Exception as e:
        raise InvalidUsage(str(e), status_code=400)

@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_single_product(product_id):
    """
    Get a single product by ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Product data
        schema:
          $ref: '#/definitions/Product'
      404:
        description: Product not found
    """
    farmer_id = get_jwt_identity()
    try:
        product = get_product(farmer_id, product_id)
        return jsonify(product.to_dict()), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@farmer_required
def update_single_product(product_id):
    """
    Update a product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
      - in: body
        name: product
        description: Updated product data
        schema:
          $ref: '#/definitions/ProductUpdate'
    responses:
      200:
        description: Updated product
        schema:
          $ref: '#/definitions/Product'
      400:
        description: Invalid input data
      404:
        description: Product not found
    """
    data = request.get_json()
    farmer_id = get_jwt_identity()
    
    # Validate input
    errors = validate_product_data(data, update=True)
    if errors:
        raise InvalidUsage('Validation failed', status_code=400, payload=errors)
    
    try:
        product = update_product(farmer_id, product_id, data)
        return jsonify(product.to_dict()), 200
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=400)

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@farmer_required
def delete_single_product(product_id):
    """
    Delete a product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Product deleted
      404:
        description: Product not found
    """
    farmer_id = get_jwt_identity()
    try:
        delete_product(farmer_id, product_id)
        return '', 204
    except NotFoundError as e:
        raise InvalidUsage(str(e), status_code=404)