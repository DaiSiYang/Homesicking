from django.urls import path
from ..views.payment_views import (
    PaymentCreateView, PaymentListView,
    RefundCreateView, RefundListView
)

urlpatterns = [
    # 支付相关
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    
    # 退款相关
    path('refund/', RefundListView.as_view(), name='refund-list'),
    path('refund/create/', RefundCreateView.as_view(), name='refund-create'),
] 