# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # 从环境变量加载数据库连接字符串
    JWT_SECRET_KEY: str  # 从环境变量加载 JWT 密钥
    JWT_ALGORITHM: str  # JWT 签名算法
    JWT_EXPIRE_MINUTES: int  # JWT 过期时间（分钟）
    REDIS_HOST: str  # Redis 主机
    REDIS_PORT: int  # Redis 端口
    REDIS_DB: int  # Redis 数据库

    # SMS配置
    SMS_API_URL: str  # Redis 数据库
    SMS_API_KEY: str  # Redis 数据库

    # 白名单路径配置
    WHITE_LIST_PATHS: list = [
        "/api/v1/auth/send-code",  # 发送短信
        "/api/v1/auth/login",  # 登录接口
        "/api/v1/user-guide/.*",  
        "/docs",  
        "/openapi.json",  
    ]

    # 新增模型相关配置
    MODEL_BASE_URL: str = ""
    MODEL_API_KEY: str = ""
    MODEL_NAME: str = ""

    class Config:
        env_file = ".env"  # 指定 .env 文件路径

# 创建配置实例
settings = Settings()
