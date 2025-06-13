# 前端多端API适配指南

## 概述

后端已完成多端API架构重构，前端需要相应更新API调用路径。本指南将帮助您完成前端的适配工作。

## 🔄 API路径变更对照表

### 认证相关API

| 功能 | 旧路径 | 新路径 | 适用端 |
|------|--------|--------|---------|
| 用户注册 | `/api/legacy/auth/register/` | `/api/v1/user/auth/register/` | 用户端 |
| 用户登录 | `/api/legacy/auth/login/` | `/api/v1/user/auth/login/` | 用户端 |
| 用户登出 | `/api/legacy/auth/logout/` | `/api/v1/user/auth/logout/` | 用户端 |
| 商户注册 | `/api/legacy/auth/register/` | `/api/v1/merchant/auth/register/` | 商户端 |
| 商户登录 | `/api/legacy/auth/login/` | `/api/v1/merchant/auth/login/` | 商户端 |
| 管理员登录 | `/api/legacy/auth/login/` | `/api/v1/admin/auth/login/` | 管理端 |

### 业务功能API

| 功能 | 旧路径 | 新路径 | 适用端 |
|------|--------|--------|---------|
| 用户个人资料 | `/api/legacy/users/me/` | `/api/v1/user/profile/me/` | 用户端 |
| 商户仪表板 | `/api/legacy/merchant/dashboard/` | `/api/v1/merchant/dashboard/stats/` | 商户端 |
| 用户管理 | `/api/legacy/admin/users/` | `/api/v1/admin/users/` | 管理端 |
| 商户管理 | `/api/legacy/admin/merchants/` | `/api/v1/admin/merchants/` | 管理端 |

### 共享业务API（保持不变）

以下API在各端都可以使用，路径保持不变：

- 地区信息：`/api/v1/{端}/regions/`
- 村庄信息：`/api/v1/{端}/villages/`
- 民宿信息：`/api/v1/{端}/homestays/`
- 产品信息：`/api/v1/{端}/products/`
- 订单管理：`/api/v1/{端}/orders/`

## 📱 各端前端适配说明

### 用户端前端 (`frontend/user/`)

#### 1. 更新API基础URL

```javascript
// 旧配置
const API_BASE_URL = '/api/legacy'

// 新配置
const API_BASE_URL = '/api/v1/user'
```

#### 2. 更新认证相关调用

```javascript
// 用户注册
// 旧: POST /api/legacy/auth/register/
// 新: POST /api/v1/user/auth/register/
const register = async (userData) => {
  return await fetch('/api/v1/user/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  })
}

// 用户登录
// 旧: POST /api/legacy/auth/login/
// 新: POST /api/v1/user/auth/login/
const login = async (credentials) => {
  return await fetch('/api/v1/user/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  })
}
```

#### 3. 更新个人资料调用

```javascript
// 获取用户个人资料
// 旧: GET /api/legacy/users/me/
// 新: GET /api/v1/user/profile/me/
const getUserProfile = async (token) => {
  return await fetch('/api/v1/user/profile/me/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
}
```

### 商户端前端 (`frontend/merchant/`)

#### 1. 更新API基础URL

```javascript
// 旧配置
const API_BASE_URL = '/api/legacy'

// 新配置
const API_BASE_URL = '/api/v1/merchant'
```

#### 2. 更新认证相关调用

```javascript
// 商户登录
// 旧: POST /api/legacy/auth/login/
// 新: POST /api/v1/merchant/auth/login/
const merchantLogin = async (credentials) => {
  return await fetch('/api/v1/merchant/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  })
}
```

#### 3. 更新仪表板调用

```javascript
// 获取商户仪表板数据
// 旧: GET /api/legacy/merchant/dashboard/
// 新: GET /api/v1/merchant/dashboard/stats/
const getDashboardStats = async (token) => {
  return await fetch('/api/v1/merchant/dashboard/stats/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
}
```

### 管理端前端 (`frontend/admin/`)

#### 1. 更新API基础URL

```javascript
// 旧配置
const API_BASE_URL = '/api/legacy'

// 新配置
const API_BASE_URL = '/api/v1/admin'
```

#### 2. 更新管理功能调用

