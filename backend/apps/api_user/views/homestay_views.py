from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.services.homestay_service import HomestayService
from apps.utils.permissions import user_api_permission
from apps.utils.response import ApiResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def homestay_list(request):
    """获取民宿列表"""
    try:
        result = HomestayService.get_homestay_list(request.GET)
        return ApiResponse.success(data=result, message="获取民宿列表成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取民宿列表失败: {str(e)}")

@api_view(['GET'])
@permission_classes([AllowAny])
def homestay_detail(request, pk):
    """获取民宿详情"""
    try:
        result = HomestayService.get_homestay_detail(pk)
        return ApiResponse.success(data=result, message="获取民宿详情成功")
    except Exception as e:
        return ApiResponse.not_found(message=f"民宿不存在: {str(e)}")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def homestay_favorite(request, pk):
    """切换民宿收藏状态"""
    try:
        result = HomestayService.toggle_favorite(request.user, pk)
        return ApiResponse.success(data=result, message="收藏状态切换成功")
    except Exception as e:
        return ApiResponse.error(message=f"操作失败: {str(e)}")

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_homestays(request):
    """获取推荐民宿"""
    try:
        result = HomestayService.get_featured_homestays()
        return ApiResponse.success(data=result, message="获取推荐民宿成功")
    except Exception as e:
        return ApiResponse.error(message=f"获取推荐民宿失败: {str(e)}")