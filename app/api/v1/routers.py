# app/api/v1/routers.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, user_guide  # 导入user_guide路由

api_router = APIRouter()

# 将用户相关路由注册到/api/v1/users路径下
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 将认证相关路由注册到/api/v1/auth路径下
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 将用户指南相关路由注册到/api/v1/user-guide路径下
api_router.include_router(user_guide.router, prefix="/user-guide", tags=["user_guide"])
