# CORS跨域问题解决指南

## 🚨 问题描述

前端应用（运行在 `http://localhost:3000`）无法访问后端API（`http://localhost:8000`），出现CORS跨域错误：

```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## ✅ 解决方案

### 1. 确认CORS配置

在 `config/settings.py` 中已经正确配置了CORS：

```python
# CORS设置
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

### 2. 启动Django服务器

#### 方法1：标准启动
```bash
cd /Users/syd/Desktop/觅乡记/backend
python3 manage.py migrate
python3 manage.py runserver 8000
```

#### 方法2：如果遇到中断问题
```bash
# 使用nohup在后台运行
nohup python3 manage.py runserver 8000 > server.log 2>&1 &

# 或者使用screen
screen -S django_server
python3 manage.py runserver 8000
# 按 Ctrl+A, 然后按 D 来分离screen会话
```

#### 方法3：使用Gunicorn（生产环境）
```bash
# 安装gunicorn（如果还没安装）
pip3 install gunicorn

# 启动服务器
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 3. 验证服务器状态

#### 检查端口占用
```bash
lsof -i :8000
```

#### 测试API端点
```bash
# 测试基本连接
curl http://localhost:8000/api/docs/

# 测试具体API
curl http://localhost:8000/api/v1/villages/
curl http://localhost:8000/api/v1/products/
```

### 4. 前端配置检查

确保前端的API请求配置正确：

```javascript
// 在前端的API配置文件中
const API_BASE_URL = 'http://localhost:8000'

// 或者使用环境变量
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'
```

## 🔧 故障排除

### 问题1：Django服务器无法启动

**可能原因**：
- 数据库连接问题
- 端口被占用
- Python环境问题
- Django配置错误

**解决步骤**：

1. **检查数据库**：
   ```bash
   # 如果使用SQLite（临时解决方案）
   python3 manage.py migrate
   
   # 如果使用MySQL，确保MySQL服务运行
   brew services start mysql
   # 或
   sudo systemctl start mysql
   ```

2. **检查Python环境**：
   ```bash
   python3 --version
   pip3 list | grep Django
   ```

3. **重新安装依赖**：
   ```bash
   pip3 install -r requirements.txt
   ```

### 问题2：CORS仍然被阻止

**增强CORS配置**：

在 `config/settings.py` 中添加更详细的CORS设置：

```python
# 更详细的CORS配置
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# 允许的请求头
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# 允许的HTTP方法
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 如果只允许特定域名（生产环境推荐）
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]
```

### 问题3：API端点不存在

**检查URL配置**：

1. 确认API路由正确配置在 `config/urls.py`
2. 检查各应用的 `urls.py` 文件
3. 运行URL测试脚本：
   ```bash
   python3 test_api_urls.py
   ```

## 🚀 快速启动脚本

创建一个启动脚本 `start_server.sh`：

```bash
#!/bin/bash
echo "启动觅乡记后端服务器..."

# 进入后端目录
cd /Users/syd/Desktop/觅乡记/backend

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip3 install -r requirements.txt

# 数据库迁移
echo "执行数据库迁移..."
python3 manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python3 manage.py collectstatic --noinput

# 启动服务器
echo "启动Django服务器..."
python3 manage.py runserver 0.0.0.0:8000
```

使用方法：
```bash
chmod +x start_server.sh
./start_server.sh
```

## 📝 验证清单

启动服务器后，请验证以下内容：

- [ ] Django服务器在8000端口正常运行
- [ ] 可以访问 `http://localhost:8000/api/docs/`
- [ ] API端点返回正确响应（不是404）
- [ ] 前端可以成功发起API请求
- [ ] 没有CORS错误
- [ ] 认证功能正常工作

## 🔍 调试技巧

1. **查看Django日志**：
   ```bash
   tail -f debug.log
   ```

2. **使用浏览器开发者工具**：
   - 检查Network标签页的请求状态
   - 查看Console中的错误信息
   - 确认请求头和响应头

3. **使用Postman或curl测试API**：
   ```bash
   curl -X GET http://localhost:8000/api/v1/villages/ \
        -H "Content-Type: application/json"
   ```

## 📞 如果问题仍然存在

1. 检查防火墙设置
2. 确认网络连接
3. 重启开发环境
4. 查看系统日志
5. 考虑使用Docker容器化部署

完成这些步骤后，前端应该能够正常访问后端API，CORS错误应该得到解决。