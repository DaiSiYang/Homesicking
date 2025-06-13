# 觅乡记 - 用户模块API

## 认证相关接口

### 用户注册

- **URL**: `/api/v1/auth/register/`
- **方法**: `POST`
- **权限**: 无需认证
- **描述**: 用户注册接口

**请求参数**:
```json
{
  "username": "user123",
  "password": "yourpassword",
  "confirm_password": "yourpassword",
  "email": "user@example.com",
  "phone": "13812345678",
  "user_type": "tourist" // tourist(游客)/merchant(商户)
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user_id": 1,
    "username": "user123",
    "email": "user@example.com",
    "user_type": "tourist",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 用户登录

- **URL**: `/api/v1/auth/login/`
- **方法**: `POST`
- **权限**: 无需认证
- **描述**: 用户登录接口

**请求参数**:
```json
{
  "username": "user123",
  "password": "yourpassword"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user_id": 1,
    "username": "user123",
    "email": "user@example.com",
    "user_type": "tourist",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 刷新Token

- **URL**: `/api/v1/auth/refresh-token/`
- **方法**: `POST`
- **权限**: 无需认证
- **描述**: 刷新JWT令牌

**请求参数**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "刷新成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 用户登出

- **URL**: `/api/v1/auth/logout/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 用户登出接口

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "登出成功",
  "data": null
}
```

## 用户信息相关接口

### 获取当前用户信息

- **URL**: `/api/v1/users/me/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取当前登录用户信息

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "phone": "13812345678",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "个人简介",
    "user_type": "tourist",
    "created_at": "2023-01-01T12:00:00Z",
    "profile": {
      "real_name": "张三",
      "gender": "male",
      "birthday": "1990-01-01",
      "address": "北京市朝阳区"
    }
  }
}
```

### 更新用户信息

- **URL**: `/api/v1/users/me/`
- **方法**: `PATCH`
- **权限**: 需要认证
- **描述**: 更新当前登录用户信息

**请求参数**:
```json
{
  "avatar": "https://example.com/new-avatar.jpg",
  "bio": "新的个人简介",
  "profile": {
    "real_name": "李四",
    "gender": "male",
    "birthday": "1992-01-01",
    "address": "上海市浦东新区"
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "phone": "13812345678",
    "avatar": "https://example.com/new-avatar.jpg",
    "bio": "新的个人简介",
    "user_type": "tourist",
    "created_at": "2023-01-01T12:00:00Z",
    "profile": {
      "real_name": "李四",
      "gender": "male",
      "birthday": "1992-01-01",
      "address": "上海市浦东新区"
    }
  }
}
```

### 修改密码

- **URL**: `/api/v1/users/change-password/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 修改用户密码

**请求参数**:
```json
{
  "old_password": "oldpassword",
  "new_password": "newpassword",
  "confirm_password": "newpassword"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

## 商户信息相关接口

### 商户入驻申请

- **URL**: `/api/v1/merchants/apply/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 用户申请成为商户

**请求参数**:
```json
{
  "business_name": "山水民宿",
  "business_license": "base64编码的图片",
  "contact_person": "王五",
  "contact_phone": "13987654321",
  "address": "浙江省杭州市临安区太湖源村",
  "description": "位于太湖源村的特色民宿"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "申请提交成功，等待审核",
  "data": {
    "id": 1,
    "business_name": "山水民宿",
    "contact_person": "王五",
    "contact_phone": "13987654321",
    "status": "pending",
    "created_at": "2023-01-01T12:00:00Z"
  }
}
```

### 获取商户信息

- **URL**: `/api/v1/merchants/me/`
- **方法**: `GET`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 获取当前商户信息

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "business_name": "山水民宿",
    "business_license": "https://example.com/license.jpg",
    "contact_person": "王五",
    "contact_phone": "13987654321",
    "address": "浙江省杭州市临安区太湖源村",
    "description": "位于太湖源村的特色民宿",
    "status": "approved",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-05T10:00:00Z"
  }
}
```

### 更新商户信息

- **URL**: `/api/v1/merchants/me/`
- **方法**: `PATCH`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 更新商户信息

**请求参数**:
```json
{
  "business_name": "山水特色民宿",
  "contact_person": "赵六",
  "contact_phone": "13765432198",
  "address": "浙江省杭州市临安区太湖源村28号",
  "description": "位于太湖源村的传统特色民宿，提供农家饭菜"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "user_id": 1,
    "business_name": "山水特色民宿",
    "business_license": "https://example.com/license.jpg",
    "contact_person": "赵六",
    "contact_phone": "13765432198",
    "address": "浙江省杭州市临安区太湖源村28号",
    "description": "位于太湖源村的传统特色民宿，提供农家饭菜",
    "status": "approved",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-10T14:00:00Z"
  }
}
```

## 收藏相关接口

### 获取收藏列表

- **URL**: `/api/v1/favorites/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取用户收藏列表

**请求参数**:
- `type`: 收藏类型，可选值：`village`, `homestay`, `product`, `food`, `travel_note`
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
        "target_type": "homestay",
        "target_id": 5,
        "created_at": "2023-01-15T09:30:00Z",
        "target_info": {
          "id": 5,
          "name": "竹林小筑",
          "cover_image": "https://example.com/homestay5.jpg",
          "intro": "位于竹林深处的特色民宿",
          "price": 298
        }
      },
      {
        "id": 2,
        "target_type": "village",
        "target_id": 3,
        "created_at": "2023-01-10T14:20:00Z",
        "target_info": {
          "id": 3,
          "name": "太湖源村",
          "cover_image": "https://example.com/village3.jpg",
          "intro": "浙江省杭州市临安区著名的乡村旅游目的地"
        }
      }
    ],
    "total": 7,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 添加收藏

- **URL**: `/api/v1/favorites/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 添加收藏

**请求参数**:
```json
{
  "target_type": "homestay",
  "target_id": 10
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "收藏成功",
  "data": {
    "id": 3,
    "target_type": "homestay",
    "target_id": 10,
    "created_at": "2023-01-20T16:40:00Z"
  }
}
```

### 取消收藏

- **URL**: `/api/v1/favorites/{id}/`
- **方法**: `DELETE`
- **权限**: 需要认证
- **描述**: 取消收藏

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "取消收藏成功",
  "data": null
}
``` 