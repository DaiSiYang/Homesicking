from django.urls import path
from apps.api_admin.views import user_views

urlpatterns = [
    path('', user_views.user_list, name='admin-user-list'),
    path('<int:user_id>/', user_views.user_detail, name='admin-user-detail'),
    path('<int:user_id>/status/', user_views.update_user_status, name='admin-user-status'),
    path('<int:user_id>/reset-password/', user_views.reset_user_password, name='admin-user-reset-password'),
    path('<int:user_id>/orders/', user_views.user_orders, name='admin-user-orders'),
]