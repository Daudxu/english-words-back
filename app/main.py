from fastapi import FastAPI
from app.api.v1.routers import api_router

app = FastAPI(title="App")

app.include_router(api_router, prefix="/api/v1")

# 打印所有路由
for route in app.routes:
    print(f"Path: {route.path}, Methods: {route.methods}")