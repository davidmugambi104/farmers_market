from models import Notification, db
from services.exceptions import NotFoundError
from datetime import datetime

def get_notifications(user_id, limit=20):
    """Get notifications for a user"""
    return Notification.query.filter_by(user_id=user_id).order_by(
        Notification.created_at.desc()
    ).limit(limit).all()

def get_unread_count(user_id):
    """Get count of unread notifications"""
    return Notification.query.filter_by(
        user_id=user_id, 
        read=False
    ).count()

def mark_all_as_read(user_id):
    """Mark all notifications as read"""
    Notification.query.filter_by(
        user_id=user_id,
        read=False
    ).update({'read': True})
    
    db.session.commit()

def mark_as_read(user_id, notification_id):
    """Mark a single notification as read"""
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id
    ).first()
    
    if not notification:
        raise NotFoundError('Notification not found')
    
    notification.read = True
    db.session.commit()
    return notification

def create_notification(user_id, title, content, type='info'):
    """Create a new notification"""
    notification = Notification(
        user_id=user_id,
        title=title,
        content=content,
        type=type
    )
    
    db.session.add(notification)
    db.session.commit()
    return notification