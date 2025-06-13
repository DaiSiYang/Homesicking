
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.services.auth_service import AuthService
from apps.utils.permissions import user_api_permission
from apps.utils.response import ApiResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """用户登录"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return ApiResponse.error(message="用户名和密码不能为空")
        
        result, error = AuthService.user_login(username, password, request)
        
        if error:
            return ApiResponse.error(message=error)
        
        return ApiResponse.success(data=result, message="登录成功")
        
    except Exception as e:
        return ApiResponse.server_error(message=f"登录失败: {str(e)}")

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """用户注册"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        if not username or not password or not email:
            return ApiResponse.error(message="用户名、密码和邮箱不能为空")
        
        result = AuthService.user_register(username, password, email, phone, request)
        return ApiResponse.created(data=result, message="注册成功")
    except Exception as e:
        return ApiResponse.error(message=f"注册失败: {str(e)}")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """用户登出"""
    try:
        result = AuthService.user_logout(request)
        return ApiResponse.success(data=result, message="登出成功")
    except Exception as e:
        return ApiResponse.error(message=f"登出失败: {str(e)}")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    try:
        result = AuthService.change_password(request.user, request.data)
        return ApiResponse.success(data=result, message="密码修改成功")
    except Exception as e:
        return ApiResponse.error(message=f"密码修改失败: {str(e)}")
