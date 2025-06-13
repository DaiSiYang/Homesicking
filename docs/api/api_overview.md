# 觅乡记 - API 接口设计概述

## API 设计原则

觅乡记平台API采用RESTful风格设计，遵循以下原则：

1. 资源导向：API围绕资源设计，使用名词表示资源
2. HTTP方法语义：
   - GET：获取资源
   - POST：创建资源
   - PUT：更新资源（全部字段）
   - PATCH：更新资源（部分字段）
   - DELETE：删除资源
3. 状态码规范：
   - 2xx：成功
   - 4xx：客户端错误
   - 5xx：服务器错误
4. 版本控制：API URL中包含版本号，如 `/api/v1/`
5. 分页处理：对列表请求提供分页、排序和筛选功能
6. 错误处理：提供统一的错误响应格式

## API 基础URL

- 开发环境：`http://localhost:8000/api/v1/`
- 生产环境：`https://api.miaxiangji.com/api/v1/`

## 认证方式

API采用JWT (JSON Web Token) 认证机制：

1. 客户端通过登录接口获取token
2. 后续请求在Header中携带token：`Authorization: Bearer <token>`
3. token过期后需要刷新或重新登录

## 通用请求头

```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token> (需要认证的接口)
```

## 通用响应格式

成功响应：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 响应数据
  }
}
```

错误响应：
```json
{
  "code": 400,
  "message": "错误信息",
  "errors": {
    "field1": ["错误描述1", "错误描述2"],
    "field2": ["错误描述"]
  }
}
```

## 分页响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      // 数据列表
    ],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "pages": 10
  }
}
```

## API 模块划分

API接口按照业务功能划分为以下几个主要模块：

1. **认证模块**：用户注册、登录、退出、Token刷新
2. **用户模块**：用户信息管理、收藏管理
3. **区域模块**：省市县、热门区域
4. **乡村模块**：乡村信息、景点
5. **住宿模块**：民宿、房型、房价
6. **农产品模块**：产品信息、SKU
7. **餐饮模块**：美食信息
8. **订单模块**：购物车、订单管理
9. **支付模块**：支付处理、退款
10. **评价模块**：评价、回复
11. **内容模块**：游记、问答、资讯
12. **商户模块**：商户资源管理
13. **管理模块**：平台内容管理、审核

## 权限设计

API接口根据用户角色进行权限控制：

1. **游客**：可访问公开内容，无需认证
2. **注册用户**：需要认证，可访问个人相关接口
3. **商户**：需要认证，可访问商户管理接口
4. **管理员**：需要认证，可访问管理后台接口

## 接口限流

为保护系统资源，API实施请求速率限制：

- 匿名用户：10次/分钟
- 注册用户：60次/分钟
- 商户用户：100次/分钟
- 管理员：200次/分钟

## API文档生成

本项目使用Django REST Framework自动生成Swagger/OpenAPI文档，文档访问地址：

- 开发环境：`http://localhost:8000/api/docs/`
- 生产环境：`https://api.miaxiangji.com/api/docs/`