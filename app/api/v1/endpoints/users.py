# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Request, Depends, HTTPException
from app.db.session import get_db
from app.db.models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

# 获取当前用户信息
@router.get("/me")
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
    
    return {
        "user_id": user.id,
        "phone": user.phone,
        "name": user.name
    }