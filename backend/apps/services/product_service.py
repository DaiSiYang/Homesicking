from django.core.paginator import Paginator
from apps.products.models import Product, ProductCategory
from apps.products.serializers import ProductSerializer, ProductCategorySerializer
from apps.users.models import UserFavorite

class ProductService:
    """产品服务"""
    
    @staticmethod
    def get_product_list(params):
        """获取产品列表"""
        queryset = Product.objects.filter(is_active=True)
        
        # 搜索过滤
        search = params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # 分类过滤
        category = params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # 地区过滤
        region = params.get('region')
        if region:
            queryset = queryset.filter(merchant__village__region_id=region)
        
        # 村庄过滤
        village = params.get('village')
        if village:
            queryset = queryset.filter(merchant__village_id=village)
        
        # 价格范围过滤
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # 排序
        ordering = params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        # 分页
        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 10))
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'results': ProductSerializer(page_obj, many=True).data
        }
    
    @staticmethod
    def get_product_detail(product_id):
        """获取产品详情"""
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            return ProductSerializer(product).data
        except Product.DoesNotExist:
            raise Exception('产品不存在')
    
    @staticmethod
    def get_product_categories():
        """获取产品分类"""
        categories = ProductCategory.objects.filter(is_active=True)
        return ProductCategorySerializer(categories, many=True).data
    
    @staticmethod
    def toggle_favorite(user, product_id):
        """切换产品收藏状态"""
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            raise Exception('产品不存在')
        
        favorite, created = UserFavorite.objects.get_or_create(
            user=user,
            content_type_id=product._meta.get_field('id').model._meta.pk.model._meta.pk,
            object_id=product_id,
            defaults={'favorite_type': 'product'}
        )
        
        if not created:
            favorite.delete()
            return {'is_favorited': False, 'message': '已取消收藏'}
        else:
            return {'is_favorited': True, 'message': '已添加收藏'}