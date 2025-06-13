from django.urls import path
from ..views.room_views import RoomTypeListView, RoomTypeDetailView, RoomAvailabilityView

urlpatterns = [
    path('', RoomTypeListView.as_view(), name='room-type-list'),
    path('<int:pk>/', RoomTypeDetailView.as_view(), name='room-type-detail'),
    path('availability/', RoomAvailabilityView.as_view(), name='room-availability'),
] 