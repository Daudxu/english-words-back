# app/middleware/jwt_middleware.py
from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings
import logging

# 初始化 logger
logger = logging.getLogger(__name__)

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Processing request: {request.method} {request.url.path}")
        
        # 白名单路径检查（精确匹配）
        if request.url.path in settings.WHITE_LIST_PATHS:
            logger.debug(f"Skipping authentication for path: {request.url.path}")
            return await call_next(request)

        # Token 提取与验证
        auth_header = request.headers.get("Authorization")
       
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning(f"Invalid Authorization header from IP: {request.client.host}")
            return JSONResponse(
                status_code=401,
                content={"code": "INVALID_AUTH_HEADER", "message": "Authorization header format is incorrect"}
            )

        token = auth_header[7:].strip()  # 移除 "Bearer " 前缀
        if not token:
            logger.warning("Token is empty")
            return JSONResponse(
                status_code=401,
                content={"code": "MISSING_TOKEN", "message": "Access token is missing"}
            )

        try:
            # 解码 Token，验证其有效性
            print("------------1-------------")
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            print("------------2-------------")
            logger.debug(f"Successfully decoded payload: {payload}")

            # 提取用户ID
            user_id_str = payload.get("sub")
            if not user_id_str:
                logger.error("Token is missing 'sub' field")
                return JSONResponse(
                    status_code=401,
                    content={"code": "INVALID_PAYLOAD", "message": "Token format error"}
                )
            
            try:
                user_id = int(user_id_str)
            except ValueError:
                logger.error(f"Invalid user ID format: {user_id_str}")
                return JSONResponse(
                    status_code=401,
                    content={"code": "INVALID_USER_ID", "message": "User ID format is invalid"}
                )

            # 时间验证，检查 Token 是否过期
            exp_timestamp = payload.get("exp")
            if not exp_timestamp or not isinstance(exp_timestamp, (int, float)):
                logger.error(f"Invalid expiration timestamp: {exp_timestamp}")
                return JSONResponse(
                    status_code=401,
                    content={"code": "INVALID_EXP", "message": "Token expiration format error"}
                )
            
            # 当前时间与过期时间对比
            current_time = datetime.now(timezone.utc).timestamp()
            if exp_timestamp < current_time:
                logger.info(f"Token expired (user ID: {user_id})")
                return JSONResponse(
                    status_code=401,
                    content={"code": "TOKEN_EXPIRED", "message": "Access token has expired"}
                )

            # 注入用户ID到 request.state
            request.state.user_id = user_id
            logger.debug(f"User ID injected into request: {user_id}")

            # 传递请求并返回响应
            response = await call_next(request)
            return response

        except ExpiredSignatureError:
            print("=========================")
            logger.info(f"Token expired")
            return JSONResponse(
                status_code=401,
                content={"code": "TOKEN_EXPIRED", "message": "Access token has expired"}
            )
        except JWTError as e:
            logger.error(f"JWT verification failed: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"code": "INVALID_TOKEN", "message": "Invalid access token"}
            )
        except Exception as e:
            logger.critical(f"Authentication system error: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"code": "AUTH_ERROR", "message": "Authentication system error"}
            )
