from django.urls import path
from apps.api_merchant.views import user_views

urlpatterns = [
    path('info/', user_views.get_user_info, name='merchant-user-info'),
]