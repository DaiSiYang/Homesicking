from django.urls import path
from ..views.homestay_views import HomestayListView, HomestayDetailView, FeaturedHomestayView

urlpatterns = [
    path('', HomestayListView.as_view(), name='homestay-list'),
    path('<int:pk>/', HomestayDetailView.as_view(), name='homestay-detail'),
    path('featured/', FeaturedHomestayView.as_view(), name='featured-homestays'),
] 