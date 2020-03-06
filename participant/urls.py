from django.contrib import admin
from django.urls import path
from . import views
app_name = 'participant'
urlpatterns = [
    path("connexion/", views.connexion, name='connexion'),
    #path("inscription/", views.inscription, name='inscription'),
    #path('activation/<uidb64>/<token>', views.activate_compte, name='activate'),
    path('<username>/', views.profile, name='profile')

]
