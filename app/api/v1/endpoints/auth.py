from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import PhoneRequest, LoginRequest, LoginResponse, CommonResponse
from app.services.auth import AuthService
from app.db.session import get_db
import redis
from app.core.config import settings  # 假设 Redis 配置在这个文件中
from app.utils.response import error_response
import re

router = APIRouter()

# 初始化 Redis 连接
redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB
)

def is_valid_phone(phone):
    pattern = re.compile(r'^1[3-9]\d{9}$')
    return bool(pattern.match(phone))

@router.post("/send-code")
async def send_code(request: PhoneRequest):
    if not request.phone:
        return error_response(400, "请输入手机号！")

    # 验证是否为合法手机号
    if not is_valid_phone(request.phone):
        return error_response(400, "请输入正确的手机号！")

    return await AuthService.send_verification_code(request.phone)
 
@router.post("/login", response_model=CommonResponse[LoginResponse])
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return await AuthService.verify_code_and_login(db, request.phone, request.code)
