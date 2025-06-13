from django.urls import path

# 这里将在后续实现商户管理功能时添加具体的视图
urlpatterns = [
    # 商户订单管理
    # path('orders/', MerchantOrderListView.as_view(), name='merchant-order-list'),
    # path('orders/<int:pk>/confirm/', MerchantOrderConfirmView.as_view(), name='merchant-order-confirm'),
    # path('orders/<int:pk>/check-in/', MerchantOrderCheckInView.as_view(), name='merchant-order-check-in'),
    # path('orders/<int:pk>/check-out/', MerchantOrderCheckOutView.as_view(), name='merchant-order-check-out'),
    # 商户退款管理
    # path('refunds/<int:pk>/process/', MerchantRefundProcessView.as_view(), name='merchant-refund-process'),
]