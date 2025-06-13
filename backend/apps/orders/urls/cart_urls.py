from django.urls import path
from ..views.cart_views import (
    CartItemListCreateView, CartItemUpdateView, 
    CartItemDeleteView, CartClearView
)

urlpatterns = [
    path('', CartItemListCreateView.as_view(), name='cart-list-create'),
    path('<int:pk>/', CartItemUpdateView.as_view(), name='cart-update'),
    path('<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-delete'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
] 