```javascript
// 管理员登录
// 旧: POST /api/legacy/auth/login/
// 新: POST /api/v1/admin/auth/login/
const adminLogin = async (credentials) => {
  return await fetch('/api/v1/admin/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  })
}

// 用户管理
// 旧: GET /api/legacy/admin/users/
// 新: GET /api/v1/admin/users/
const getUsers = async (token) => {
  return await fetch('/api/v1/admin/users/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
}
```

## 🔧 通用适配工具

### 1. API客户端封装

建议为每个前端创建统一的API客户端：

```javascript
// api-client.js
class APIClient {
  constructor(baseURL, endpoint) {
    this.baseURL = baseURL
    this.endpoint = endpoint
  }
  
  async request(path, options = {}) {
    const url = `${this.baseURL}${this.endpoint}${path}`
    const token = localStorage.getItem('token')
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    }
    
    return await fetch(url, { ...defaultOptions, ...options })
  }
}

// 用户端
const userAPI = new APIClient('/api/v1', '/user')

// 商户端
const merchantAPI = new APIClient('/api/v1', '/merchant')

// 管理端
const adminAPI = new APIClient('/api/v1', '/admin')
```

### 2. 环境配置

在各前端项目中添加环境配置：

```javascript
// config/api.js
const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8000',
    endpoint: process.env.REACT_APP_API_ENDPOINT || '/user' // user/merchant/admin
  },
  production: {
    baseURL: 'https://api.miaxiangji.com',
    endpoint: process.env.REACT_APP_API_ENDPOINT || '/user'
  }
}

export const getAPIConfig = () => {
  const env = process.env.NODE_ENV || 'development'
  return API_CONFIG[env]
}
```

## 🧪 测试适配结果

### 1. 运行后端API测试

```bash
# 在backend目录下运行
python3 test_multiapi_endpoints.py

# 或测试特定端
python3 test_multiapi_endpoints.py --user
python3 test_multiapi_endpoints.py --merchant
python3 test_multiapi_endpoints.py --admin
```

### 2. 前端集成测试

在每个前端项目中添加API测试：

```javascript
// tests/api.test.js
describe('API Integration Tests', () => {
  test('用户登录API', async () => {
    const response = await userAPI.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({
        username: 'testuser',
        password: 'testpass'
      })
    })
    
    expect(response.status).toBe(200)
  })
})
```

## 📋 迁移检查清单

### 用户端前端
- [ ] 更新API基础URL配置
- [ ] 更新用户注册API调用
- [ ] 更新用户登录API调用
- [ ] 更新用户个人资料API调用
- [ ] 更新收藏功能API调用
- [ ] 测试所有用户功能

### 商户端前端
- [ ] 更新API基础URL配置
- [ ] 更新商户登录API调用
- [ ] 更新商户注册API调用
- [ ] 更新商户仪表板API调用
- [ ] 更新商户业务管理API调用
- [ ] 测试所有商户功能

### 管理端前端
- [ ] 更新API基础URL配置
- [ ] 更新管理员登录API调用
- [ ] 更新用户管理API调用
- [ ] 更新商户管理API调用
- [ ] 更新系统管理API调用
- [ ] 测试所有管理功能

## ⚠️ 注意事项

1. **渐进式迁移**：建议先在开发环境完成迁移和测试，再部署到生产环境

2. **向后兼容**：Legacy API仍然可用，可以逐步迁移而不是一次性全部更改

3. **错误处理**：新API的错误响应格式可能有所不同，需要更新错误处理逻辑

4. **权限验证**：新的多端API有更严格的权限控制，确保前端正确处理权限错误

5. **Token管理**：各端的Token是独立的，不能跨端使用

## 🚀 部署建议

1. **开发环境测试**：先在本地开发环境完成所有适配
2. **预发布环境验证**：在预发布环境进行完整的功能测试
3. **灰度发布**：可以考虑灰度发布，逐步切换到新API
4. **监控告警**：部署后密切监控API调用情况和错误率

## 📞 技术支持

如果在适配过程中遇到问题，可以：

1. 查看后端API文档：`/api/docs/`
2. 运行API测试脚本验证后端功能
3. 检查浏览器开发者工具的网络请求
4. 查看后端日志文件：`backend/debug.log`

完成适配后，您的前端应用将享受到更清晰的架构、更好的权限控制和更易维护的代码结构！