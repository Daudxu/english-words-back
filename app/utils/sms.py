async def send_sms(phone: str, message: str):
    # 这里调用实际的短信 SDK
    print(f"Sending SMS to {phone}: {message}")
    # 例如：调用阿里云、腾讯云等短信服务