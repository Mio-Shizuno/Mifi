import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mifi')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # 服务器
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/mifi_test'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    