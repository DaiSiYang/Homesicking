from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.utils.response import ApiResponse
from apps.utils.permissions import IsAdminUser
from apps.users.models import User
from apps.orders.models import Order
from apps.homestays.models import Homestay
from apps.products.models import Product
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_stats(request):
    """获取仪表板统计数据"""
    try:
        # 统计数据
        total_users = User.objects.filter(user_type='user').count()
        total_merchants = User.objects.filter(user_type='merchant').count()
        total_orders = Order.objects.count()
        total_income = Order.objects.filter(status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # 今日数据
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today).count()
        today_income = Order.objects.filter(
            created_at__date=today, 
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # 本月数据
        month_start = today.replace(day=1)
        month_orders = Order.objects.filter(created_at__date__gte=month_start).count()
        month_income = Order.objects.filter(
            created_at__date__gte=month_start,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        data = {
            'total_users': total_users,
            'total_merchants': total_merchants,
            'total_orders': total_orders,
            'total_income': float(total_income),
            'today_orders': today_orders,
            'today_income': float(today_income),
            'month_orders': month_orders,
            'month_income': float(month_income),
        }
        
        return ApiResponse.success(data=data)
    except Exception as e:
        return ApiResponse.error(message=f"获取统计数据失败: {str(e)}")

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def recent_activities(request):
    """获取最近活动"""
    try:
        limit = int(request.GET.get('limit', 10))
        
        # 获取最近的订单、用户注册等活动
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:limit//2]
        recent_users = User.objects.filter(user_type='user').order_by('-date_joined')[:limit//2]
        
        activities = []
        
        # 添加订单活动
        for order in recent_orders:
            activities.append({
                'id': f'order_{order.id}',
                'type': 'order',
                'title': f'新订单 {order.order_no}',  # 修改：order_number -> order_no
                'description': f'用户 {order.user.username} 下单 ¥{order.total_amount}',
                'time': order.created_at.isoformat(),
                'status': order.status
            })
        
        # 添加用户注册活动
        for user in recent_users:
            activities.append({
                'id': f'user_{user.id}',
                'type': 'user',
                'title': '新用户注册',
                'description': f'用户 {user.username} 注册了账号',
                'time': user.date_joined.isoformat(),
                'status': 'active'
            })
        
        # 按时间排序
        activities.sort(key=lambda x: x['time'], reverse=True)
        
        return ApiResponse.success(data={
            'results': activities[:limit],
            'count': len(activities)
        })
    except Exception as e:
        return ApiResponse.error(message=f"获取最近活动失败: {str(e)}")

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def todo_list(request):
    """获取待办事项"""
    try:
        todos = []
        
        # 待审核的商户
        pending_merchants = User.objects.filter(
            user_type='merchant', 
            merchant_profile__status='pending'
        ).count()
        if pending_merchants > 0:
            todos.append({
                'id': 'pending_merchants',
                'type': '商户审核',
                'title': f'有 {pending_merchants} 个商户待审核',
                'priority': 'high',
                'url': '/merchants'
            })
        
        # 待处理的退款
        pending_refunds = Order.objects.filter(status='refund_requested').count()
        if pending_refunds > 0:
            todos.append({
                'id': 'pending_refunds',
                'type': '退款处理',
                'title': f'有 {pending_refunds} 个退款申请待处理',
                'priority': 'high',
                'url': '/orders'
            })
        
        # 待审核的产品
        pending_products = Product.objects.filter(status='pending').count()
        if pending_products > 0:
            todos.append({
                'id': 'pending_products',
                'type': '产品审核',
                'title': f'有 {pending_products} 个产品待审核',
                'priority': 'medium',
                'url': '/products'
            })
        
        return ApiResponse.success(data=todos)
    except Exception as e:
        return ApiResponse.error(message=f"获取待办事项失败: {str(e)}")