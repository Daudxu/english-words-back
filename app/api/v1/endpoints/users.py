from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import CommonResponse, UserResponse  # 引入UserResponse和CommonResponse

router = APIRouter()

# 获取当前用户信息
@router.get("/me", response_model=CommonResponse)
async def get_user_info(
    request: Request, 
    db: Session = Depends(get_db)
):
    # 从中间件注入的request.state获取user_id
    user_id = getattr(request.state, "user_id", None)
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="用户未认证"
        )
    
    # 查询数据库获取用户信息
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    # 构建 UserResponse 实例
    user_data = UserResponse(
        user_id=user.id,
        name=user.name,
        phone=user.phone,
        vip_start_time=user.vip_start_time or 0,
        vip_end_time=user.vip_end_time or 0
    )

    # 返回 CommonResponse，包含 UserResponse
    return CommonResponse(
        status=200,
        message="获取用户信息成功",
        data=user_data
    )
