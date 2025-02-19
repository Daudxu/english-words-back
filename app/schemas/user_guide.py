# app/schemas/user_guide.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from enum import Enum

# 定义枚举类型
class UserGuideType(Enum):
    privacy_policy = "privacy_policy"
    user_agreement = "user_agreement"
    contact_info = "contact_info"

# 定义泛型类型变量 T
T = TypeVar('T')

# 用户指南请求模型
class UserGuideRequest(BaseModel):
    type: UserGuideType  # 使用枚举类型
    title: Optional[str]  # 标题字段，部分类型可能没有标题
    content: str  # 具体内容字段，必填

    class Config:
        orm_mode = True

# 用户指南响应模型
class UserGuideResponse(BaseModel):
    title: Optional[str]  # 用户指南的标题，可能为空
    content: str  # 用户指南的内容，必填

    class Config:
        orm_mode = True

# 通用响应模型，返回 UserGuideResponse 或其他类型的响应
class CommonResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None
