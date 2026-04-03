from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config, DevelopmentConfig
import os

# 初始化扩展
mongo = PyMongo()
jwt = JWTManager()

def create_app(config_class=None):
    """创建 Flask 应用工厂"""
    if config_class is None:
        config_class = DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else Config
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    CORS(app)
    mongo.init_app(app)
    jwt.init_app(app)
    
    # 注册蓝图
    from routes import auth_bp, posts_bp, users_bp, comments_bp, messages_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(messages_bp)
    
    # 错误处理
    @app.errorhandler(400)
    def bad_request(error):
        return {'message': '请求错误'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'message': '未授权'}, 401
    
    @app.errorhandler(404)
    def not_found(error):
        return {'message': '资源不存在'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'message': '服务器错误'}, 500
    
    return app