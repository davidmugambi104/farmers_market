from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from services.exceptions import AuthError
from backend.models import User
def farmer_required(fn):
    """Decorator to require farmer role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'farmer':
            raise AuthError('Farmer access required')
        
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            raise AuthError('Admin access required')
        
        return fn(*args, **kwargs)
    return wrapper