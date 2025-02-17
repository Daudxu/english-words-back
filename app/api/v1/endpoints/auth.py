from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import PhoneRequest, LoginRequest, LoginResponse
from app.services.auth import AuthService
from app.db.session import get_db
import redis
from app.core.config import settings  # 假设 Redis 配置在这个文件中

router = APIRouter()

# 初始化 Redis 连接
redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB
)

@router.post("/send-code")
async def send_code(request: PhoneRequest, db: Session = Depends(get_db)):
    # 调用短信服务发送验证码
    code = "123456"  # 这里假设验证码是固定的，实际应该使用随机生成的验证码
    await AuthService.send_verification_code(db, request.phone)
    
    # 将验证码存储到 Redis 中，设置过期时间为 5 分钟（300 秒）
    redis_client.setex(request.phone, 300, code)
    
    return {"message": "Verification code sent"}

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 从 Redis 中获取验证码
    stored_code = redis_client.get(request.phone)
    
    if stored_code is None:
        print("Verification code expired or not found - login failed")
        raise HTTPException(status_code=400, detail="Verification code expired or not found")
    
    # 验证手机号和验证码
    if request.code != stored_code.decode('utf-8'):
        print("Invalid code or phone number - login failed")
        raise HTTPException(status_code=400, detail="Invalid code or phone number")
    
    # 验证码验证通过后，进行登录操作
    user = await AuthService.verify_code_and_login(db, request.phone, request.code)
    if not user:
        print("User not found - login failed")
        raise HTTPException(status_code=400, detail="Invalid code or phone number")
    
    # 登录成功后，从 Redis 中删除验证码
    redis_client.delete(request.phone)
    
    return user