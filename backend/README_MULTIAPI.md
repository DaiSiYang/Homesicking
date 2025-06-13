# 觅乡记后端多端API架构

## 架构概述

觅乡记后端已重构为支持三个不同端的多端API架构：

1. **用户端API** (`/api/v1/user/`)
   - 面向普通用户的接口
   - 提供浏览、预订、支付等功能

2. **商户端API** (`/api/v1/merchant/`)
   - 面向商户的接口
   - 提供商品管理、订单处理、数据分析等功能

3. **管理端API** (`/api/v1/admin/`)
   - 面向平台管理员的接口
   - 提供用户管理、内容审核、系统配置等功能

## 目录结构

```
backend/
├── apps/
│   ├── api_user/         # 用户端API应用
│   │   ├── views/        # 视图函数
│   │   ├── serializers/  # 序列化器
│   │   └── urls/         # URL配置
│   ├── api_merchant/     # 商户端API应用
│   │   ├── views/
│   │   ├── serializers/
│   │   └── urls/
│   ├── api_admin/        # 管理端API应用
│   │   ├── views/
│   │   ├── serializers/
│   │   └── urls/
│   ├── services/         # 业务服务层
│   └── ... (其他业务应用)
```

## URL路由配置

- 新版多端API: `/api/v1/`
  - 用户端: `/api/v1/user/`
  - 商户端: `/api/v1/merchant/`
  - 管理端: `/api/v1/admin/`

- 兼容旧版API: `/api/legacy/`

## 权限控制

每个端都有独立的权限控制装饰器：

- `@user_api_permission` - 用户端API权限
- `@merchant_api_permission` - 商户端API权限
- `@admin_api_permission` - 管理端API权限

## 服务层

业务逻辑集中在服务层实现，避免在视图中直接处理复杂业务逻辑：

- `AuthService` - 认证相关服务
- `UserService` - 用户相关服务
- `MerchantService` - 商户相关服务

## 迁移指南

### 从旧版API迁移到多端API

1. 确定接口所属的端（用户端/商户端/管理端）
2. 在对应的API应用中创建视图和URL
3. 使用服务层处理业务逻辑
4. 应用适当的权限装饰器
5. 更新前端调用路径

### 添加新功能

1. 确定功能所属的端
2. 在对应的API应用中添加视图和URL
3. 在服务层实现业务逻辑
4. 添加适当的测试

## 测试

为确保多端API正常工作，请运行以下测试：

```bash
# 运行所有测试
python manage.py test

# 运行特定端的测试
python manage.py test apps.api_user
python manage.py test apps.api_merchant
python manage.py test apps.api_admin
```

## 文档

API文档可通过以下URL访问：

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## 注意事项

1. 旧版API (`/api/legacy/`) 将逐步废弃，请尽快迁移到新版多端API
2. 确保在适当的端实现功能，避免功能重复或混乱
3. 使用服务层共享业务逻辑，避免代码重复
4. 始终应用正确的权限装饰器，确保安全性