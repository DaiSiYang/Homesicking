from django.urls import path
from apps.api_user.views.product_views import product_list, product_detail, product_categories, product_favorite

urlpatterns = [
    path('', product_list, name='product-list'),
    path('<int:pk>/', product_detail, name='product-detail'),
    path('<int:pk>/favorite/', product_favorite, name='product-favorite'),
    path('categories/', product_categories, name='product-categories'),
]