from django.urls import path
from ..views.category_views import CategoryListView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
] 