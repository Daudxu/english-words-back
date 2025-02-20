from datetime import datetime, UTC
import pytz
# current_time = int(datetime.utcnow().timestamp())
# current_time2 = datetime.now(UTC)

# print(current_time)
# print(current_time2)


# # 获取东八区的时区对象
# tz = pytz.timezone('Asia/Shanghai')

# # 获取当前东八区的时间
# current_time = datetime.now(tz)

# # 获取当前东八区时间对应的 Unix 时间戳（秒）
# timestamp = int(current_time.timestamp())

# print(f"当前东八区时间: {current_time}")
# print(f"当前东八区时间的 Unix 时间戳: {timestamp}")


# from datetime import datetime
# import pytz

# 获取东八区的时区对象
tz = pytz.timezone('Asia/Shanghai')

# 获取当前东八区的时间
current_time_east8 = datetime.now(tz)

# 获取当前东八区时间对应的 Unix 时间戳（秒）
current_time = int(current_time_east8.timestamp())
print(f"当前东八区时间戳: {current_time}")

# 当前时间 + 2 天（单位秒）
vip_end_time = current_time + (2 * 24 * 60 * 60)
print(f"VIP 到期时间戳: {vip_end_time}")

# 将 VIP 到期时间戳转换为东八区的日期时间
vip_end_datetime = datetime.fromtimestamp(vip_end_time, tz)
print(f"VIP 到期时间（东八区）: {vip_end_datetime}")