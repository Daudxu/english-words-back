from pydantic import BaseModel

class PhoneRequest(BaseModel):
    phone: str  # 手机号

class LoginRequest(BaseModel):
    phone: str  # 手机号
    code: str   # 验证码

class LoginResponse(BaseModel):
    user_id: int
    phone: str
    token: str  # 登录成功后返回的 JWT Token