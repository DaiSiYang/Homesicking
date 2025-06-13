from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Attraction
from ..serializers import AttractionListSerializer, AttractionDetailSerializer


class AttractionListView(ListAPIView):
    """
    景点列表视图
    """
    serializer_class = AttractionListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Attraction.objects.filter(status='active')
        
        # 根据所属乡村筛选
        village_id = self.request.query_params.get('village_id')
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        
        # 票价筛选
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(ticket_price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(ticket_price__lte=float(max_price))
        
        # 搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data)


class AttractionDetailView(RetrieveAPIView):
    """
    景点详情视图
    """
    queryset = Attraction.objects.filter(status='active')
    serializer_class = AttractionDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data) 