from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models.post import Post
from models.user import User
from . import posts_bp

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

@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    """创建帖子"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('title') or not data.get('content'):
        return {'message': '缺少必要字段'}, 400
    
    post_id = Post.create(
        user_id,
        data['title'],
        data['content'],
        data.get('type', 'text'),
        data.get('images'),
        data.get('characters')
    )
    
    post = Post.find_by_id(post_id)
    return {'message': '创建成功', 'post': serialize_post(post)}, 201

@posts_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    """获取推流"""
    page = request.args.get('page', 1, type=int)
    posts = Post.find_all(page)
    
    return {'posts': [serialize_post(p) for p in posts]}, 200

@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """获取单个帖子"""
    post = Post.find_by_id(post_id)
    if not post:
        return {'message': '帖子不存在'}, 404
    
    return {'post': serialize_post(post)}, 200

@posts_bp.route('/<post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """更新帖子"""
    user_id = get_jwt_identity()
    post = Post.find_by_id(post_id)
    
    if not post:
        return {'message': '帖子不存在'}, 404
    
    if str(post['author']) != user_id:
        return {'message': '无权限更新'}, 401
    
    data = request.get_json()
    Post.update(post_id, data)
    post = Post.find_by_id(post_id)
    
    return {'message': '更新成功', 'post': serialize_post(post)}, 200

@posts_bp.route('/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """删除帖子"""
    user_id = get_jwt_identity()
    post = Post.find_by_id(post_id)
    
    if not post:
        return {'message': '帖子不存在'}, 404
    
    if str(post['author']) != user_id:
        return {'message': '无权限删除'}, 401
    
    Post.delete(post_id)
    return {'message': '删除成功'}, 200