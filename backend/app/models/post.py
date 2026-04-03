from bson import ObjectId
from datetime import datetime

def get_mongo():
    """获取 mongo 实例"""
    from main import mongo
    return mongo

class Post:
    """帖子模型"""
    
    @staticmethod
    def create(author_id, title, content, post_type, images=None, characters=None):
        """创建帖子"""
        mongo = get_mongo()
        post_data = {
            'author': ObjectId(author_id),
            'title': title,
            'content': content,
            'type': post_type,
            'images': images or [],
            'characters': characters or [],
            'likes': [],
            'comments': [],
            'like_count': 0,
            'comment_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = mongo.db.posts.insert_one(post_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(post_id):
        """查找单个帖子"""
        mongo = get_mongo()
        try:
            return mongo.db.posts.find_one({'_id': ObjectId(post_id)})
        except:
            return None
    
    @staticmethod
    def find_all(page=1, limit=10):
        """获取所有帖子（分页）"""
        mongo = get_mongo()
        skip = (page - 1) * limit
        posts = list(mongo.db.posts.find().sort('created_at', -1).skip(skip).limit(limit))
        return posts
    
    @staticmethod
    def find_by_author(author_id, page=1, limit=10):
        """获取特定用户的帖子"""
        mongo = get_mongo()
        skip = (page - 1) * limit
        posts = list(mongo.db.posts.find({'author': ObjectId(author_id)}).sort('created_at', -1).skip(skip).limit(limit))
        return posts
    
    @staticmethod
    def update(post_id, update_data):
        """更新帖子"""
        mongo = get_mongo()
        update_data['updated_at'] = datetime.utcnow()
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def delete(post_id):
        """删除帖子"""
        mongo = get_mongo()
        mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
    
    @staticmethod
    def add_like(post_id, user_id):
        """添加点赞"""
        mongo = get_mongo()
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$addToSet': {'likes': ObjectId(user_id)}, '$inc': {'like_count': 1}}
        )
    
    @staticmethod
    def remove_like(post_id, user_id):
        """移除点赞"""
        mongo = get_mongo()
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$pull': {'likes': ObjectId(user_id)}, '$inc': {'like_count': -1}}
        )
    
    @staticmethod
    def add_comment(post_id, comment_id):
        """添加评论"""
        mongo = get_mongo()
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$push': {'comments': ObjectId(comment_id)}, '$inc': {'comment_count': 1}}
        )
    
    @staticmethod
    def remove_comment(post_id, comment_id):
        """移除评论"""
        mongo = get_mongo()
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$pull': {'comments': ObjectId(comment_id)}, '$inc': {'comment_count': -1}}
        )