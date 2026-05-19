from django.urls import path
from . import views

urlpatterns = [
    # WeeklyLogs
    path('weeklylogs/', views.weeklylog_list, name='weeklylog_list'),
    path('weeklylogs/<int:id>/', views.weeklylog_detail, name='weeklylog_detail'),
    path('weeklylogs/create/', views.weeklylog_create, name='weeklylog_create'),   # NEW
    path('weeklylogs/<int:id>/update/', views.weeklylog_update_status, name='weeklylog_update_status'),  # NEW

    # Placements
    path('placements/', views.placement_list, name='placement_list'),

    # Evaluations
    path('evaluations/', views.evaluation_list, name='evaluation_list'),
    path('evaluations/create/', views.evaluation_create, name='evaluation_create'),  # NEW
]
