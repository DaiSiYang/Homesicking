from django.db.models import F, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Food
from ..serializers import FoodListSerializer, FoodDetailSerializer


class FoodListView(ListAPIView):
    """
    美食列表视图
    """
    serializer_class = FoodListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Food.objects.filter(status='approved')
        
        # 根据乡村筛选
        village_id = self.request.query_params.get('village_id')
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        
        # 根据类别筛选
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 根据价格范围筛选
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(
                Q(discount_price__gte=float(min_price)) | 
                Q(discount_price__isnull=True, price__gte=float(min_price))
            )
        if max_price:
            queryset = queryset.filter(
                Q(discount_price__lte=float(max_price), discount_price__isnull=False) | 
                Q(discount_price__isnull=True, price__lte=float(max_price))
            )
        
        # 根据特色筛选
        is_featured = self.request.query_params.get('is_featured')
        if is_featured:
            is_featured_value = is_featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured_value)
        
        # 根据评分筛选
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))
        
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
            if sort_order == 'asc':
                queryset = queryset.order_by(
                    F('discount_price').asc(nulls_last=True),
                    'price'
                )
            else:
                queryset = queryset.order_by(
                    F('discount_price').desc(nulls_last=True),
                    '-price'
                )
        elif sort_by == 'rating':
            order_field = '-rating' if sort_order == 'desc' else 'rating'
            queryset = queryset.order_by(order_field)
        else:
            order_field = '-created_at' if sort_order == 'desc' else 'created_at'
            queryset = queryset.order_by(order_field)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data)


class FoodDetailView(RetrieveAPIView):
    """
    美食详情视图
    """
    queryset = Food.objects.filter(status='approved')
    serializer_class = FoodDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 增加浏览量
        Food.objects.filter(id=instance.id).update(views=F('views') + 1)
        
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data)


class FeaturedFoodView(APIView):
    """
    推荐美食视图
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        village_id = request.query_params.get('village_id')
        
        # 获取推荐美食
        queryset = Food.objects.filter(status='approved', is_featured=True)
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        
        queryset = queryset[:6]
        serializer = FoodListSerializer(queryset, many=True)
        
        return ApiResponse(data=serializer.data) 