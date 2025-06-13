from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import CartItem, Order, OrderItem, Payment, Refund
from apps.products.models import Product, Food
from apps.homestays.models import RoomType, RoomInventory


class CartItemSerializer(serializers.ModelSerializer):
    """购物车项序列化器"""
    item_name = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()
    item_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'user_id', 'item_type', 'product_id', 'food_id', 'room_type_id',
                 'item_name', 'item_image', 'item_price', 'quantity', 'total_price',
                 'check_in_date', 'check_out_date', 'created_at']
        read_only_fields = ['user_id', 'created_at']
    
    def get_item_name(self, obj):
        if obj.item_type == 'product' and obj.product:
            return obj.product.name
        elif obj.item_type == 'food' and obj.food:
            return obj.food.name
        elif obj.item_type == 'room' and obj.room_type:
            return obj.room_type.name
        return None
    
    def get_item_image(self, obj):
        if obj.item_type == 'product' and obj.product:
            return obj.product.cover_image
        elif obj.item_type == 'food' and obj.food:
            return obj.food.cover_image
        elif obj.item_type == 'room' and obj.room_type:
            return obj.room_type.cover_image
        return None
    
    def get_item_price(self, obj):
        if obj.item_type == 'product' and obj.product:
            return obj.product.discount_price or obj.product.price
        elif obj.item_type == 'food' and obj.food:
            return obj.food.discount_price or obj.food.price
        elif obj.item_type == 'room' and obj.room_type:
            # 如果是房间，返回每晚价格
            if obj.check_in_date and obj.check_out_date:
                # 获取该日期区间内的平均价格
                inventory = RoomInventory.objects.filter(
                    room_type=obj.room_type,
                    date__gte=obj.check_in_date,
                    date__lt=obj.check_out_date
                )
                if inventory.exists():
                    total_price = sum(inv.current_price for inv in inventory)
                    days = (obj.check_out_date - obj.check_in_date).days
                    return total_price / days if days > 0 else 0
            
            return obj.room_type.discount_price or obj.room_type.price
        return 0
    
    def get_total_price(self, obj):
        item_price = self.get_item_price(obj)
        
        if obj.item_type in ['product', 'food']:
            return item_price * obj.quantity
        elif obj.item_type == 'room' and obj.check_in_date and obj.check_out_date:
            # 计算天数
            days = (obj.check_out_date - obj.check_in_date).days
            return item_price * days
        return 0


class OrderItemSerializer(serializers.ModelSerializer):
    """订单项序列化器"""
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'item_type', 'product_id', 'food_id', 'room_type_id',
                 'name', 'image', 'price', 'quantity', 'amount', 'check_in_date',
                 'check_out_date', 'days', 'created_at']
        read_only_fields = ['id', 'order_id', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_no', 'user_id', 'merchant_id', 'order_type', 
                 'total_amount', 'payment_amount', 'status', 'status_display',
                 'contact_name', 'contact_phone', 'contact_email', 'remark',
                 'paid_at', 'canceled_at', 'refunded_at', 'completed_at',
                 'created_at', 'items']
        read_only_fields = ['id', 'order_no', 'user_id', 'merchant_id', 'created_at']
    
    def get_status_display(self, obj):
        return dict(Order.STATUS_CHOICES).get(obj.status, '')


class OrderCreateSerializer(serializers.Serializer):
    """创建订单序列化器"""
    cart_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        write_only=True
    )
    contact_name = serializers.CharField(max_length=50)
    contact_phone = serializers.CharField(max_length=20)
    contact_email = serializers.EmailField(required=False, allow_blank=True)
    remark = serializers.CharField(required=False, allow_blank=True)


class PaymentSerializer(serializers.ModelSerializer):
    """支付记录序列化器"""
    payment_method_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ['id', 'order_id', 'payment_no', 'payment_method', 'payment_method_display',
                 'amount', 'status', 'status_display', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'payment_no', 'created_at']
    
    def get_payment_method_display(self, obj):
        return dict(Payment.PAYMENT_METHOD_CHOICES).get(obj.payment_method, '')
    
    def get_status_display(self, obj):
        return dict(Payment.STATUS_CHOICES).get(obj.status, '')


class RefundSerializer(serializers.ModelSerializer):
    """退款记录序列化器"""
    reason_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Refund
        fields = ['id', 'order_id', 'refund_no', 'amount', 'reason', 'reason_display',
                 'reason_detail', 'status', 'status_display', 'merchant_remark',
                 'refund_time', 'created_at']
        read_only_fields = ['id', 'refund_no', 'created_at']
    
    def get_reason_display(self, obj):
        return dict(Refund.REFUND_REASON_CHOICES).get(obj.reason, '')
    
    def get_status_display(self, obj):
        return dict(Refund.STATUS_CHOICES).get(obj.status, '')


class RefundCreateSerializer(serializers.Serializer):
    """创建退款申请序列化器"""
    order_id = serializers.IntegerField(required=True)
    reason = serializers.ChoiceField(choices=Refund.REFUND_REASON_CHOICES)
    reason_detail = serializers.CharField(required=False, allow_blank=True) 