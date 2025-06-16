from django.urls import path
from apps.api_admin.views import product_views

urlpatterns = [
    path('', product_views.product_list, name='admin-product-list'),
    path('<int:product_id>/', product_views.product_detail, name='admin-product-detail'),
    path('<int:product_id>/status/', product_views.update_product_status, name='admin-product-status'),
    path('<int:product_id>/reviews/', product_views.product_reviews, name='admin-product-reviews'),
    path('categories/', product_views.product_categories, name='admin-product-categories'),
]