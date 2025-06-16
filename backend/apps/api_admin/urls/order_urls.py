from django.urls import path
from apps.api_admin.views import order_views

urlpatterns = [
    path('', order_views.order_list, name='admin-order-list'),
    path('<int:order_id>/', order_views.order_detail, name='admin-order-detail'),
    path('<int:order_id>/status/', order_views.update_order_status, name='admin-order-status'),
    path('stats/', order_views.order_stats, name='admin-order-stats'),
]