from bson import ObjectId
from datetime import datetime

def get_mongo():
    """获取 mongo 实例"""
    from main import mongo
    return mongo

class User:
    """用户模型"""
    
    @staticmethod
    def create(username, email, password_hash):
        """创建用户"""
        mongo = get_mongo()
        user_data = {
            'username': username,
            'email': email,
            'password': password_hash,
            'avatar': 'https://via.placeholder.com/150',
            'bio': '',
            'favorite_characters': [],
            'followers': [],
            'following': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(email):
        """通过邮箱查找用户"""
        mongo = get_mongo()
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_username(username):
        """通过用户名查找用户"""
        mongo = get_mongo()
        return mongo.db.users.find_one({'username': username})
    
    @staticmethod
    def find_by_id(user_id):
        """通过 ID 查找用户"""
        mongo = get_mongo()
        try:
            return mongo.db.users.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    @staticmethod
    def update(user_id, update_data):
        """更新用户信息"""
        mongo = get_mongo()
        update_data['updated_at'] = datetime.utcnow()
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def add_follower(user_id, follower_id):
        """添加粉丝"""
        mongo = get_mongo()
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'followers': ObjectId(follower_id)}}
        )
    
    @staticmethod
    def add_following(user_id, following_id):
        """添加关注"""
        mongo = get_mongo()
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'following': ObjectId(following_id)}}
        )
    
    @staticmethod
    def remove_follower(user_id, follower_id):
        """移除粉丝"""
        mongo = get_mongo()
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$pull': {'followers': ObjectId(follower_id)}}
        )
    
    @staticmethod
    def remove_following(user_id, following_id):
        """移除关注"""
        mongo = get_mongo()
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$pull': {'following': ObjectId(following_id)}}
        )