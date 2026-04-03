from bson import ObjectId
from datetime import datetime

def get_mongo():
    """获取 mongo 实例"""
    from main import mongo
    return mongo

class Message:
    """私信模型"""
    
    @staticmethod
    def create(sender_id, recipient_id, content):
        """创建私信"""
        mongo = get_mongo()
        message_data = {
            'sender': ObjectId(sender_id),
            'recipient': ObjectId(recipient_id),
            'content': content,
            'is_read': False,
            'created_at': datetime.utcnow()
        }
        result = mongo.db.messages.insert_one(message_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_conversation(user_id, other_user_id):
        """获取与某用户的私信会话"""
        mongo = get_mongo()
        return list(mongo.db.messages.find({
            '$or': [
                {'sender': ObjectId(user_id), 'recipient': ObjectId(other_user_id)},
                {'sender': ObjectId(other_user_id), 'recipient': ObjectId(user_id)}
            ]
        }).sort('created_at', 1))
    
    @staticmethod
    def find_conversations(user_id):
        """获取用户的所有会话"""
        mongo = get_mongo()
        return list(mongo.db.messages.aggregate([
            {
                '$match': {
                    '$or': [
                        {'sender': ObjectId(user_id)},
                        {'recipient': ObjectId(user_id)}
                    ]
                }
            },
            {'$sort': {'created_at': -1}},
            {
                '$group': {
                    '_id': {
                        '$cond': [
                            {'$eq': ['$sender', ObjectId(user_id)]},
                            '$recipient',
                            '$sender'
                        ]
                    },
                    'last_message': {'$first': '$content'},
                    'last_time': {'$first': '$created_at'}
                }
            }
        ]))
    
    @staticmethod
    def mark_as_read(user_id, other_user_id):
        """标记消息为已读"""
        mongo = get_mongo()
        mongo.db.messages.update_many(
            {'recipient': ObjectId(user_id), 'sender': ObjectId(other_user_id)},
            {'$set': {'is_read': True}}
        )