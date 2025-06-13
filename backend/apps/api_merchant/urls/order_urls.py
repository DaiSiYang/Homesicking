from django.urls import path
from apps.api_merchant.views import order_views

urlpatterns = [
    path('recent/', order_views.get_recent_orders, name='merchant-recent-orders'),
    path('', order_views.get_merchant_orders, name='merchant-orders'),
]