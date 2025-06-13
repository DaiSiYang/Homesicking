from django.urls import path
from ..views.village_views import VillageListView, VillageDetailView, RecommendedVillageView

urlpatterns = [
    path('', VillageListView.as_view(), name='village-list'),
    path('<int:pk>/', VillageDetailView.as_view(), name='village-detail'),
    path('recommended/', RecommendedVillageView.as_view(), name='recommended-villages'),
] 