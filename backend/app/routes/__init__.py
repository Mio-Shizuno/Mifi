from flask import Blueprint

# 蓝图初始化
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')
users_bp = Blueprint('users', __name__, url_prefix='/api/users')
comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')
messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages')

# 导入路由
from . import auth, posts, users, comments, messages