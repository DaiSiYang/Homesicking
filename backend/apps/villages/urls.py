from django.urls import path, include

urlpatterns = [
    path('villages/', include('apps.villages.urls.village_urls')),
    path('attractions/', include('apps.villages.urls.attraction_urls')),
] 