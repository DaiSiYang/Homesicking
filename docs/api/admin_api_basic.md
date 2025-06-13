# 觅乡记 - 管理后台API (基础部分)

## 通用说明

管理后台API仅供平台管理员使用，所有接口均需要管理员权限。

基础URL: `/api/v1/admin/`

## 用户管理接口

### 获取用户列表

- **URL**: `/api/v1/admin/users/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取用户列表

**请求参数**:
- `user_type`: 用户类型，可选值：`tourist`, `merchant`, `admin`
- `status`: 用户状态，可选值：`active`, `inactive`, `pending`
- `keyword`: 关键词搜索（用户名/手机号/邮箱）
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "phone": "13800000000",
        "user_type": "admin",
        "is_active": true,
        "is_verified": true,
        "created_at": "2023-01-01T00:00:00Z"
      },
      {
        "id": 2,
        "username": "merchant1",
        "email": "merchant1@example.com",
        "phone": "13800000001",
        "user_type": "merchant",
        "is_active": true,
        "is_verified": true,
        "created_at": "2023-01-02T00:00:00Z"
      },
      {
        "id": 3,
        "username": "user1",
        "email": "user1@example.com",
        "phone": "13800000002",
        "user_type": "tourist",
        "is_active": true,
        "is_verified": true,
        "created_at": "2023-01-03T00:00:00Z"
      }
    ],
    "total": 3,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取用户详情

- **URL**: `/api/v1/admin/users/{id}/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取用户详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 3,
    "username": "user1",
    "email": "user1@example.com",
    "phone": "13800000002",
    "avatar": "https://example.com/avatar3.jpg",
    "bio": "热爱旅行的人",
    "user_type": "tourist",
    "is_active": true,
    "is_verified": true,
    "created_at": "2023-01-03T00:00:00Z",
    "updated_at": "2023-01-03T00:00:00Z",
    "profile": {
      "real_name": "张三",
      "gender": "male",
      "birthday": "1990-01-01",
      "address": "北京市朝阳区"
    },
    "orders_count": 5,
    "reviews_count": 3,
    "travel_notes_count": 2,
    "last_login": "2023-05-15T10:30:00Z"
  }
}
```

### 修改用户状态

- **URL**: `/api/v1/admin/users/{id}/status/`
- **方法**: `PATCH`
- **权限**: 需要管理员权限
- **描述**: 修改用户状态（激活/禁用）

**请求参数**:
```json
{
  "is_active": false,
  "reason": "违反平台规则"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "用户状态已更新",
  "data": {
    "id": 3,
    "username": "user1",
    "is_active": false,
    "updated_at": "2023-05-16T09:30:00Z"
  }
}
```

## 商户管理接口

### 获取商户申请列表

- **URL**: `/api/v1/admin/merchant-applications/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取商户入驻申请列表

**请求参数**:
- `status`: 申请状态，可选值：`pending`, `approved`, `rejected`
- `keyword`: 关键词搜索（商户名称/联系人/手机号）
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "user_id": 4,
        "username": "merchant2",
        "business_name": "青山农家",
        "contact_person": "李四",
        "contact_phone": "13800000003",
        "address": "浙江省杭州市临安区太湖源村15号",
        "status": "pending",
        "created_at": "2023-05-15T14:30:00Z"
      },
      {
        "id": 2,
        "user_id": 5,
        "username": "merchant3",
        "business_name": "山水人家",
        "contact_person": "王五",
        "contact_phone": "13800000004",
        "address": "浙江省杭州市临安区太湖源村28号",
        "status": "pending",
        "created_at": "2023-05-14T16:20:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取商户申请详情

- **URL**: `/api/v1/admin/merchant-applications/{id}/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取商户入驻申请详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 4,
    "username": "merchant2",
    "email": "merchant2@example.com",
    "phone": "13800000003",
    "business_name": "青山农家",
    "business_license": "https://example.com/license1.jpg",
    "contact_person": "李四",
    "contact_phone": "13800000003",
    "address": "浙江省杭州市临安区太湖源村15号",
    "description": "位于太湖源村的农家乐，提供住宿和农家菜",
    "status": "pending",
    "created_at": "2023-05-15T14:30:00Z",
    "updated_at": "2023-05-15T14:30:00Z"
  }
}
```

### 审核商户申请

- **URL**: `/api/v1/admin/merchant-applications/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核商户入驻申请

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "资料齐全，符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 1,
    "user_id": 4,
    "business_name": "青山农家",
    "status": "approved",
    "updated_at": "2023-05-16T10:30:00Z"
  }
}
```

### 获取商户列表

- **URL**: `/api/v1/admin/merchants/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取商户列表

**请求参数**:
- `status`: 商户状态，可选值：`active`, `inactive`
- `keyword`: 关键词搜索（商户名称/联系人/手机号）
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "user_id": 2,
        "username": "merchant1",
        "business_name": "山水民宿",
        "contact_person": "张三",
        "contact_phone": "13800000001",
        "address": "浙江省杭州市临安区太湖源村28号",
        "status": "active",
        "homestays_count": 2,
        "products_count": 3,
        "orders_count": 15,
        "created_at": "2023-01-02T00:00:00Z"
      },
      {
        "id": 3,
        "user_id": 4,
        "username": "merchant2",
        "business_name": "青山农家",
        "contact_person": "李四",
        "contact_phone": "13800000003",
        "address": "浙江省杭州市临安区太湖源村15号",
        "status": "active",
        "homestays_count": 1,
        "products_count": 2,
        "orders_count": 8,
        "created_at": "2023-05-16T10:30:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取商户详情

- **URL**: `/api/v1/admin/merchants/{id}/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取商户详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 2,
    "username": "merchant1",
    "email": "merchant1@example.com",
    "phone": "13800000001",
    "business_name": "山水民宿",
    "business_license": "https://example.com/license.jpg",
    "contact_person": "张三",
    "contact_phone": "13800000001",
    "address": "浙江省杭州市临安区太湖源村28号",
    "description": "位于太湖源村的特色民宿",
    "status": "active",
    "created_at": "2023-01-02T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "homestays": [
      {
        "id": 1,
        "name": "溪山隐居",
        "status": "active",
        "orders_count": 10
      },
      {
        "id": 2,
        "name": "山林别院",
        "status": "active",
        "orders_count": 5
      }
    ],
    "products": [
      {
        "id": 1,
        "name": "太湖源山核桃",
        "status": "active",
        "sales": 100
      },
      {
        "id": 2,
        "name": "土鸡蛋",
        "status": "active",
        "sales": 50
      },
      {
        "id": 3,
        "name": "野生蜂蜜",
        "status": "active",
        "sales": 30
      }
    ],
    "total_orders": 15,
    "total_revenue": 15000,
    "avg_rating": 4.8
  }
}
```

### 修改商户状态

- **URL**: `/api/v1/admin/merchants/{id}/status/`
- **方法**: `PATCH`
- **权限**: 需要管理员权限
- **描述**: 修改商户状态（激活/禁用）

**请求参数**:
```json
{
  "status": "inactive",
  "reason": "违反平台规则"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "商户状态已更新",
  "data": {
    "id": 1,
    "business_name": "山水民宿",
    "status": "inactive",
    "updated_at": "2023-05-16T11:30:00Z"
  }
}
``` 