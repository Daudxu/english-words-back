from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class PhoneRequest(BaseModel):
    phone: str  

class LoginRequest(BaseModel):
    phone: str  
    code: str   

class LoginResponse(BaseModel):
    user_id: Optional[T] = None
    phone: str
    token: str  

class CommonResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None