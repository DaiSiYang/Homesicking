from django.urls import path
from apps.api_admin.views import settings_views

urlpatterns = [
    path('system/', settings_views.system_settings, name='admin-system-settings'),
    path('email/', settings_views.email_settings, name='admin-email-settings'),
    path('payment/', settings_views.payment_settings, name='admin-payment-settings'),
    path('backup/', settings_views.backup_data, name='admin-backup-data'),
]