from flask import request, jsonify
from flask_jwt_extended import create_access_token
from bcrypt import hashpw, gensalt, checkpw
from models.user import User
from . import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return {'message': '缺少必要字段'}, 400
    
    # 检查用户是否已存在
    if User.find_by_email(data['email']) or User.find_by_username(data['username']):
        return {'message': '用户已存在'}, 400
    
    # 密码加密
    password_hash = hashpw(data['password'].encode('utf-8'), gensalt())
    
    # 创建用户
    user_id = User.create(data['username'], data['email'], password_hash)
    user = User.find_by_id(user_id)
    
    # 生成 JWT
    access_token = create_access_token(identity=str(user['_id']))
    
    return {
        'message': '注册成功',
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'avatar': user['avatar']
        }
    }, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return {'message': '缺少必要字段'}, 400
    
    user = User.find_by_email(data['email'])
    if not user or not checkpw(data['password'].encode('utf-8'), user['password']):
        return {'message': '邮箱或密码错误'}, 401
    
    # 生成 JWT
    access_token = create_access_token(identity=str(user['_id']))
    
    return {
        'message': '登录成功',
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'avatar': user['avatar']
        }
    }, 200