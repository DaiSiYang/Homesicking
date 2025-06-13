from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.services.product_service import ProductService
from apps.utils.permissions import user_api_permission
from apps.utils.response import ApiResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """获取产品列表"""
    try:
        result = ProductService.get_product_list(request.GET)
        return ApiResponse.success(data=result, message="获取产品列表成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取产品列表失败: {str(e)}")

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, pk):
    """获取产品详情"""
    try:
        result = ProductService.get_product_detail(pk)
        return ApiResponse.success(data=result, message="获取产品详情成功")
    except Exception as e:
        return ApiResponse.not_found(message=f"产品不存在: {str(e)}")

@api_view(['GET'])
@permission_classes([AllowAny])
def product_categories(request):
    """获取产品分类"""
    try:
        result = ProductService.get_product_categories()
        return ApiResponse.success(data=result, message="获取产品分类成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取产品分类失败: {str(e)}")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_favorite(request, pk):
    """切换产品收藏状态"""
    try:
        result = ProductService.toggle_favorite(request.user, pk)
        return ApiResponse.success(data=result, message="收藏状态切换成功")
    except Exception as e:
        return ApiResponse.error(message=f"操作失败: {str(e)}")