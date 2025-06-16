from django.urls import path
from apps.api_admin.views import homestay_views

urlpatterns = [
    path('', homestay_views.homestay_list, name='admin-homestay-list'),
    path('<int:homestay_id>/', homestay_views.homestay_detail, name='admin-homestay-detail'),
    path('<int:homestay_id>/status/', homestay_views.update_homestay_status, name='admin-homestay-status'),
    path('<int:homestay_id>/bookings/', homestay_views.homestay_bookings, name='admin-homestay-bookings'),
]