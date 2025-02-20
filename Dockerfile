# 使用 Python 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制.env 文件
COPY .env .

# 复制项目代码
COPY . .

# 暴露应用端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]