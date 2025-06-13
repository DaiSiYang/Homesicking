from rest_framework.decorators import api_view
from apps.services.merchant_service import MerchantService
from apps.utils.permissions import merchant_api_permission
from apps.utils.response import ApiResponse

@api_view(['GET', 'PUT'])
@merchant_api_permission
def merchant_profile(request):
    """获取/更新商户档案信息"""
    try:
        if request.method == 'GET':
            profile = MerchantService.get_merchant_profile(request.user)
            return ApiResponse.success(data=profile, message="获取商户信息成功")
        elif request.method == 'PUT':
            profile = MerchantService.update_merchant_profile(request.user, request.data)
            return ApiResponse.success(data=profile, message="更新商户信息成功")
    except Exception as e:
        return ApiResponse.error(message=f"操作失败: {str(e)}")

@api_view(['GET', 'PUT'])
@merchant_api_permission
def notification_settings(request):
    """获取/更新通知设置"""
    try:
        if request.method == 'GET':
            settings = MerchantService.get_notification_settings(request.user)
            return ApiResponse.success(data=settings, message="获取通知设置成功")
        elif request.method == 'PUT':
            settings = MerchantService.update_notification_settings(request.user, request.data)
            return ApiResponse.success(data=settings, message="更新通知设置成功")
    except Exception as e:
        return ApiResponse.error(message=f"操作失败: {str(e)}")