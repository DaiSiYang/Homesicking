
from rest_framework.decorators import api_view
from apps.services.user_service import UserService
from apps.utils.permissions import user_api_permission
from apps.utils.response import ApiResponse

@api_view(['GET'])
@user_api_permission
def get_user_profile(request):
    """获取用户资料"""
    try:
        profile = UserService.get_user_profile(request.user)
        return ApiResponse.success(data=profile, message="获取用户资料成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取用户资料失败: {str(e)}")

@api_view(['PUT'])
@user_api_permission
def update_user_profile(request):
    """更新用户资料"""
    try:
        profile = UserService.update_user_profile(request.user, request.data)
        return ApiResponse.success(data=profile, message="更新用户资料成功")
    except Exception as e:
        return ApiResponse.error(message=f"更新用户资料失败: {str(e)}")
