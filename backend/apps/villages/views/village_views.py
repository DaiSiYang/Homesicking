from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Village
from ..serializers import VillageListSerializer, VillageDetailSerializer


class VillageListView(ListAPIView):
    """
    乡村列表视图
    """
    serializer_class = VillageListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Village.objects.filter(status='approved')
        
        # 根据区域筛选
        region_id = self.request.query_params.get('region_id')
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        
        # 根据推荐状态筛选
        is_recommended = self.request.query_params.get('is_recommended')
        if is_recommended:
            is_recommended_value = is_recommended.lower() == 'true'
            queryset = queryset.filter(is_recommended=is_recommended_value)
        
        # 搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        
        # 排序
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        sort_order = self.request.query_params.get('sort_order', 'desc')
        
        if sort_by == 'rating':
            order_field = '-rating' if sort_order == 'desc' else 'rating'
        elif sort_by == 'views':
            order_field = '-views' if sort_order == 'desc' else 'views'
        else:  # 默认按创建时间
            order_field = '-created_at' if sort_order == 'desc' else 'created_at'
        
        return queryset.order_by(order_field)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(f"--- Village List API Response ---")
        print(response.data)
        print(f"---------------------------------")
        return response


class VillageDetailView(RetrieveAPIView):
    """
    乡村详情视图
    """
    queryset = Village.objects.filter(status='approved')
    serializer_class = VillageDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        print(f"--- Village Detail API Response (ID: {kwargs.get('pk')}) ---")
        print(response.data)
        print(f"------------------------------------------------------")
        return response


class RecommendedVillageView(APIView):
    """
    推荐乡村视图
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        # 获取推荐乡村
        queryset = Village.objects.filter(status='approved', is_recommended=True)[:5]
        serializer = VillageListSerializer(queryset, many=True)
        
        return ApiResponse(data=serializer.data)