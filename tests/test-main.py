from datetime import datetime, timedelta, UTC
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

# 密钥，实际使用时建议从环境变量或配置文件中读取
SECRET_KEY = "qweqweqwe"
# 加密算法
ALGORITHM = "HS256"
# 令牌过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES = 600

# 定义 OAuth2 认证方案，这里 tokenUrl 只是形式上的，实际不会用到
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    # 配置 Swagger UI 的安全方案
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": [],
    },
    # 定义安全方案
    openapi_tags=[
        {
            "name": "protected",
            "description": "受保护的接口，需要 JWT 认证",
            "externalDocs": {
                "description": "更多信息",
                "url": "https://example.com",
            },
        },
    ],
    # 定义安全方案的详细信息
    security=[
        {
            "OAuth2PasswordBearer": []
        }
    ]
)


# 定义用户 ID 模型
class UserId(BaseModel):
    user_id: int


# 生成 JWT 令牌
def create_jwt_token(user_id: int) -> str:
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user_id),
        "exp": int((datetime.now(UTC) + expire).timestamp())
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解密 JWT 令牌
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError("用户 ID 未找到")
        return int(user_id)
    except JWTError:
        return None


# 获取当前用户 ID
async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_jwt_token(token)
    if user_id is None:
        raise credentials_exception
    return user_id


# 生成 JWT 令牌的端点
@app.post("/generate_token")
async def generate_token(user_id_data: UserId):
    access_token = create_jwt_token(user_id_data.user_id)
    return {"access_token": access_token, "token_type": "bearer"}


# 受保护的端点
@app.get("/protected", tags=["protected"])
async def protected_route(user_id: int = Depends(get_current_user_id)):
    return {"message": f"你已通过认证，用户 ID: {user_id}"}

# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQwMDU3ODY1fQ.NKtwj1wfjrCjiXgSvd8aCzgJWxV9EH-fq9Sn6vWkpcE