from models import Message, db, User
from services.exceptions import NotFoundError
from datetime import datetime

def get_conversations(user_id):
    """Get all conversations for a user"""
    # Get distinct conversation partners
    sent = db.session.query(Message.receiver_id).filter_by(sender_id=user_id).distinct()
    received = db.session.query(Message.sender_id).filter_by(receiver_id=user_id).distinct()
    
    # Combine and get unique user IDs
    user_ids = {r[0] for r in sent} | {r[0] for r in received}
    
    # Get last message for each conversation
    conversations = []
    for partner_id in user_ids:
        last_message = Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == partner_id)) |
            ((Message.sender_id == partner_id) & (Message.receiver_id == user_id))
        ).order_by(Message.created_at.desc()).first()
        
        if last_message:
            partner = User.query.get(partner_id)
            conversations.append({
                'partner': partner,
                'last_message': last_message,
                'unread_count': Message.query.filter_by(
                    sender_id=partner_id, 
                    receiver_id=user_id,
                    read=False
                ).count()
            })
    
    return conversations

def get_conversation(user_id, other_user_id):
    """Get conversation between two users"""
    # Verify other user exists
    if not User.query.get(other_user_id):
        raise NotFoundError('User not found')
    
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.created_at.asc()).all()
    
    return messages

def send_message(sender_id, receiver_id, content):
    """Send a new message"""
    # Verify receiver exists
    if not User.query.get(receiver_id):
        raise NotFoundError('Receiver not found')
    
    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    
    db.session.add(message)
    db.session.commit()
    return message

def mark_as_read(user_id, sender_id):
    """Mark messages as read"""
    Message.query.filter_by(
        sender_id=sender_id,
        receiver_id=user_id,
        read=False
    ).update({'read': True})
    
    db.session.commit()