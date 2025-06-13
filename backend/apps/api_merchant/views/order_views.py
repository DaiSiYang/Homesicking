from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.services.merchant_service import MerchantService
from apps.utils.permissions import merchant_api_permission
from apps.utils.response import ApiResponse

@api_view(['GET'])
@merchant_api_permission
def get_recent_orders(request):
    """获取最近订单"""
    try:
        limit = int(request.GET.get('limit', 5))
        orders = MerchantService.get_recent_orders(request.user, limit)
        return ApiResponse.success(data=orders, message="获取最近订单成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取最近订单失败: {str(e)}")

@api_view(['GET'])
@merchant_api_permission
def get_merchant_orders(request):
    """获取商户订单列表"""
    try:
        orders = MerchantService.get_merchant_orders(request.user, request.GET)
        return ApiResponse.success(data=orders, message="获取订单列表成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取订单列表失败: {str(e)}")