from django.urls import path
from . import views

urlpatterns = [
    path('weeklylogs/', views.weeklylog_list, name='weeklylog_list'),
    path('weeklylogs/<int:id>/', views.weeklylog_detail, name='weeklylog_detail'),
    path('placements/', views.placement_list, name='placement_list'),
    path('evaluations/', views.evaluation_list, name='evaluation_list'),
]
