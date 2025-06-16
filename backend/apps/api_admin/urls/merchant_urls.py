from django.urls import path
from apps.api_admin.views import merchant_views

urlpatterns = [
    path('', merchant_views.merchant_list, name='admin-merchant-list'),
    path('<int:merchant_id>/', merchant_views.merchant_detail, name='admin-merchant-detail'),
    path('<int:merchant_id>/review/', merchant_views.review_merchant, name='admin-merchant-review'),
    path('<int:merchant_id>/status/', merchant_views.update_merchant_status, name='admin-merchant-status'),
    path('<int:merchant_id>/products/', merchant_views.merchant_products, name='admin-merchant-products'),
]