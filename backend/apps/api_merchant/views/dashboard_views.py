
from rest_framework.decorators import api_view
from apps.services.merchant_service import MerchantService
from apps.utils.permissions import merchant_api_permission
from apps.utils.response import ApiResponse

@api_view(['GET'])
@merchant_api_permission
def get_dashboard_data(request):
    """获取商户仪表盘数据"""
    try:
        data = MerchantService.get_dashboard_data(request.user)
        return ApiResponse.success(data=data, message="获取仪表盘数据成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取仪表盘数据失败: {str(e)}")
