from models import User, db
from services.exceptions import AuthError

def get_user_settings(user_id):
    """Get user settings"""
    return User.query.get(user_id)

def update_user_settings(user_id, data):
    """Update user settings"""
    user = User.query.get(user_id)
    
    # Update fields
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.farm_name = data.get('farm_name', user.farm_name)
    
    db.session.commit()
    return user

def change_password(user_id, current_password, new_password):
    """Change user password"""
    user = User.query.get(user_id)
    
    if not user.verify_password(current_password):
        raise AuthError('Current password is incorrect')
    
    user.password = new_password
    db.session.commit()
    return user