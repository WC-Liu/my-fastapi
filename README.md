# 🎬 电影评论管理系统

基于 **FastAPI** 构建的现代化电影评论管理后端服务，提供完善的用户认证、电影管理和评论功能。

## ✨ 功能特性

### 👤 用户系统
- 用户注册（邮箱验证激活）
- 登录/登出（双令牌 JWT 认证）
- 令牌刷新与黑名单机制
- 密码重置（邮箱验证）
- 用户信息管理（管理员）

### 🎥 电影管理
- 电影 CRUD（增删改查）
- 电影评分与分类
- 管理员专属管理权限

### 💬 评论系统
- 用户对电影发表评论
- 评分与评论内容
- 评论管理（管理员）

### 🔐 安全特性
- 密码使用 Argon2 强哈希
- JWT 双令牌（Access Token + Refresh Token）
- 令牌黑名单（Redis）
- 邮箱验证机制
- 角色权限控制（普通用户/管理员）
- 统一异常处理

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.12** | 编程语言 |
| **FastAPI** | Web 框架 |
| **SQLModel** | ORM（SQLAlchemy + Pydantic） |
| **PostgreSQL** | 关系数据库 |
| **Redis** | 缓存与令牌黑名单 |
| **Alembic** | 数据库迁移 |
| **Celery + Flower** | 异步任务队列与监控 |
| **Pydantic** | 数据验证 |
| **JWT** | 身份认证 |
| **Argon2 / bcrypt** | 密码哈希 |
| **FastAPI-Mail** | 邮件服务 |
| **Ruff** | 代码检查 |
| **Pytest** | 单元测试 |
| **Docker** | 容器化部署（推荐） |

## 📁 项目结构
```text
my-fastapi/
├── app/
│   ├── core/
│   │   ├── config.py          # 全局配置
│   │   ├── dependencies.py    # 依赖注入
│   │   └── security.py        # 密码/JWT/令牌处理
│   ├── db/
│   │   ├── db.py              # 数据库连接
│   │   └── redis.py           # Redis 连接
│   ├── models/
│   │   └── models.py          # 数据库模型（User, Movie, Review）
│   ├── routers/
│   │   ├── auth.py            # 认证路由
│   │   ├── movies.py          # 电影路由
│   │   ├── users.py           # 用户路由
│   │   └── reviews.py         # 评论路由
│   ├── schemas/
│   │   ├── auth.py            # 认证数据模型
│   │   ├── movie.py           # 电影数据模型
│   │   ├── review.py          # 评论数据模型
│   │   └── user.py            # 用户数据模型
│   ├── service/
│   │   ├── auth_service.py    # 认证业务逻辑
│   │   ├── user_service.py    # 用户业务逻辑
│   │   ├── movie_service.py   # 电影业务逻辑
│   │   ├── review_service.py  # 评论业务逻辑
│   │   └── mail_service.py    # 邮件业务逻辑
│   ├── utils/
│   │   ├── exceptions.py      # 自定义异常处理
│   │   ├── middleware.py      # 中间件
│   │   ├── mail.py            # 邮件工具
│   │   └── celery.py          # Celery 任务配置
│   └── main.py                # 应用入口
├── migrations/                # 数据库迁移文件
├── tests/                     # 测试文件
├── pyproject.toml             # 项目配置
├── alembic.ini                # Alembic 配置
└── README.md
```
## 🚀 快速开始

### 前置条件

- Python 3.12+
- PostgreSQL
- Redis
- uv

### 1. 克隆项目

```bash
git clone https://github.com/WC-Liu/my-fastapi.git
cd my-fastapi
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
JWT_SECRET=your-secret-key
JWT_ALGORITHMA=HS256
REDIS_URL=redis://localhost:6379/0

# 邮件配置（用于邮箱验证和密码重置）
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-password
MAIL_FROM=your-email@example.com
MAIL_PORT=465
MAIL_SERVER=smtp.example.com
```

### 3. 安装依赖

```bash
uv sync
```

### 4. 运行数据库迁移

```bash
alembic upgrade head
```

### 5. 启动服务

```bash
fastapi dev
```

### 6. 访问文档

启动后访问：

- **API 文档**: http://localhost:8000/docs
- **替代文档**: http://localhost:8000/redoc

## 📬 API 接口

### 认证 `/api/v1/auth`

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/register` | 用户注册 | 公开 |
| GET | `/verify/{token}` | 邮箱验证 | 公开 |
| POST | `/login` | 用户登录 | 公开 |
| POST | `/refresh` | 刷新令牌 | 公开 |
| GET | `/logout` | 退出登录 | 登录用户 |
| POST | `/password-reset-request` | 请求密码重置 | 公开 |
| POST | `/password-reset-confirm/{token}` | 确认密码重置 | 公开 |
| GET | `/me` | 获取当前用户 | 登录用户 |

### 用户 `/api/v1/users`

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/` | 获取所有用户 | 管理员 |
| GET | `/{uid}` | 获取指定用户 | 管理员 |
| PATCH | `/{uid}` | 更新用户 | 管理员 |
| DELETE | `/{uid}` | 删除用户 | 管理员 |

### 电影 `/api/v1/movies`

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/` | 获取所有电影 | 登录用户 |
| GET | `/{uid}` | 获取电影详情 | 登录用户 |
| POST | `/` | 创建电影 | 管理员 |
| PATCH | `/{uid}` | 更新电影 | 管理员 |
| DELETE | `/{uid}` | 删除电影 | 管理员 |

## 🧪 运行测试

```bash
pytest tests/ -v
```

## 📦 Docker 部署（推荐）

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY . .

CMD ["fastapi", "dev"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

## 📄 开源协议

MIT
