from django.db.models import F, Q
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Homestay
from ..serializers import HomestayListSerializer, HomestayDetailSerializer


class HomestayListView(ListAPIView):
    """
    民宿列表视图
    """
    serializer_class = HomestayListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Homestay.objects.filter(status='approved')
        
        # 根据乡村筛选
        village_id = self.request.query_params.get('village_id')
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        
        # 根据价格范围筛选
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(lowest_price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(lowest_price__lte=float(max_price))
        
        # 根据特色筛选
        is_featured = self.request.query_params.get('is_featured')
        if is_featured:
            is_featured_value = is_featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured_value)
        
        # 根据评分筛选
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))
        
        # 根据设施筛选
        # 由于设施是JSON字段，这里使用简化方式，实际项目中可能需要更复杂的查询
        facility = self.request.query_params.get('facility')
        if facility:
            queryset = queryset.filter(features__icontains=facility)
        
        # 搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(intro__icontains=keyword) |
                Q(village__name__icontains=keyword)
            )
        
        # 排序
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        sort_order = self.request.query_params.get('sort_order', 'desc')
        
        if sort_by == 'price':
            order_field = 'lowest_price' if sort_order == 'asc' else '-lowest_price'
        elif sort_by == 'rating':
            order_field = 'rating' if sort_order == 'asc' else '-rating'
        else:
            order_field = 'created_at' if sort_order == 'asc' else '-created_at'
        
        return queryset.order_by(order_field)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        # 添加查询日期到上下文
        context = {'today': request.query_params.get('date', timezone.now().date())}
        
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context=context)
        return ApiResponse(data=serializer.data)


class HomestayDetailView(RetrieveAPIView):
    """
    民宿详情视图
    """
    queryset = Homestay.objects.filter(status='approved')
    serializer_class = HomestayDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 增加浏览量
        Homestay.objects.filter(id=instance.id).update(views=F('views') + 1)
        
        # 添加查询日期范围到上下文
        context = {
            'today': request.query_params.get('date', timezone.now().date()),
            'check_in': request.query_params.get('check_in'),
            'check_out': request.query_params.get('check_out')
        }
        
        serializer = self.get_serializer(instance, context=context)
        return ApiResponse(data=serializer.data)


class FeaturedHomestayView(APIView):
    """
    特色民宿视图
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        # 获取特色民宿
        queryset = Homestay.objects.filter(status='approved', is_featured=True)[:5]
        serializer = HomestayListSerializer(queryset, many=True)
        
        return ApiResponse(data=serializer.data) 