import uuid
from datetime import datetime
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Order, Payment, Refund
from ..serializers import PaymentSerializer, RefundSerializer, RefundCreateSerializer


class PaymentCreateView(APIView):
    """
    创建支付记录视图
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        order_id = request.data.get('order_id')
        payment_method = request.data.get('payment_method')
        
        if not order_id or not payment_method:
            return ApiResponse(
                code=400,
                message="订单ID和支付方式为必填项",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if payment_method not in dict(Payment.PAYMENT_METHOD_CHOICES):
            return ApiResponse(
                code=400,
                message="无效的支付方式",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # 检查订单状态
        if order.status != 'pending_payment':
            return ApiResponse(
                code=400,
                message="该订单无法支付",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建支付记录
        payment_no = f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
        payment = Payment.objects.create(
            order=order,
            payment_no=payment_no,
            payment_method=payment_method,
            amount=order.payment_amount,
            status='pending'
        )
        
        # 模拟支付过程（实际项目中需要对接第三方支付API）
        # 这里直接设置为支付成功
        payment.status = 'success'
        payment.transaction_id = f"TR{uuid.uuid4().hex[:10]}"
        payment.save()
        
        # 更新订单状态
        order.status = 'paid'
        order.paid_at = timezone.now()
        order.save()
        
        return ApiResponse(
            message="支付成功",
            data={
                'payment_id': payment.id,
                'payment_no': payment.payment_no,
                'order_no': order.order_no,
                'amount': payment.amount,
                'status': payment.status
            }
        )


class PaymentListView(ListAPIView):
    """
    支付记录列表视图
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # 获取用户相关的所有订单ID
        order_ids = Order.objects.filter(user=self.request.user).values_list('id', flat=True)
        return Payment.objects.filter(order_id__in=order_ids).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data)


class RefundCreateView(APIView):
    """
    申请退款视图
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = RefundCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.validated_data.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # 检查订单状态
        if order.status not in ['paid', 'confirmed']:
            return ApiResponse(
                code=400,
                message="该订单无法申请退款",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查是否已存在退款申请
        if Refund.objects.filter(order=order, status__in=['pending', 'approved', 'processing']).exists():
            return ApiResponse(
                code=400,
                message="该订单已存在退款申请",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建退款申请
        refund_no = f"REF{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
        refund = Refund.objects.create(
            order=order,
            refund_no=refund_no,
            amount=order.payment_amount,
            reason=serializer.validated_data.get('reason'),
            reason_detail=serializer.validated_data.get('reason_detail', ''),
            status='pending'
        )
        
        # 更新订单状态
        order.status = 'refunding'
        order.save()
        
        return ApiResponse(
            message="退款申请已提交",
            data={
                'refund_id': refund.id,
                'refund_no': refund.refund_no,
                'order_no': order.order_no,
                'amount': refund.amount,
                'status': refund.status
            }
        )


class RefundListView(ListAPIView):
    """
    退款记录列表视图
    """
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # 获取用户相关的所有订单ID
        order_ids = Order.objects.filter(user=self.request.user).values_list('id', flat=True)
        return Refund.objects.filter(order_id__in=order_ids).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data) 