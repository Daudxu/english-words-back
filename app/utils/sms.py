import requests
from app.schemas.sms import CommonResponse  # 引入新的 CommonResponse
from app.core.config import settings

def send_sms(phone: str, code: str) -> CommonResponse:
    requestParams = {
        'key': settings.SMS_API_KEY,
        'mobile': phone,
        'tpl_id': '157293',  # 请替换为你自己设置的模板ID
        'vars': '{"code": ' + code + '}',  # 模板变量，替换短信内容的验证码部分
        'tpl_value': '',  # 如有特殊需求，可使用
        'ext': '',  # 可选扩展字段
    }
    print(requestParams)
    try:
        # 发起接口网络请求
        response = requests.get(settings.SMS_API_URL, params=requestParams)
        response.raise_for_status()  # 如果返回的状态码不是200，将抛出异常

        # 解析响应结果
        response_result = response.json()
        if response.status_code == 200:
            if response_result.get("error_code") == 0:
                # 发送成功
                return CommonResponse(status=200, message="短信发送成功", data=None)
            else:
                # 如果聚合数据返回错误码
                return CommonResponse(status=400, message=f"短信发送失败: {response_result.get('reason')}", data=None)
        else:
            # 请求失败，返回异常信息
            return CommonResponse(status=500, message="短信发送失败，网络异常", data=None)
    
    except requests.RequestException as e:
        # 捕获网络请求异常
        return CommonResponse(status=500, message=f"请求异常: {str(e)}", data=None)
