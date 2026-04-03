from bson import ObjectId
from datetime import datetime

def get_mongo():
    """获取 mongo 实例"""
    from main import mongo
    return mongo

class Comment:
    """评论模型"""
    
    @staticmethod
    def create(post_id, author_id, content):
        """创建评论"""
        mongo = get_mongo()
        comment_data = {
            'post': ObjectId(post_id),
            'author': ObjectId(author_id),
            'content': content,
            'likes': [],
            'created_at': datetime.utcnow()
        }
        result = mongo.db.comments.insert_one(comment_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(comment_id):
        """查找评论"""
        mongo = get_mongo()
        try:
            return mongo.db.comments.find_one({'_id': ObjectId(comment_id)})
        except:
            return None
    
    @staticmethod
    def find_by_post(post_id):
        """获取帖子的所有评论"""
        mongo = get_mongo()
        return list(mongo.db.comments.find({'post': ObjectId(post_id)}).sort('created_at', -1))
    
    @staticmethod
    def delete(comment_id):
        """删除评论"""
        mongo = get_mongo()
        mongo.db.comments.delete_one({'_id': ObjectId(comment_id)})
    
    @staticmethod
    def add_like(comment_id, user_id):
        """评论点赞"""
        mongo = get_mongo()
        mongo.db.comments.update_one(
            {'_id': ObjectId(comment_id)},
            {'$addToSet': {'likes': ObjectId(user_id)}}
        )
    
    @staticmethod
    def remove_like(comment_id, user_id):
        """评论取消点赞"""
        mongo = get_mongo()
        mongo.db.comments.update_one(
            {'_id': ObjectId(comment_id)},
            {'$pull': {'likes': ObjectId(user_id)}}
        )