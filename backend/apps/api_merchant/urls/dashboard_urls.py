from django.urls import path
from apps.api_merchant.views import dashboard_views

urlpatterns = [
    path('', dashboard_views.get_dashboard_data, name='merchant-dashboard'),
]