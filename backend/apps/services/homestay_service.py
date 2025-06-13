from django.core.paginator import Paginator
from apps.homestays.models import Homestay
from apps.homestays.serializers import HomestaySerializer
from apps.users.models import UserFavorite

class HomestayService:
    """民宿服务"""
    
    @staticmethod
    def get_homestay_list(params):
        """获取民宿列表"""
        queryset = Homestay.objects.filter(is_active=True)
        
        # 搜索过滤
        search = params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # 地区过滤
        region = params.get('region')
        if region:
            queryset = queryset.filter(village__region_id=region)
        
        # 村庄过滤
        village = params.get('village')
        if village:
            queryset = queryset.filter(village_id=village)
        
        # 价格范围过滤
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        
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
            'results': HomestaySerializer(page_obj, many=True).data
        }
    
    @staticmethod
    def get_homestay_detail(homestay_id):
        """获取民宿详情"""
        try:
            homestay = Homestay.objects.get(id=homestay_id, is_active=True)
            return HomestaySerializer(homestay).data
        except Homestay.DoesNotExist:
            raise Exception('民宿不存在')
    
    @staticmethod
    def get_featured_homestays():
        """获取推荐民宿"""
        queryset = Homestay.objects.filter(is_active=True, is_featured=True)[:6]
        return HomestaySerializer(queryset, many=True).data
    
    @staticmethod
    def toggle_favorite(user, homestay_id):
        """切换民宿收藏状态"""
        try:
            homestay = Homestay.objects.get(id=homestay_id, is_active=True)
        except Homestay.DoesNotExist:
            raise Exception('民宿不存在')
        
        favorite, created = UserFavorite.objects.get_or_create(
            user=user,
            content_type_id=homestay._meta.get_field('id').model._meta.pk.model._meta.pk,
            object_id=homestay_id,
            defaults={'favorite_type': 'homestay'}
        )
        
        if not created:
            favorite.delete()
            return {'is_favorited': False, 'message': '已取消收藏'}
        else:
            return {'is_favorited': True, 'message': '已添加收藏'}