from django.urls import path
from apps.api_merchant.views import auth_views

urlpatterns = [
    path('login/', auth_views.merchant_login, name='merchant-login'),
    path('register/', auth_views.merchant_register, name='merchant-register'),
]