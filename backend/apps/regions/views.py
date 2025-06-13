from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from apps.utils.response import ApiResponse
from .models import Region
from .serializers import RegionSerializer, RegionDetailSerializer


class RegionListView(ListAPIView):
    """
    区域列表视图
    """
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Region.objects.filter(status='active')
        
        # 根据父级ID筛选
        parent_id = self.request.query_params.get('parent_id')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        else:
            # 如果未指定父级，默认返回省级区域
            queryset = queryset.filter(level='province')
        
        # 根据级别筛选
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # 是否热门
        is_hot = self.request.query_params.get('is_hot')
        if is_hot:
            is_hot_value = is_hot.lower() == 'true'
            queryset = queryset.filter(is_hot=is_hot_value)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data)


class RegionDetailView(RetrieveAPIView):
    """
    区域详情视图
    """
    queryset = Region.objects.filter(status='active')
    serializer_class = RegionDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data) 