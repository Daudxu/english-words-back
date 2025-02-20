from pydantic import BaseModel
from typing import Optional

# 定义用户信息响应模型
class UserResponse(BaseModel):
    user_id: Optional[int] = None  # 用户ID, 可以为空，适用于某些场景
    name: str  # 用户名称
    phone: str  # 用户手机号
    vip_start_time: int  # VIP开始时间（时间戳）
    vip_end_time: int  # VIP结束时间（时间戳）

    class Config:
        from_attributes = True  # 允许从ORM模型直接转换

# 定义通用响应模型
class CommonResponse(BaseModel):
    status: int  # 状态码
    message: str  # 消息
    data: Optional[UserResponse] = None  # 数据部分，可能为空

