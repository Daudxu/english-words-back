# app/main.py
from fastapi import FastAPI
from app.api.v1.routers import api_router
from app.middleware.jwt_middleware import JWTMiddleware  # 导入中间件
from fastapi.middleware.cors import CORSMiddleware

# 创建 FastAPI 应用
app = FastAPI(title="App")

# 添加 CORS 中间件

# 配置 CORS 中间件
origins = [
    # "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # 允许的来源列表
    allow_origins=["*"],  # 允许的来源列表
    allow_credentials=True,  # 是否允许发送 Cookie
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 明确列出允许的方法
    allow_headers=["Content-Type", "Authorization"],      # 允许所有的请求头
)


# 将 JWT 校验中间件添加到 FastAPI 应用中
app.add_middleware(JWTMiddleware)

# 将 api_router 添加到应用中，并设置 API 路由前缀
app.include_router(api_router, prefix="/api/v1")

# 打印所有路由，检查是否注册成功
for route in app.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")

# 如果你运行应用，使用以下命令启动：
# uvicorn app.main:app --reload