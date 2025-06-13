from django.urls import path, include

urlpatterns = [
    path('homestays/', include('apps.homestays.urls.homestay_urls')),
    path('room-types/', include('apps.homestays.urls.room_urls')),
]