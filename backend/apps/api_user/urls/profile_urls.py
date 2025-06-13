
from django.urls import path
from apps.api_user.views import profile_views

urlpatterns = [
    path('', profile_views.get_user_profile, name='user-profile'),
    path('update/', profile_views.update_user_profile, name='user-profile-update'),
]
