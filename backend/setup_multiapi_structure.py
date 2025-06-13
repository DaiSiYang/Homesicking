#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
觅乡记后端多端架构重构脚本
用于快速创建新的多端API架构
"""

import os
import sys
from pathlib import Path

def create_directory(path):
    """创建目录"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建目录: {path}")

def create_file(path, content=""):
    """创建文件"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ 创建文件: {path}")

def setup_api_user_app():
    """创建用户端API应用"""
    print("\n=== 创建用户端API应用 ===")
    
    base_path = "apps/api_user"
    create_directory(base_path)
    
    # 创建基础文件
    create_file(f"{base_path}/__init__.py")
    create_file(f"{base_path}/apps.py", '''
from django.apps import AppConfig

class ApiUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api_user'
    verbose_name = '用户端API'
''')
    
    # 创建视图目录
    views_path = f"{base_path}/views"
    create_directory(views_path)
    create_file(f"{views_path}/__init__.py")
    create_file(f"{views_path}/auth_views.py", '''
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.services.auth_service import AuthService
from apps.utils.permissions import user_api_permission

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """用户登录"""
    try:
        result = AuthService.user_login(request.data)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """用户注册"""
    try:
        result = AuthService.user_register(request.data)
        return Response(result, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
''')
    
    create_file(f"{views_path}/profile_views.py", '''
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.services.user_service import UserService
from apps.utils.permissions import user_api_permission

@api_view(['GET'])
@user_api_permission
def get_user_profile(request):
    """获取用户资料"""
    try:
        profile = UserService.get_user_profile(request.user)
        return Response(profile, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@user_api_permission
def update_user_profile(request):
    """更新用户资料"""
    try:
        profile = UserService.update_user_profile(request.user, request.data)
        return Response(profile, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
''')
    
    # 创建序列化器目录
    serializers_path = f"{base_path}/serializers"
    create_directory(serializers_path)
    create_file(f"{serializers_path}/__init__.py")
    create_file(f"{serializers_path}/user_serializers.py", '''
from rest_framework import serializers
from apps.users.models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """用户端用户资料序列化器"""
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar', 'phone', 'email', 'gender', 'birthday']
        
class UserSerializer(serializers.ModelSerializer):
    """用户端用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'date_joined']
        read_only_fields = ['id', 'date_joined']
''')
    
    # 创建URL配置
    urls_path = f"{base_path}/urls"
    create_directory(urls_path)
    create_file(f"{urls_path}/__init__.py")
    create_file(f"{urls_path}/auth_urls.py", '''
from django.urls import path
from apps.api_user.views import auth_views

urlpatterns = [
    path('login/', auth_views.user_login, name='user-login'),
    path('register/', auth_views.user_register, name='user-register'),
]
''')
    
    create_file(f"{urls_path}/profile_urls.py", '''
from django.urls import path
from apps.api_user.views import profile_views

urlpatterns = [
    path('', profile_views.get_user_profile, name='user-profile'),
    path('update/', profile_views.update_user_profile, name='user-profile-update'),
]
''')

def setup_api_merchant_app():
    """创建商户端API应用"""
    print("\n=== 创建商户端API应用 ===")
    
    base_path = "apps/api_merchant"
    create_directory(base_path)
    
    # 创建基础文件
    create_file(f"{base_path}/__init__.py")
    create_file(f"{base_path}/apps.py", '''
from django.apps import AppConfig

class ApiMerchantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api_merchant'
    verbose_name = '商户端API'
''')
    
    # 创建视图目录
    views_path = f"{base_path}/views"
    create_directory(views_path)
    create_file(f"{views_path}/__init__.py")
    create_file(f"{views_path}/auth_views.py", '''
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.services.auth_service import AuthService
from apps.utils.permissions import merchant_api_permission

