from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models.user import User
from models.post import Post
from . import users_bp

def serialize_user(user):
    """序列化用户"""
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'avatar': user['avatar'],
        'bio': user.get('bio', ''),
        'favoriteCharacters': user.get('favorite_characters', []),
        'followersCount': len(user.get('followers', [])),
        'followingCount': len(user.get('following', []))
    }

def serialize_post(post):
    """序列化帖子"""
    author = User.find_by_id(str(post['author']))
    return {
        'id': str(post['_id']),
        'title': post['title'],
        'content': post['content'],
        'type': post['type'],
        'images': post.get('images', []),
        'characters': post.get('characters', []),
        'likeCount': post.get('like_count', 0),
        'commentCount': post.get('comment_count', 0),
        'author': {
            'id': str(author['_id']),
            'username': author['username'],
            'avatar': author['avatar']
        } if author else None,
        'createdAt': post['created_at'].isoformat() if post.get('created_at') else None
    }

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户资料"""
    user = User.find_by_id(user_id)
    if not user:
        return {'message': '用户不存在'}, 404
    
    return {'user': serialize_user(user)}, 200

@users_bp.route('/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """获取用户的��有帖子"""
    page = request.args.get('page', 1, type=int)
    posts = Post.find_by_author(user_id, page)
    
    return {'posts': [serialize_post(p) for p in posts]}, 200

@users_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新个人资料"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    update_data = {}
    if 'bio' in data:
        update_data['bio'] = data['bio']
    if 'avatar' in data:
        update_data['avatar'] = data['avatar']
    if 'favoriteCharacters' in data:
        update_data['favorite_characters'] = data['favoriteCharacters']
    
    User.update(user_id, update_data)
    user = User.find_by_id(user_id)
    
    return {'message': '更新成功', 'user': serialize_user(user)}, 200

@users_bp.route('/<user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    """关注用户"""
    current_user_id = get_jwt_identity()
    
    if current_user_id == user_id:
        return {'message': '不能关注自己'}, 400
    
    User.add_following(current_user_id, user_id)
    User.add_follower(user_id, current_user_id)
    
    return {'message': '关注成功'}, 200

@users_bp.route('/<user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    """取消关注"""
    current_user_id = get_jwt_identity()
    
    User.remove_following(current_user_id, user_id)
    User.remove_follower(user_id, current_user_id)
    
    return {'message': '取消关注成功'}, 200