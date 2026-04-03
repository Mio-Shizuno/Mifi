from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models.comment import Comment
from models.post import Post
from models.user import User
from . import comments_bp

def serialize_comment(comment):
    """序列化评论"""
    author = User.find_by_id(str(comment['author']))
    return {
        'id': str(comment['_id']),
        'content': comment['content'],
        'author': {
            'id': str(author['_id']),
            'username': author['username'],
            'avatar': author['avatar']
        } if author else None,
        'createdAt': comment['created_at'].isoformat() if comment.get('created_at') else None
    }

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    """创建评论"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('postId') or not data.get('content'):
        return {'message': '缺少必要字段'}, 400
    
    post = Post.find_by_id(data['postId'])
    if not post:
        return {'message': '帖子不存在'}, 404
    
    comment_id = Comment.create(data['postId'], user_id, data['content'])
    Post.add_comment(data['postId'], comment_id)
    
    comment = Comment.find_by_id(comment_id)
    return {'message': '评论成功', 'comment': serialize_comment(comment)}, 201

@comments_bp.route('/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """删除评论"""
    user_id = get_jwt_identity()
    comment = Comment.find_by_id(comment_id)
    
    if not comment:
        return {'message': '评论不存在'}, 404
    
    if str(comment['author']) != user_id:
        return {'message': '无权限删除'}, 401
    
    post_id = comment['post']
    Comment.delete(comment_id)
    Post.remove_comment(str(post_id), comment_id)
    
    return {'message': '删除成功'}, 200