@api_view(['POST'])
@permission_classes([AllowAny])
def merchant_login(request):
    """商户登录"""
    try:
        result = AuthService.merchant_login(request.data)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def merchant_register(request):
    """商户注册"""
    try:
        result = AuthService.merchant_register(request.data)
        return Response(result, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
''')
    
    create_file(f"{views_path}/dashboard_views.py", '''
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.services.merchant_service import MerchantService
from apps.utils.permissions import merchant_api_permission

@api_view(['GET'])
@merchant_api_permission
def get_dashboard_data(request):
    """获取商户仪表盘数据"""
    try:
        data = MerchantService.get_dashboard_data(request.user)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
''')

def setup_api_admin_app():
    """创建管理端API应用"""
    print("\n=== 创建管理端API应用 ===")
    
    base_path = "apps/api_admin"
    create_directory(base_path)
    
    # 创建基础文件
    create_file(f"{base_path}/__init__.py")
    create_file(f"{base_path}/apps.py", '''
from django.apps import AppConfig

class ApiAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api_admin'
    verbose_name = '管理端API'
''')
    
    # 创建视图目录
    views_path = f"{base_path}/views"
    create_directory(views_path)
    create_file(f"{views_path}/__init__.py")
    create_file(f"{views_path}/auth_views.py", '''
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.services.auth_service import AuthService
from apps.utils.permissions import admin_api_permission

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """管理员登录"""
    try:
        result = AuthService.admin_login(request.data)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
''')

def setup_services_app():
    """创建服务层应用"""
    print("\n=== 创建服务层应用 ===")
    
    base_path = "apps/services"
    create_directory(base_path)
    
    # 创建基础文件
    create_file(f"{base_path}/__init__.py")
    create_file(f"{base_path}/apps.py", '''
from django.apps import AppConfig

class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'
    verbose_name = '业务服务层'
''')
    
    # 创建服务文件
    create_file(f"{base_path}/auth_service.py", '''
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.users.serializers import UserSerializer

class AuthService:
    """认证服务"""
    
    @staticmethod
    def user_login(data):
        """用户登录"""
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user and user.user_type == 'customer':
            refresh = RefreshToken.for_user(user)
            return {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        raise Exception('用户名或密码错误')
    
    @staticmethod
    def merchant_login(data):
        """商户登录"""
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user and user.user_type == 'merchant':
            refresh = RefreshToken.for_user(user)
            return {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        raise Exception('商户名或密码错误')
    
    @staticmethod
    def admin_login(data):
        """管理员登录"""
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user and user.user_type in ['admin', 'super_admin']:
            refresh = RefreshToken.for_user(user)
            return {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        raise Exception('管理员账号或密码错误')
''')
    
    create_file(f"{base_path}/user_service.py", '''
from apps.users.models import User, UserProfile
from apps.api_user.serializers.user_serializers import UserSerializer, UserProfileSerializer

class UserService:
    """用户服务"""
    
    @staticmethod
    def get_user_profile(user):
        """获取用户资料"""
        serializer = UserSerializer(user)
        return serializer.data
    
    @staticmethod
    def update_user_profile(user, data):
        """更新用户资料"""
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return UserSerializer(user).data
        raise Exception('数据验证失败')
''')
    
    create_file(f"{base_path}/merchant_service.py", '''
from apps.orders.models import Order
from apps.products.models import Product
from apps.homestays.models import Homestay

class MerchantService:
    """商户服务"""
    
    @staticmethod
    def get_dashboard_data(user):
        """获取商户仪表盘数据"""
        # 获取商户的统计数据
        total_orders = Order.objects.filter(merchant=user).count()
        total_products = Product.objects.filter(merchant=user).count()
        total_homestays = Homestay.objects.filter(merchant=user).count()
        
        return {
            'total_orders': total_orders,
            'total_products': total_products,
            'total_homestays': total_homestays,
            'recent_orders': [],  # 最近订单
            'sales_stats': {},    # 销售统计
        }
''')

def update_permissions():
    """更新权限系统"""
    print("\n=== 更新权限系统 ===")
    
    permissions_content = '''
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

def user_api_permission(view_func):
    """用户端API权限装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # JWT认证
        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
            if user and user.user_type == 'customer':
                request.user = user
                return view_func(request, *args, **kwargs)
        except:
            pass
        return Response({'error': '用户认证失败'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper

def merchant_api_permission(view_func):
    """商户端API权限装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # JWT认证
        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
            if user and user.user_type == 'merchant':
                request.user = user
                return view_func(request, *args, **kwargs)
        except:
            pass
        return Response({'error': '商户认证失败'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper

def admin_api_permission(view_func):
    """管理端API权限装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # JWT认证
        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
            if user and user.user_type in ['admin', 'super_admin']:
                request.user = user
                return view_func(request, *args, **kwargs)
        except:
            pass
        return Response({'error': '管理员认证失败'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper
'''
    
    # 更新权限文件
    with open('apps/utils/permissions.py', 'a', encoding='utf-8') as f:
        f.write('\n\n# === 多端API权限装饰器 ===\n')
        f.write(permissions_content)
    
    print("✓ 更新权限系统完成")

def create_new_urls():
    """创建新的URL配置"""
    print("\n=== 创建新的URL配置 ===")
    
    # 创建多端API URL配置
    create_file("config/api_urls.py", '''
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
    # 可以继续添加其他管理端路由
]

# 多端API总路由
multi_api_patterns = [
    path('user/', include((user_api_patterns, 'user_api'))),
    path('merchant/', include((merchant_api_patterns, 'merchant_api'))),
    path('admin/', include((admin_api_patterns, 'admin_api'))),
]
''')

def main():
    """主函数"""
    print("觅乡记后端多端架构重构开始...")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists('manage.py'):
        print("❌ 请在Django项目根目录下运行此脚本")
        sys.exit(1)
    
    try:
        # 创建各个应用
        setup_api_user_app()
        setup_api_merchant_app()
        setup_api_admin_app()
        setup_services_app()
        
        # 更新权限系统
        update_permissions()
        
        # 创建新的URL配置
        create_new_urls()
        
        print("\n" + "=" * 50)
        print("✅ 多端架构重构完成！")
        print("\n📋 接下来需要手动完成的步骤:")
        print("1. 在 settings.py 中添加新的应用:")
        print("   - 'apps.api_user'")
        print("   - 'apps.api_merchant'")
        print("   - 'apps.api_admin'")
        print("   - 'apps.services'")
        print("\n2. 更新 config/urls.py 中的路由配置")
        print("\n3. 运行数据库迁移: python manage.py makemigrations && python manage.py migrate")
        print("\n4. 测试各端API功能")
        
    except Exception as e:
        print(f"❌ 重构过程中出现错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()