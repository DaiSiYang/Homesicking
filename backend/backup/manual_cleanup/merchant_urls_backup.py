from django.urls import path
from ..views.merchant_views import (
    MerchantApplyView, MerchantProfileView
)

urlpatterns = [
    path('apply/', MerchantApplyView.as_view(), name='merchant-apply'),
    path('me/', MerchantProfileView.as_view(), name='merchant-profile'),
]