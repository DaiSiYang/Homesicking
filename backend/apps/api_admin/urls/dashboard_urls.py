from django.urls import path
from apps.api_admin.views import dashboard_views

urlpatterns = [
    path('stats/', dashboard_views.dashboard_stats, name='admin-dashboard-stats'),
    path('activities/', dashboard_views.recent_activities, name='admin-recent-activities'),
    path('todos/', dashboard_views.todo_list, name='admin-todo-list'),
]