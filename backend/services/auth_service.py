from models import User, db
from services.exceptions import AuthError

def register_user(data):
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        raise AuthError('Username already exists')
    if User.query.filter_by(email=data['email']).first():
        raise AuthError('Email already exists')
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # Password setter handles hashing
        farm_name=data.get('farm_name', '')
    )
    
    db.session.add(user)
    db.session.commit()
    return user

def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        raise AuthError('Invalid email or password')
    
    return user

def get_current_user(user_id):
    return User.query.get(user_id)