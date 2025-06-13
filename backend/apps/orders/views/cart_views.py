from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging  # 添加这行导入

from apps.utils.response import ApiResponse
from ..models import CartItem
from ..serializers import CartItemSerializer
from apps.products.models import Product, Food
from apps.homestays.models import RoomType

# 添加logger配置
logger = logging.getLogger(__name__)


class CartItemListCreateView(ListCreateAPIView):
    """
    购物车列表和创建视图
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        try:
            # 检查用户认证
            if not request.user.is_authenticated:
                logger.warning(f"未认证用户尝试访问购物车: {request.META.get('REMOTE_ADDR')}")
                return Response({
                    'code': 401,
                    'message': '用户未认证，请先登录',
                    'detail': '需要有效的JWT令牌'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            logger.info(f"用户 {request.user.username} 请求购物车列表")
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            
            # 计算总价
            total_price = sum(item['total_price'] for item in serializer.data)
            total_quantity = sum(item['quantity'] for item in serializer.data if item['item_type'] != 'room')
            
            return ApiResponse(data={
                'items': serializer.data,
                'total_price': total_price,
                'total_quantity': total_quantity,
                'count': len(serializer.data)
            })
            
        except Exception as e:
            logger.error(f"获取购物车列表失败: {str(e)}, 用户: {request.user}")
            return Response({
                'code': 500,
                'message': '获取购物车失败',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 验证商品是否存在
        item_type = serializer.validated_data.get('item_type')
        product_id = serializer.validated_data.get('product_id')
        food_id = serializer.validated_data.get('food_id')
        room_type_id = serializer.validated_data.get('room_type_id')
        check_in_date = serializer.validated_data.get('check_in_date')
        check_out_date = serializer.validated_data.get('check_out_date')
        
        if item_type == 'product' and product_id:
            get_object_or_404(Product, id=product_id, status='approved')
        elif item_type == 'food' and food_id:
            get_object_or_404(Food, id=food_id, status='approved')
        elif item_type == 'room' and room_type_id:
            get_object_or_404(RoomType, id=room_type_id, status='active')
            if not check_in_date or not check_out_date:
                return ApiResponse(
                    code=400,
                    message="添加房间到购物车需要提供入住和退房日期",
                    status=status.HTTP_400_BAD_REQUEST
                )
            if check_in_date >= check_out_date:
                return ApiResponse(
                    code=400,
                    message="退房日期必须晚于入住日期",
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return ApiResponse(
                code=400,
                message="无效的商品类型或商品ID",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查购物车中是否已存在相同商品
        existing_item = None
        if item_type == 'product':
            existing_item = CartItem.objects.filter(
                user=request.user,
                item_type='product',
                product_id=product_id
            ).first()
        elif item_type == 'food':
            existing_item = CartItem.objects.filter(
                user=request.user,
                item_type='food',
                food_id=food_id
            ).first()
        elif item_type == 'room':
            existing_item = CartItem.objects.filter(
                user=request.user,
                item_type='room',
                room_type_id=room_type_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            ).first()
        
        if existing_item and item_type in ['product', 'food']:
            # 更新数量
            existing_item.quantity += serializer.validated_data.get('quantity', 1)
            existing_item.save()
            return ApiResponse(
                message="购物车数量已更新",
                data=CartItemSerializer(existing_item).data
            )
        
        # 创建新的购物车项
        serializer.save(user=self.request.user)
        
        return ApiResponse(
            message="商品已添加到购物车",
            data=serializer.data
        )


class CartItemUpdateView(APIView):
    """
    购物车项更新视图
    """
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
        
        # 仅允许更新数量
        quantity = request.data.get('quantity')
        if quantity is not None:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    # 如果数量为0或负数，删除该项
                    cart_item.delete()
                    return ApiResponse(message="购物车项已删除")
                
                cart_item.quantity = quantity
                cart_item.save()
                return ApiResponse(
                    message="购物车数量已更新",
                    data=CartItemSerializer(cart_item).data
                )
            except ValueError:
                return ApiResponse(
                    code=400,
                    message="数量必须是整数",
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # 对于房间类型，允许更新入住和退房日期
        check_in_date = request.data.get('check_in_date')
        check_out_date = request.data.get('check_out_date')
        
        if cart_item.item_type == 'room' and (check_in_date or check_out_date):
            if check_in_date:
                cart_item.check_in_date = check_in_date
            if check_out_date:
                cart_item.check_out_date = check_out_date
            
            if cart_item.check_in_date >= cart_item.check_out_date:
                return ApiResponse(
                    code=400,
                    message="退房日期必须晚于入住日期",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.save()
            return ApiResponse(
                message="购物车入住日期已更新",
                data=CartItemSerializer(cart_item).data
            )
        
        return ApiResponse(
            code=400,
            message="无效的更新参数",
            status=status.HTTP_400_BAD_REQUEST
        )


class CartItemDeleteView(DestroyAPIView):
    """
    购物车项删除视图
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse(message="购物车项已删除")


class CartClearView(APIView):
    """
    清空购物车视图
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return ApiResponse(message="购物车已清空")