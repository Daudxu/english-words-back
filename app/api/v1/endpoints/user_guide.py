# app/api/v1/endpoints/user_guide.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_guide import UserGuideService
from app.db.session import get_db  # 获取数据库会话的依赖
from app.schemas.user_guide import UserGuideResponse, CommonResponse

router = APIRouter()

@router.get("/{type}", response_model=CommonResponse[UserGuideResponse])
async def get_user_guide(type: str, db: Session = Depends(get_db)):
    # 验证type是否合法
    if type not in ['privacy_policy', 'user_agreement', 'contact_info', 'complaint', 'about']:
        # 直接返回带有错误状态的CommonResponse
        return CommonResponse(status=400, message="Invalid type provided", data=None)

    # 获取用户指南内容
    user_guide = UserGuideService.get_user_guide(db, type)

    if not user_guide:
        # 直接返回带有错误状态的CommonResponse
        return CommonResponse(status=404, message=f"{type} not found", data=None)

    # 如果查询成功，返回包含数据的CommonResponse
    return CommonResponse(status=200, message="Success", data=user_guide)
