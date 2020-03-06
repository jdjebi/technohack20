from django.contrib import admin
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('eat/check/participant/<participant_id>/', views.check_user_eat1, name='check_func'),
    path('eat/check/participant/<jour>/<periode>/<participant_id>/', views.check_user_eat2, name='check_func2'),
    path('eat/register/participant/<jour>/<periode>/<participant_id>/', views.set_user_eat1, name='register_func'),

    path('eat/stats/', views.eat_global_stats, name="global_stats"),
    path('eat/stats/<str:jour>/<str:periode>/', views.eat_stats, name="stats"),
    path('eat/stats/<str:jour>/<str:periode>/liste', views.stats_liste, name="stats_liste"),
    path('eat/stats/orga/', views.orga_eat_history, name="orga_eat_history"),

    path('eat/get/stats/<str:jour>/<str:periode>/', views.get_eat_stats, name="get_stats"),
    path('eat/get/stats/', views.get_global_eat_stats, name="get_global_stats"),


]
