from datetime import datetime
import uuid
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import CartItem, Order, OrderItem, Payment
from ..serializers import OrderSerializer, OrderCreateSerializer
from apps.products.models import Product, Food
from apps.homestays.models import RoomType, RoomInventory


class OrderListView(ListAPIView):
    """
    订单列表视图
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        
        # 根据订单状态筛选
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # 根据订单类型筛选
        order_type = self.request.query_params.get('type')
        if order_type:
            queryset = queryset.filter(order_type=order_type)
        
        # 时间范围筛选
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data)


class OrderDetailView(RetrieveAPIView):
    """
    订单详情视图
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data)


class OrderCreateView(APIView):
    """
    创建订单视图
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart_ids = serializer.validated_data.get('cart_ids', [])
        if not cart_ids:
            return ApiResponse(
                code=400,
                message="请选择要购买的商品",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取购物车项
        cart_items = CartItem.objects.filter(id__in=cart_ids, user=request.user)
        if not cart_items or cart_items.count() != len(cart_ids):
            return ApiResponse(
                code=400,
                message="购物车中的部分商品不存在",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查商品类型是否一致
        item_types = set(item.item_type for item in cart_items)
        if len(item_types) > 1:
            return ApiResponse(
                code=400,
                message="不同类型的商品需要分开下单",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查商品是否来自同一商户
        if item_types.pop() == 'product':
            merchant_ids = set(item.product.merchant_id for item in cart_items if item.product)
            if len(merchant_ids) > 1:
                return ApiResponse(
                    code=400,
                    message="不同商户的商品需要分开下单",
                    status=status.HTTP_400_BAD_REQUEST
                )
            merchant_id = merchant_ids.pop()
            order_type = 'product'
        elif item_types.pop() == 'food':
            merchant_ids = set(item.food.merchant_id for item in cart_items if item.food)
            if len(merchant_ids) > 1:
                return ApiResponse(
                    code=400,
                    message="不同商户的商品需要分开下单",
                    status=status.HTTP_400_BAD_REQUEST
                )
            merchant_id = merchant_ids.pop()
            order_type = 'food'
        elif item_types.pop() == 'room':
            merchant_ids = set(item.room_type.homestay.merchant_id for item in cart_items if item.room_type)
            if len(merchant_ids) > 1:
                return ApiResponse(
                    code=400,
                    message="不同民宿的房间需要分开下单",
                    status=status.HTTP_400_BAD_REQUEST
                )
            merchant_id = merchant_ids.pop()
            order_type = 'room'
        else:
            return ApiResponse(
                code=400,
                message="无效的商品类型",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建订单
        order_no = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8]}"
        total_amount = 0
        
        order = Order.objects.create(
            order_no=order_no,
            user=request.user,
            merchant_id=merchant_id,
            order_type=order_type,
            total_amount=0,  # 临时值，稍后更新
            payment_amount=0,  # 临时值，稍后更新
            status='pending_payment',
            contact_name=serializer.validated_data.get('contact_name'),
            contact_phone=serializer.validated_data.get('contact_phone'),
            contact_email=serializer.validated_data.get('contact_email', ''),
            remark=serializer.validated_data.get('remark', '')
        )
        
        # 创建订单项并计算总金额
        for cart_item in cart_items:
            if cart_item.item_type == 'product' and cart_item.product:
                product = cart_item.product
                price = product.discount_price or product.price
                amount = price * cart_item.quantity
                
                # 检查库存
                if product.stock < cart_item.quantity:
                    transaction.set_rollback(True)
                    return ApiResponse(
                        code=400,
                        message=f"商品 {product.name} 库存不足",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # 创建订单项
                OrderItem.objects.create(
                    order=order,
                    item_type='product',
                    product=product,
                    name=product.name,
                    image=product.cover_image,
                    price=price,
                    quantity=cart_item.quantity,
                    amount=amount
                )
                
                # 更新库存
                Product.objects.filter(id=product.id).update(
                    stock=product.stock - cart_item.quantity,
                    sales=product.sales + cart_item.quantity
                )
                
                total_amount += amount
            
            elif cart_item.item_type == 'food' and cart_item.food:
                food = cart_item.food
                price = food.discount_price or food.price
                amount = price * cart_item.quantity
                
                # 创建订单项
                OrderItem.objects.create(
                    order=order,
                    item_type='food',
                    food=food,
                    name=food.name,
                    image=food.cover_image,
                    price=price,
                    quantity=cart_item.quantity,
                    amount=amount
                )
                
                total_amount += amount
            
            elif cart_item.item_type == 'room' and cart_item.room_type:
                room_type = cart_item.room_type
                
                if not cart_item.check_in_date or not cart_item.check_out_date:
                    transaction.set_rollback(True)
                    return ApiResponse(
                        code=400,
                        message="房间订单需要提供入住和退房日期",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # 检查可用性
                inventories = RoomInventory.objects.filter(
                    room_type=room_type,
                    date__gte=cart_item.check_in_date,
                    date__lt=cart_item.check_out_date
                )
                
                if not inventories or any(inv.available < cart_item.quantity for inv in inventories):
                    transaction.set_rollback(True)
                    return ApiResponse(
                        code=400,
                        message=f"房型 {room_type.name} 在所选日期内库存不足",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # 计算总价
                days = (cart_item.check_out_date - cart_item.check_in_date).days
                total_price = sum(inv.current_price for inv in inventories)
                
                # 创建订单项
                OrderItem.objects.create(
                    order=order,
                    item_type='room',
                    room_type=room_type,
                    name=room_type.name,
                    image=room_type.cover_image,
                    price=total_price / days if days > 0 else 0,
                    quantity=cart_item.quantity,
                    amount=total_price * cart_item.quantity,
                    check_in_date=cart_item.check_in_date,
                    check_out_date=cart_item.check_out_date,
                    days=days
                )
                
                # 更新库存
                for inv in inventories:
                    inv.available -= cart_item.quantity
                    inv.save()
                
                total_amount += total_price * cart_item.quantity
        
        # 更新订单总金额
        order.total_amount = total_amount
        order.payment_amount = total_amount
        order.save()
        
        # 删除已购买的购物车项
        cart_items.delete()
        
        return ApiResponse(
            message="订单创建成功",
            data={
                'order_id': order.id,
                'order_no': order.order_no,
                'total_amount': order.total_amount
            }
        )


class OrderCancelView(APIView):
    """
    取消订单视图
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        
        # 只有待支付的订单可以取消
        if order.status != 'pending_payment':
            return ApiResponse(
                code=400,
                message="只有待支付的订单可以取消",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 取消订单并恢复库存
        order_items = OrderItem.objects.filter(order=order)
        
        for item in order_items:
            if item.item_type == 'product' and item.product:
                # 恢复特产库存
                Product.objects.filter(id=item.product.id).update(
                    stock=item.product.stock + item.quantity,
                    sales=item.product.sales - item.quantity
                )
            
            elif item.item_type == 'room' and item.room_type and item.check_in_date and item.check_out_date:
                # 恢复房间库存
                inventories = RoomInventory.objects.filter(
                    room_type=item.room_type,
                    date__gte=item.check_in_date,
                    date__lt=item.check_out_date
                )
                
                for inv in inventories:
                    inv.available += item.quantity
                    inv.save()
        
        # 更新订单状态
        order.status = 'canceled'
        order.canceled_at = timezone.now()
        order.save()
        
        return ApiResponse(message="订单已取消") 