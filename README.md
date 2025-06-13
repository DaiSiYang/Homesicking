# 觅乡记 - 乡村旅游平台

一个集线上推广、预订和管理功能为一体的乡村旅游平台。

## 项目介绍

觅乡记致力于打造一个连接游客与乡村的桥梁，通过线上平台展示乡村风貌，提供民宿预订、特色商品销售、资讯发布与社区互动等服务。

## 系统架构

项目分为三大端口：
- 用户端：面向游客，提供浏览、预订、评价等功能
- 商户端：面向村民/经营者，提供资源管理、订单处理等功能
- 管理后台：面向平台管理员，提供审核、配置、数据统计等功能

## 技术栈

- **前端**：Vue 3、Element Plus、HTML/CSS/JavaScript
- **后端**：Python (Django, Django REST Framework)
- **数据库**：MySQL
- **API**：RESTful 风格

## 功能模块

### 用户端
- **首页**：轮播图、地图热力图、热门乡村目的地、旅游资讯
- **搜索**：多维度搜索、筛选
- **详情页**：景点、美食、民宿、农产品详情
- **预订支付**：购物车、在线预订、支付、电子凭证
- **社区互动**：游记、评价、问答
- **用户中心**：个人信息、收藏、订单、游记管理

### 商户端
- **资源管理**：发布/编辑民宿、农产品，管理库存/价格
- **订单管理**：确认订单、管理入住、处理退款
- **评价管理**：查看评价、回复

### 平台管理后台
- **用户管理**：审核注册用户、管理用户信息
- **商户管理**：审核入驻申请、处理投诉
- **内容管理**：审核内容、推荐配置、标签管理
- **数据统计**：用户数据、热门资源、交易数据
- **系统设置**：基础配置、帮助中心

## 项目结构

```
miaxiangji/
├── frontend/               # 前端代码
│   ├── user/               # 用户端
│   ├── merchant/           # 商户端
│   └── admin/              # 管理后台
├── backend/                # 后端代码
│   ├── config/             # 项目配置
│   ├── apps/               # 应用模块
│   ├── media/              # 媒体文件
│   └── static/             # 静态资源
└── docs/                   # 项目文档
```

## 安装与运行

### 前端
```bash
# 进入对应前端目录（用户端/商户端/管理后台）
cd frontend/user  # 或 merchant 或 admin

# 安装依赖
npm install

# 开发环境运行
npm run dev

# 构建生产环境
npm run build
```

### 后端
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python manage.py migrate

# 运行开发服务器
python manage.py runserver
``` 