from django.urls import path
from apps.api_admin.views import auth_views

urlpatterns = [
    path('login/', auth_views.admin_login, name='admin-login'),
    path('register/', auth_views.admin_register, name='admin-register'),  # 新增注册路由
    path('logout/', auth_views.admin_logout, name='admin-logout'),
    path('profile/', auth_views.admin_profile, name='admin-profile'),
]