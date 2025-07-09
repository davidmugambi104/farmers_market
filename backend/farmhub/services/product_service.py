from models import Product, db
from services.exceptions import NotFoundError

def get_products(farmer_id):
    """Get all products for a farmer"""
    return Product.query.filter_by(farmer_id=farmer_id).all()

def create_product(farmer_id, data):
    """Create a new product"""
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        category=data['category'],
        stock_quantity=data['stock_quantity'],
        unit=data['unit'],
        farmer_id=farmer_id,
        image_url=data.get('image_url', '')
    )
    db.session.add(product)
    db.session.commit()
    return product

def get_product(farmer_id, product_id):
    """Get a single product by ID"""
    product = Product.query.filter_by(id=product_id, farmer_id=farmer_id).first()
    if not product:
        raise NotFoundError('Product not found')
    return product

def update_product(farmer_id, product_id, data):
    """Update an existing product"""
    product = get_product(farmer_id, product_id)
    
    # Update fields
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.unit = data.get('unit', product.unit)
    product.image_url = data.get('image_url', product.image_url)
    
    db.session.commit()
    return product

def delete_product(farmer_id, product_id):
    """Delete a product"""
    product = get_product(farmer_id, product_id)
    db.session.delete(product)
    db.session.commit()