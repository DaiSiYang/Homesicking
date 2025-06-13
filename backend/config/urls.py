from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger文档视图
schema_view = get_schema_view(
    openapi.Info(
        title="觅乡记 API",
        default_version='v1',
        description="觅乡记乡村旅游平台API文档",
        terms_of_service="https://www.miaxiangji.com/terms/",
        contact=openapi.Contact(email="contact@miaxiangji.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 用户端API路由
user_api_patterns = [
    path('auth/', include('apps.api_user.urls.auth_urls')),
    path('profile/', include('apps.api_user.urls.profile_urls')),
    # 用户端业务路由
    path('regions/', include('apps.regions.urls')),
    path('villages/', include('apps.villages.urls.village_urls')),
    path('attractions/', include('apps.villages.urls.attraction_urls')),
    path('homestays/', include('apps.homestays.urls.homestay_urls')),
    path('products/', include('apps.products.urls.product_urls')),
    path('foods/', include('apps.products.urls.food_urls')),
    path('cart/', include('apps.orders.urls.cart_urls')),
    path('orders/', include('apps.orders.urls.order_urls')),
    path('favorites/', include('apps.users.urls.favorite_urls')),
]

# 商户端API路由
merchant_api_patterns = [
    path('auth/', include('apps.api_merchant.urls.auth_urls')),
    path('dashboard/', include('apps.api_merchant.urls.dashboard_urls')),
    path('user/', include('apps.api_merchant.urls.user_urls')),
    # 商户端业务路由
    path('homestays/', include('apps.homestays.urls.homestay_urls')),
    path('products/', include('apps.products.urls.product_urls')),
    path('orders/', include('apps.orders.urls.order_urls')),
    # 添加商户端专用路由
    path('orders/', include('apps.api_merchant.urls.order_urls')),
    path('statistics/', include('apps.api_merchant.urls.dashboard_urls')),
    path('profile/', include('apps.api_merchant.urls.profile_urls')),
    path('settings/', include('apps.api_merchant.urls.profile_urls')),
]

# 管理端API路由
admin_api_patterns = [
    path('auth/', include('apps.api_admin.urls.auth_urls')),
    # 管理端业务路由
    path('users/', include('apps.users.urls.user_urls')),
    # path('merchants/', include('apps.users.urls.merchant_urls')),  # 文件已删除，功能移到admin端
    path('regions/', include('apps.regions.urls')),
    path('villages/', include('apps.villages.urls.village_urls')),
    path('homestays/', include('apps.homestays.urls.homestay_urls')),
    path('products/', include('apps.products.urls.product_urls')),
    path('orders/', include('apps.orders.urls.order_urls')),
    path('system/', include('apps.admin.urls')),
]

# 多端API总路由
api_v1_patterns = [
    path('user/', include((user_api_patterns, 'user_api'))),
    path('merchant/', include((merchant_api_patterns, 'merchant_api'))),
    path('admin/', include((admin_api_patterns, 'admin_api'))),
]

# 兼容旧版API路由（逐步迁移）
# 注意：已删除的冗余认证和商户管理路由
legacy_api_patterns = [
    # path('auth/', include('apps.users.urls.auth_urls')),  # 已删除，使用新的多端认证
    path('users/', include('apps.users.urls.user_urls')),
    # path('merchants/', include('apps.users.urls.merchant_urls')),  # 已删除，移到admin端
    path('regions/', include('apps.regions.urls')),
    path('villages/', include('apps.villages.urls.village_urls')),
    path('attractions/', include('apps.villages.urls.attraction_urls')),
    path('homestays/', include('apps.homestays.urls.homestay_urls')),
    path('room-types/', include('apps.homestays.urls.room_urls')),
    path('categories/', include('apps.products.urls.category_urls')),
    path('products/', include('apps.products.urls.product_urls')),
    path('foods/', include('apps.products.urls.food_urls')),
    path('cart/', include('apps.orders.urls.cart_urls')),
    path('orders/', include('apps.orders.urls.order_urls')),
    path('payment/', include('apps.orders.urls.payment_urls')),
    path('favorites/', include('apps.users.urls.favorite_urls')),
    # path('merchant/', include('apps.users.urls.merchant_manage_urls')),  # 已删除，移到merchant端
    path('admin/', include('apps.admin.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # API文档
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # 直接用户端API路由（与前端匹配）
    path('api/user/', include((user_api_patterns, 'user_api_direct'))),
    path('api/merchant/', include((merchant_api_patterns, 'merchant_api_direct'))),
    path('api/admin/', include((admin_api_patterns, 'admin_api_direct'))),
    # 新版多端API路由
    path('api/v1/', include(api_v1_patterns)),
    # 兼容旧版API路由（逐步迁移）
    path('api/legacy/', include(legacy_api_patterns)),
]