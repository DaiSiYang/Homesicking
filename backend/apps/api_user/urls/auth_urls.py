
from django.urls import path
from apps.api_user.views.auth_views import user_login, user_register, user_logout, change_password

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),
    path('change-password/', change_password, name='change_password'),
]
