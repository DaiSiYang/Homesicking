from django.db.models import F, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Product
from ..serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(ListAPIView):
    """
    特产列表视图
    """
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        print("--- ProductListView: get_queryset called ---") # 新增打印
        print(f"Request query_params: {self.request.query_params}") # 新增打印
        
        queryset = Product.objects.filter(status='approved')
        print(f"Initial queryset count (status='approved'): {queryset.count()}") # 新增打印
        
        # 根据乡村筛选
        village_id = self.request.query_params.get('village_id')
        if village_id:
            queryset = queryset.filter(village_id=village_id)
            print(f"After village_id filter ({village_id}): {queryset.count()}") # 新增打印
        
        # 根据类别筛选
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            print(f"After category_id filter ({category_id}): {queryset.count()}") # 新增打印
        
        # 根据价格范围筛选
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(
                Q(discount_price__gte=float(min_price)) | 
                Q(discount_price__isnull=True, price__gte=float(min_price))
            )
            print(f"After min_price filter ({min_price}): {queryset.count()}") # 新增打印
        if max_price:
            queryset = queryset.filter(
                Q(discount_price__lte=float(max_price), discount_price__isnull=False) | 
                Q(discount_price__isnull=True, price__lte=float(max_price))
            )
            print(f"After max_price filter ({max_price}): {queryset.count()}") # 新增打印
        
        # 根据特色筛选
        is_featured = self.request.query_params.get('is_featured')
        if is_featured:
            is_featured_value = is_featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured_value)
            print(f"After is_featured filter ({is_featured_value}): {queryset.count()}") # 新增打印
        
        # 根据评分筛选
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))
            print(f"After min_rating filter ({min_rating}): {queryset.count()}") # 新增打印
        
        # 搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(intro__icontains=keyword) |
                Q(village__name__icontains=keyword)
            )
            print(f"After keyword filter ('{keyword}'): {queryset.count()}") # 新增打印
        
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
        elif sort_by == 'sales':
            order_field = '-sales' if sort_order == 'desc' else 'sales'
            queryset = queryset.order_by(order_field)
        elif sort_by == 'rating':
            order_field = '-rating' if sort_order == 'desc' else 'rating'
            queryset = queryset.order_by(order_field)
        else:
            order_field = '-created_at' if sort_order == 'desc' else 'created_at'
            queryset = queryset.order_by(order_field)
        
        print(f"Final queryset count before sorting: {queryset.count()}") # 新增打印
        # 可以在这里打印queryset中的一些具体数据，例如前几个产品的名称
        # for product in queryset[:3]: 
        #     print(f"  - Product ID: {product.id}, Name: {product.name}, Cover Image: {product.cover_image}")

        return queryset
    
    def list(self, request, *args, **kwargs):
        print("--- ProductListView: list method called ---") # 新增打印
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(f"Serialized page data count: {len(serializer.data)}") # 新增打印
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        print(f"Serialized queryset data count: {len(serializer.data)}") # 新增打印
        return ApiResponse(data=serializer.data)


class ProductDetailView(RetrieveAPIView):
    """
    特产详情视图
    """
    queryset = Product.objects.filter(status='approved')
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        print(f"--- ProductDetailView: retrieve called for pk: {kwargs.get('pk')} ---") # 新增打印
        instance = self.get_object()
        print(f"Instance found: {instance.name if instance else 'None'}") # 新增打印
        if instance:
            print(f"  Cover Image: {instance.cover_image}")
            if hasattr(instance, 'gallery') and instance.gallery.exists():
                print(f"  Gallery images count: {instance.gallery.count()}")
                for img in instance.gallery.all():
                    print(f"    - Gallery Image URL: {img.image_url}")
            else:
                print("  No gallery images or gallery attribute missing.")

        # 增加浏览量
        Product.objects.filter(id=instance.id).update(views=F('views') + 1)
        
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data)


class FeaturedProductView(APIView):
    """
    推荐特产视图
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        village_id = request.query_params.get('village_id')
        
        # 获取推荐特产
        queryset = Product.objects.filter(status='approved', is_featured=True)
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        
        queryset = queryset[:6]
        serializer = ProductListSerializer(queryset, many=True)
        
        return ApiResponse(data=serializer.data)