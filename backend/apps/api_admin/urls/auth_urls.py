from django.urls import path
from apps.api_admin.views import auth_views

urlpatterns = [
    path('login/', auth_views.admin_login, name='admin-login'),
]