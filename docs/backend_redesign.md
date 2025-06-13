# 觅乡记后端架构重构方案

## 当前架构问题分析

### 现有架构特点
- 单一API入口，所有端共用相同的接口
- 权限控制混杂在各个视图中
- 缺乏明确的端点分离
- 商户端和管理端功能耦合度高

### 存在的问题
1. **权限管理复杂**：三个端的权限需求不同，当前架构难以清晰管理
2. **接口职责不清**：同一个接口可能需要处理不同端的不同需求
3. **扩展性差**：新增功能时需要考虑对其他端的影响
4. **维护困难**：代码耦合度高，修改一个端可能影响其他端

## 新架构设计方案

### 1. 多端API分离架构

```
api/
├── v1/
│   ├── user/          # 用户端API
│   │   ├── auth/       # 用户认证
│   │   ├── profile/    # 用户资料
│   │   ├── booking/    # 预订相关
│   │   ├── orders/     # 订单管理
│   │   ├── favorites/  # 收藏功能
│   │   └── content/    # 内容浏览
│   ├── merchant/       # 商户端API
│   │   ├── auth/       # 商户认证
│   │   ├── profile/    # 商户资料
│   │   ├── products/   # 产品管理
│   │   ├── homestays/  # 民宿管理
│   │   ├── orders/     # 订单管理
│   │   ├── analytics/  # 数据分析
│   │   └── finance/    # 财务管理
│   └── admin/          # 管理后台API
│       ├── auth/       # 管理员认证
│       ├── users/      # 用户管理
│       ├── merchants/  # 商户管理
│       ├── content/    # 内容管理
│       ├── orders/     # 订单监控
│       ├── analytics/  # 平台数据
│       └── system/     # 系统设置
```

### 2. 应用重构方案

#### 2.1 核心业务应用（保持不变）
- `apps.users` - 用户模型和基础功能
- `apps.regions` - 地区管理
- `apps.villages` - 村庄和景点
- `apps.homestays` - 民宿管理
- `apps.products` - 产品管理
- `apps.orders` - 订单系统

#### 2.2 新增端点应用
- `apps.api_user` - 用户端API视图和序列化器
- `apps.api_merchant` - 商户端API视图和序列化器
- `apps.api_admin` - 管理端API视图和序列化器

#### 2.3 共享服务应用
- `apps.services` - 业务逻辑服务层
- `apps.notifications` - 通知服务
- `apps.analytics` - 数据分析服务
- `apps.payments` - 支付服务

### 3. 权限系统重构

#### 3.1 角色定义
```python
class UserRole(models.TextChoices):
    CUSTOMER = 'customer', '普通用户'
    MERCHANT = 'merchant', '商户'
    ADMIN = 'admin', '管理员'
    SUPER_ADMIN = 'super_admin', '超级管理员'
```

#### 3.2 权限装饰器
```python
# 用户端权限
@user_api_permission
def user_view(request):
    pass

# 商户端权限
@merchant_api_permission
def merchant_view(request):
    pass

# 管理端权限
@admin_api_permission
def admin_view(request):
    pass
```

### 4. 服务层架构

#### 4.1 业务服务层
```python
# apps/services/user_service.py
class UserService:
    @staticmethod
    def create_user_profile(user_data):
        # 用户创建逻辑
        pass
    
    @staticmethod
    def update_user_profile(user, profile_data):
        # 用户更新逻辑
        pass

# apps/services/order_service.py
class OrderService:
    @staticmethod
    def create_order(user, order_data):
        # 订单创建逻辑
        pass
    
    @staticmethod
    def process_payment(order, payment_data):
        # 支付处理逻辑
        pass
```

### 5. 数据传输对象(DTO)

#### 5.1 不同端的数据需求
```python
# 用户端序列化器
class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images', 'description']

# 商户端序列化器
class MerchantProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'cost', 'stock', 'sales_count', 'status']

# 管理端序列化器
class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

### 6. 中间件和认证

#### 6.1 端点识别中间件
```python
class APIEndpointMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 根据URL路径识别API端点
        if request.path.startswith('/api/v1/user/'):
            request.api_endpoint = 'user'
        elif request.path.startswith('/api/v1/merchant/'):
            request.api_endpoint = 'merchant'
        elif request.path.startswith('/api/v1/admin/'):
            request.api_endpoint = 'admin'
        
        response = self.get_response(request)
        return response
```

### 7. 实施步骤

#### 阶段一：基础架构搭建（1-2周）
1. 创建新的API应用结构
2. 重构URL路由配置
3. 实现权限系统
4. 创建基础中间件

#### 阶段二：用户端API迁移（1周）
1. 迁移用户认证相关API
2. 迁移用户端业务API
3. 测试用户端功能

#### 阶段三：商户端API迁移（1-2周）
1. 迁移商户认证相关API
2. 迁移商户端业务API
3. 实现商户端特有功能
4. 测试商户端功能

#### 阶段四：管理端API迁移（1-2周）
1. 迁移管理员认证相关API
2. 迁移管理端业务API
3. 实现管理端特有功能
4. 测试管理端功能

#### 阶段五：优化和完善（1周）
1. 性能优化
2. 安全加固
3. 文档完善
4. 全面测试

### 8. 技术栈建议

- **框架**: Django + Django REST Framework
- **认证**: JWT Token + 角色权限
- **数据库**: MySQL/PostgreSQL
- **缓存**: Redis
- **任务队列**: Celery
- **API文档**: drf-yasg
- **监控**: Django Debug Toolbar + Sentry

### 9. 优势

1. **清晰的职责分离**：每个端有独立的API和业务逻辑
2. **更好的安全性**：不同端的权限完全隔离
3. **易于维护**：修改一个端不会影响其他端
4. **便于扩展**：新增功能时可以针对特定端开发
5. **团队协作**：不同团队可以并行开发不同端的功能

### 10. 注意事项

1. **数据一致性**：确保不同端操作同一数据时的一致性
2. **代码复用**：避免重复代码，合理使用服务层
3. **API版本管理**：为未来的API升级做好准备
4. **性能考虑**：避免N+1查询，合理使用缓存
5. **测试覆盖**：确保每个端的API都有充分的测试覆盖

## 总结

这个重构方案将现有的单一API架构改造为多端分离的架构，每个端都有独立的API入口和权限控制，同时保持核心业务逻辑的统一。这样的设计既保证了各端的独立性，又避免了代码重复，为后续的功能扩展和维护提供了良好的基础。