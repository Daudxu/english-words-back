from datetime import timedelta
from jose import jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models.user import User
from app.schemas.auth import LoginResponse
from app.utils.sms import send_sms

class AuthService:
    @staticmethod
    async def send_verification_code(db: Session, phone: str):
        # 调用短信 SDK 发送验证码
        code = "123456"  # 模拟生成验证码
        await send_sms(phone, f"Your verification code is: {code}")

    @staticmethod
    async def verify_code_and_login(db: Session, phone: str, code: str) -> LoginResponse:
        # 模拟验证码验证
        if code != "123456":  # 假设验证码是 123456
            return None

        # 查询用户
        user = db.query(User).filter(User.phone == phone).first()
        if not user:
            # 如果用户不存在，可以自动创建用户
            user = User(phone=phone)
            db.add(user)
            db.commit()
            db.refresh(user)

        # 生成 JWT Token
        token = AuthService.create_jwt_token(user.id)
        return LoginResponse(
            user_id=user.id,
            phone=user.phone,
            token=token
        )

    @staticmethod
    def create_jwt_token(user_id: int) -> str:
        # 生成 JWT Token
        expire = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        to_encode = {"sub": str(user_id), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt