from django.urls import path
from ..views.food_views import FoodListView, FoodDetailView, FeaturedFoodView

urlpatterns = [
    path('', FoodListView.as_view(), name='food-list'),
    path('<int:pk>/', FoodDetailView.as_view(), name='food-detail'),
    path('featured/', FeaturedFoodView.as_view(), name='featured-foods'),
]