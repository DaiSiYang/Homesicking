from django.urls import path
from ..views import ProductListView, ProductDetailView, CategoryListView

urlpatterns = [
    # 产品相关的 URL 配置
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='product-category-list'),
]