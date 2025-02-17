from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库连接字符串
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/app"
    
    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key"  # 用于签名 JWT 的密钥
    JWT_ALGORITHM: str = "HS256"            # JWT 签名算法
    JWT_EXPIRE_MINUTES: int = 30            # Token 过期时间（分钟）

    # 新增 Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

# 创建配置实例
settings = Settings()