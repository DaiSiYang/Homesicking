from django.urls import path
from ..views.attraction_views import AttractionListView, AttractionDetailView

urlpatterns = [
    path('', AttractionListView.as_view(), name='attraction-list'),
    path('<int:pk>/', AttractionDetailView.as_view(), name='attraction-detail'),
] 