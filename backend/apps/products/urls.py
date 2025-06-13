from django.urls import path, include

urlpatterns = [
    path('categories/', include('apps.products.urls.category_urls')),
    path('products/', include('apps.products.urls.product_urls')),
    path('foods/', include('apps.products.urls.food_urls')),
] 