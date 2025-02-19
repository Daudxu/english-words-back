# app/main.py
from fastapi import FastAPI
from app.api.v1.routers import api_router
from app.middleware.jwt_middleware import JWTMiddleware  # 导入中间件

# 创建 FastAPI 应用
app = FastAPI(title="App")

# 将 JWT 校验中间件添加到 FastAPI 应用中
app.add_middleware(JWTMiddleware)

# 将 api_router 添加到应用中，并设置 API 路由前缀
app.include_router(api_router, prefix="/api/v1")

# 打印所有路由，检查是否注册成功
for route in app.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")

# 如果你运行应用，使用以下命令启动：
# uvicorn app.main:app --reload