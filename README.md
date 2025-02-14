App Api

###

app/: 主应用目录，包含所有应用代码。

main.py: 应用的入口文件，包含 FastAPI 应用的初始化和启动逻辑。

api/: 包含所有 API 相关的代码。

v1/: 版本化的 API 目录，便于未来扩展多个版本。

endpoints/: 包含各个端点的实现文件，如 users.py、items.py。

routers.py: 定义 API 路由，将各个端点组织起来。

core/: 包含核心配置和安全相关的代码。

config.py: 应用配置，如数据库连接、环境变量等。

security.py: 安全相关的代码，如认证、授权等。

db/: 数据库相关代码。

models/: 数据库模型定义。

repositories/: 数据库操作层，负责与数据库交互。

session.py: 数据库会话管理。

schemas/: Pydantic 模型定义，用于请求和响应的数据验证。

services/: 业务逻辑层，处理具体的业务逻辑。

utils/: 工具函数和辅助代码。

tests/: 单元测试和集成测试代码。

requirements.txt: 项目依赖包列表。

Dockerfile: Docker 镜像构建文件。

docker-compose.yml: Docker Compose 配置文件，用于本地开发和测试。

README.md: 项目说明文档。

.env: 环境变量配置文件。