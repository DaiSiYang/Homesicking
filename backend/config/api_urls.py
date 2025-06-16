
from django.urls import path, include

# 用户端API路由
user_api_patterns = [
    path('auth/', include('apps.api_user.urls.auth_urls')),
    path('profile/', include('apps.api_user.urls.profile_urls')),
    # 可以继续添加其他用户端路由
]

# 商户端API路由
merchant_api_patterns = [
    path('auth/', include('apps.api_merchant.urls.auth_urls')),
    path('dashboard/', include('apps.api_merchant.urls.dashboard_urls')),
    # 可以继续添加其他商户端路由
]

# 管理端API路由
admin_api_patterns = [
    path('auth/', include('apps.api_admin.urls.auth_urls')),
    path('dashboard/', include('apps.api_admin.urls.dashboard_urls')),
    path('users/', include('apps.api_admin.urls.user_urls')),
    path('merchants/', include('apps.api_admin.urls.merchant_urls')),
    path('products/', include('apps.api_admin.urls.product_urls')),
    path('homestays/', include('apps.api_admin.urls.homestay_urls')),
    path('orders/', include('apps.api_admin.urls.order_urls')),
    path('content/', include('apps.api_admin.urls.content_urls')),
    path('settings/', include('apps.api_admin.urls.settings_urls')),
]

# 多端API总路由
multi_api_patterns = [
    path('user/', include((user_api_patterns, 'user_api'))),
    path('merchant/', include((merchant_api_patterns, 'merchant_api'))),
    path('admin/', include((admin_api_patterns, 'admin_api'))),
]
