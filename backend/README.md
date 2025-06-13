# 觅乡记 - 乡村旅游平台后端

觅乡记是一个乡村旅游平台，旨在促进乡村旅游发展，让用户发现和体验美丽乡村。

## 项目结构

```
backend/
├── apps/                   # 应用目录
│   ├── admin/              # 管理后台应用
│   ├── regions/            # 区域管理应用
│   ├── users/              # 用户应用
│   ├── villages/           # 乡村和景点应用
│   ├── homestays/          # 民宿和房型应用
│   └── utils/              # 公共工具类
├── config/                 # 项目配置
│   ├── settings.py         # 主配置文件
│   ├── urls.py             # URL配置
│   ├── wsgi.py             # WSGI配置
│   └── asgi.py             # ASGI配置
├── manage.py               # Django管理脚本
└── requirements.txt        # 项目依赖
```

## 主要功能

- 用户注册、登录、退出
- 用户信息管理
- 商户入驻与管理
- 区域管理
- 乡村和景点信息展示
- 民宿和房型信息展示
- 房间库存和价格管理
- 收藏管理
- RESTful API

## 开发环境配置

1. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

4. 运行开发服务器

```bash
python manage.py runserver
```

## API文档

API文档通过Swagger提供，可以在以下URL访问：

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## 技术栈

- Django 4.2
- Django REST Framework
- Django REST Framework SimpleJWT
- PostgreSQL / MySQL
- Swagger / ReDoc

## 环境变量

项目使用.env文件管理环境变量，需要创建.env文件并设置以下变量：

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
``` 