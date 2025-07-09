from datetime import datetime
import random
from models import Order, OrderItem, db, Product
from services.exceptions import NotFoundError, InvalidOperation

def get_orders(user_id):
    """Get all orders for a user"""
    return Order.query.filter_by(customer_id=user_id).all()

def create_order(customer_id, data):
    """Create a new order"""
    # Generate unique order number
    order_number = f"FARM-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    # Calculate total amount and validate products
    total = 0
    items = []
    
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            raise NotFoundError(f"Product {item['product_id']} not found")
        
        if product.stock_quantity < item['quantity']:
            raise InvalidOperation(f"Not enough stock for product {product.name}")
        
        total += product.price * item['quantity']
        
        # Create order item
        order_item = OrderItem(
            product_id=product.id,
            quantity=item['quantity'],
            unit_price=product.price
        )
        items.append(order_item)
        
        # Update stock
        product.stock_quantity -= item['quantity']
    
    # Create order
    order = Order(
        order_number=order_number,
        customer_id=customer_id,
        total_amount=total,
        items=items
    )
    
    db.session.add(order)
    db.session.commit()
    return order

def get_order(user_id, order_id):
    """Get a single order by ID"""
    order = Order.query.filter_by(id=order_id, customer_id=user_id).first()
    if not order:
        raise NotFoundError('Order not found')
    return order

def update_order_status(user_id, order_id, status):
    """Update order status"""
    order = get_order(user_id, order_id)
    
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if status not in valid_statuses:
        raise InvalidOperation(f"Invalid status: {status}")
    
    order.status = status
    db.session.commit()
    return order