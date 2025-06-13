
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from apps.services.auth_service import AuthService
from apps.utils.permissions import merchant_api_permission
from apps.utils.response import ApiResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def merchant_login(request):
    """商户登录"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return ApiResponse.error(message="用户名和密码不能为空")
        
        result, error_message = AuthService.merchant_login(username, password, request)
        
        if result:
            return ApiResponse.success(data=result, message="商户登录成功")
        else:
            return ApiResponse.error(message=error_message or "登录失败")
    except Exception as e:
        return ApiResponse.error(message=f"商户登录失败: {str(e)}")

@api_view(['POST'])
@permission_classes([AllowAny])
def merchant_register(request):
    """商户注册"""
    try:
        result = AuthService.merchant_register(request.data)
        return ApiResponse.created(data=result, message="商户注册成功")
    except Exception as e:
        return ApiResponse.error(message=f"商户注册失败: {str(e)}")
