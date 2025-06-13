from django.urls import path
from apps.api_user.views.homestay_views import homestay_list, homestay_detail, homestay_favorite, featured_homestays

urlpatterns = [
    path('', homestay_list, name='homestay-list'),
    path('<int:pk>/', homestay_detail, name='homestay-detail'),
    path('<int:pk>/favorite/', homestay_favorite, name='homestay-favorite'),
    path('featured/', featured_homestays, name='featured-homestays'),
]