from django.urls import path
from ..views.product_views import ProductListView, ProductDetailView
from ..views.category_views import CategoryListView # CategoryListView 通常在 category_views.py

urlpatterns = [
    # 产品相关的 URL 配置
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='product-category-list'), # 使用从 category_views 导入的视图
]