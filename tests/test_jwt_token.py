from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError

# 密钥，实际使用时建议从配置文件中读取
SECRET_KEY = 'qweqweqwe'
# 加密算法
ALGORITHM = 'HS256'

def create_jwt_token(user_id: int) -> str:
    # 设置过期时间
    expire = timedelta(minutes=600)
    # 当前时间 + 过期时间
    to_encode = {
        "sub": str(user_id),  # 用户ID
        "exp": int((datetime.now(UTC) + expire).timestamp())  # 生成标准的 Unix 时间戳（秒）
    }
    # 使用密钥对内容进行加密
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        # 尝试解密令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从解密后的负载中提取用户 ID
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError("用户 ID 未找到")
        return user_id
    except JWTError as e:
        # 捕获 JWT 解密过程中的异常
        print(f"JWT 解密失败: {e}")
        return None

# 示例：创建令牌
token = create_jwt_token(2)
print("生成的 JWT 令牌:", token)

# 示例：解密令牌
decoded_user_id = decode_jwt_token(token)
if decoded_user_id:
    print("解密后得到的用户 ID:", decoded_user_id)