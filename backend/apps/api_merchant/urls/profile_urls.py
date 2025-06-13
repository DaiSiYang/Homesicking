from django.urls import path
from apps.api_merchant.views import profile_views

urlpatterns = [
    path('', profile_views.merchant_profile, name='merchant-profile'),
    path('notifications/', profile_views.notification_settings, name='merchant-notifications'),
]