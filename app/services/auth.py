# app/services/auth.py

from datetime import datetime, timedelta, UTC
from jose import jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models.user import User
from app.schemas.auth import LoginResponse, CommonResponse
from app.utils.sms import send_sms
import random
from app.utils.response import success_response, error_response
import redis

# 初始化 Redis 连接
redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB
)

class AuthService:
    @staticmethod
    async def send_verification_code(phone: str):
        existing_code = redis_client.get(phone)
        if existing_code:
            return error_response(400, "验证码已发送。请等待一分钟。")
        code = random.randint(100000, 999999)
        code_str = str(code)

        try:
            redis_client.setex(phone, 60, code)
            return send_sms(phone, code_str)
        except Exception as e:
            return error_response(500, str(e))

    @staticmethod
    async def verify_code_and_login(db: Session, phone: str, code: str) -> CommonResponse[LoginResponse]:
        stored_code = redis_client.get(phone)
        if stored_code is None or stored_code.decode('utf-8') != code:
            # 如果验证码错误，返回统一结构的错误信息
            return CommonResponse(status=400, message="验证码不正确", data=None)

        # 查询用户
        user = db.query(User).filter(User.phone == phone).first()
        if not user:
            # 如果用户不存在，可以自动创建用户
            user = User(phone=phone)
            # 设置 VIP 相关时间
            current_time = int(datetime.utcnow().timestamp())  # 当前时间戳
            vip_end_time = current_time + (2 * 24 * 60 * 60)  # 当前时间 + 2天（单位秒）

            user.vip_start_time = current_time
            user.vip_end_time = vip_end_time

            db.add(user)
            db.commit()
            db.refresh(user)

        # 生成 JWT Token
        token = AuthService.create_jwt_token(user.id)

        # 登录成功后，从 Redis 中删除验证码
        redis_client.delete(phone)

        # 构建 LoginResponse 实例
        login_response = LoginResponse(
            user_id=user.id,
            phone=user.phone,
            token=token
        )

        # 返回成功的 CommonResponse，包含 LoginResponse
        return CommonResponse(status=200, message="Login successful", data=login_response)

    @staticmethod
    def create_jwt_token(user_id: int) -> str:
        # 生成 JWT Token
        print(settings.JWT_EXPIRE_MINUTES)
        print(settings.JWT_SECRET_KEY)
        print(settings.JWT_ALGORITHM)
        print(user_id)
        expire = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),  # 用户ID
            "exp": int((datetime.now(UTC) + expire).timestamp())  # 生成标准的 Unix 时间戳（秒）
        }
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
   