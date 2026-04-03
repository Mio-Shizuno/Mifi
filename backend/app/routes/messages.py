from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models.message import Message
from models.user import User
from . import messages_bp

def serialize_message(message):
    """序列化消息"""
    sender = User.find_by_id(str(message['sender']))
    recipient = User.find_by_id(str(message['recipient']))
    
    return {
        'id': str(message['_id']),
        'content': message['content'],
        'isRead': message.get('is_read', False),
        'sender': {
            'id': str(sender['_id']),
            'username': sender['username'],
            'avatar': sender['avatar']
        } if sender else None,
        'recipient': {
            'id': str(recipient['_id']),
            'username': recipient['username'],
            'avatar': recipient['avatar']
        } if recipient else None,
        'createdAt': message['created_at'].isoformat() if message.get('created_at') else None
    }

@messages_bp.route('/', methods=['POST'])
@jwt_required()
def send_message():
    """发送私信"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('recipientId') or not data.get('content'):
        return {'message': '缺少必要字段'}, 400
    
    recipient = User.find_by_id(data['recipientId'])
    if not recipient:
        return {'message': '接收者不存在'}, 404
    
    message_id = Message.create(user_id, data['recipientId'], data['content'])
    message = Message.find_conversation(user_id, data['recipientId'])[-1]
    
    return {'message': '发送成功', 'data': serialize_message(message)}, 201

@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """获取会话列表"""
    user_id = get_jwt_identity()
    conversations = Message.find_conversations(user_id)
    return {'conversations': conversations}, 200

@messages_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_messages(user_id):
    """获取与特定用户的消息"""
    current_user_id = get_jwt_identity()
    messages = Message.find_conversation(current_user_id, user_id)
    Message.mark_as_read(current_user_id, user_id)
    
    return {'messages': [serialize_message(m) for m in messages]}, 200