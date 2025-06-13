from django.urls import path, include

urlpatterns = [
    path('cart/', include('apps.orders.urls.cart_urls')),
    path('orders/', include('apps.orders.urls.order_urls')),
    path('payment/', include('apps.orders.urls.payment_urls')),
] 