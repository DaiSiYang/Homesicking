
from apps.orders.models import Order
from apps.products.models import Product
from apps.homestays.models import Homestay
from apps.users.models import User

class MerchantService:
    """商户服务"""
    
    @staticmethod
    def get_dashboard_data(user):
        """获取商户仪表盘数据"""
        total_orders = Order.objects.filter(merchant=user).count()
        total_products = Product.objects.filter(merchant=user).count()
        total_homestays = Homestay.objects.filter(merchant=user).count()
        
        return {
            'total_orders': total_orders,
            'total_products': total_products,
            'total_homestays': total_homestays,
            'recent_orders': MerchantService.get_recent_orders(user, 5),
            'sales_stats': {},
        }
    
    @staticmethod
    def get_recent_orders(user, limit=5):
        """获取最近订单"""
        from apps.orders.serializers import OrderSerializer
        
        recent_orders = Order.objects.filter(
            merchant=user
        ).order_by('-created_at')[:limit]
        
        return OrderSerializer(recent_orders, many=True).data
    
    @staticmethod
    def get_merchant_orders(user, params):
        """获取商户订单列表"""
        from apps.orders.serializers import OrderSerializer
        from django.core.paginator import Paginator
        
        orders = Order.objects.filter(merchant=user).order_by('-created_at')
        
        # 分页
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 10))
        paginator = Paginator(orders, limit)
        page_obj = paginator.get_page(page)
        
        return {
            'results': OrderSerializer(page_obj.object_list, many=True).data,
            'total': paginator.count,
            'page': page,
            'pages': paginator.num_pages
        }
    
    @staticmethod
    def get_merchant_profile(user):
        """获取商户档案信息"""
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': getattr(user, 'shop_name', ''),
            'description': getattr(user, 'description', ''),
            'phone': getattr(user, 'phone', ''),
            'address': getattr(user, 'address', ''),
            'business_hours': getattr(user, 'business_hours', ''),
            'logo': getattr(user, 'logo', ''),
            'license': getattr(user, 'license', ''),
            'images': getattr(user, 'images', []),
        }
    
    @staticmethod
    def update_merchant_profile(user, data):
        """更新商户档案信息"""
        # 更新用户信息
        for field in ['shop_name', 'description', 'phone', 'address', 'business_hours', 'logo', 'license', 'images']:
            if field in data:
                setattr(user, field, data[field])
        user.save()
        
        return MerchantService.get_merchant_profile(user)
    
    @staticmethod
    def get_notification_settings(user):
        """获取通知设置"""
        return {
            'email_notifications': getattr(user, 'email_notifications', True),
            'sms_notifications': getattr(user, 'sms_notifications', True),
            'order_notifications': getattr(user, 'order_notifications', True),
            'marketing_notifications': getattr(user, 'marketing_notifications', False),
        }
    
    @staticmethod
    def update_notification_settings(user, data):
        """更新通知设置"""
        for field in ['email_notifications', 'sms_notifications', 'order_notifications', 'marketing_notifications']:
            if field in data:
                setattr(user, field, data[field])
        user.save()
        
        return MerchantService.get_notification_settings(user)
