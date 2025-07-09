def validate_product_data(data, update=False):
    """Validate product data"""
    errors = {}
    
    if not update or 'name' in data:
        if not data.get('name') or len(data['name']) < 3:
            errors['name'] = 'Name must be at least 3 characters'
    
    if not update or 'price' in data:
        price = data.get('price')
        if price is None:
            errors['price'] = 'Price is required'
        elif not isinstance(price, (int, float)) or price <= 0:
            errors['price'] = 'Price must be a positive number'
    
    if not update or 'stock_quantity' in data:
        stock = data.get('stock_quantity')
        if stock is None:
            errors['stock_quantity'] = 'Stock quantity is required'
        elif not isinstance(stock, int) or stock < 0:
            errors['stock_quantity'] = 'Stock must be a non-negative integer'
    
    if not update or 'category' in data:
        if not data.get('category'):
            errors['category'] = 'Category is required'
    
    if not update or 'unit' in data:
        if not data.get('unit'):
            errors['unit'] = 'Unit is required'
    
    return errors

def validate_order_data(data):
    """Validate order data"""
    errors = {}
    
    items = data.get('items')
    if not items or not isinstance(items, list) or len(items) == 0:
        errors['items'] = 'At least one order item is required'
    else:
        for i, item in enumerate(items):
            if not item.get('product_id'):
                errors[f'items.{i}.product_id'] = 'Product ID is required'
            if not item.get('quantity') or item['quantity'] <= 0:
                errors[f'items.{i}.quantity'] = 'Quantity must be positive integer'
    
    return errors

def validate_password_change(data):
    """Validate password change data"""
    errors = {}
    
    if not data.get('current_password'):
        errors['current_password'] = 'Current password is required'
    
    new_password = data.get('new_password')
    if not new_password:
        errors['new_password'] = 'New password is required'
    elif len(new_password) < 8:
        errors['new_password'] = 'Password must be at least 8 characters'
    
    confirm_password = data.get('confirm_password')
    if not confirm_password:
        errors['confirm_password'] = 'Confirm password is required'
    elif new_password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match'
    
    return errors
# utils/validators.py

def validate_user_registration(data):
    """Validate user registration data"""
    errors = {}

    if not data.get('username') or len(data['username'].strip()) < 3:
        errors['username'] = 'Username must be at least 3 characters.'

    if not data.get('email'):
        errors['email'] = 'Email is required.'
    elif '@' not in data['email']:  # You can improve this with regex
        errors['email'] = 'Invalid email format.'

    password = data.get('password')
    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters.'

    confirm_password = data.get('confirm_password')
    if not confirm_password:
        errors['confirm_password'] = 'Confirm password is required.'
    elif password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    return errors
def validate_user_login(data):
    """Validate user login data"""
    errors = {}

    if not data.get('email'):
        errors['email'] = 'Email is required.'
    elif '@' not in data['email']:  # Basic format check
        errors['email'] = 'Invalid email format.'

    if not data.get('password'):
        errors['password'] = 'Password is required.'

    return errors


# Export the validation functions for use in other modules
__all__ = [
    'validate_product_data',
    'validate_order_data',
    'validate_password_change',
    'validate_user_registration',
    'validate_user_login'
]

