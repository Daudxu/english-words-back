from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import PhoneRequest, LoginRequest, LoginResponse
from app.services.auth import AuthService
from app.db.session import get_db

router = APIRouter()

@router.post("/send-code")
async def send_code(request: PhoneRequest, db: Session = Depends(get_db)):
    # 调用短信服务发送验证码
    await AuthService.send_verification_code(db, request.phone)
    return {"message": "Verification code sent"}

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 验证手机号和验证码
    user = await AuthService.verify_code_and_login(db, request.phone, request.code)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid code or phone number")
    return user