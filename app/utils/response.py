# app/utils/response.py

def success_response(data=None, message="Success"):
    """成功响应封装"""
    return {
        "status": 200,
        "message": message,
        "data": data
    }

def error_response(status_code, message="Error"):
    """错误响应封装"""
    return {
        "status": status_code,
        "message": message,
        "data": None
    }