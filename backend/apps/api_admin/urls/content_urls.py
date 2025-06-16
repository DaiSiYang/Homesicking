from django.urls import path
from apps.api_admin.views import content_views

urlpatterns = [
    path('articles/', content_views.article_list, name='admin-article-list'),
    path('articles/<int:article_id>/', content_views.article_detail, name='admin-article-detail'),
    path('banners/', content_views.banner_list, name='admin-banner-list'),
    path('banners/<int:banner_id>/', content_views.banner_detail, name='admin-banner-detail'),
    path('announcements/', content_views.announcement_list, name='admin-announcement-list'),
]