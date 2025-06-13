
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from apps.services.auth_service import AuthService
from apps.utils.permissions import admin_api_permission
from apps.utils.response import ApiResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """管理员登录"""
    try:
        result = AuthService.admin_login(request.data)
        return ApiResponse.success(data=result, message="管理员登录成功")
    except Exception as e:
        return ApiResponse.error(message=f"管理员登录失败: {str(e)}")
