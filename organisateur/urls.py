from django.contrib import admin
from django.urls import path
from . import views
app_name = 'organisateur'
urlpatterns = [
    path("connexion/", views.connexion, name='connexion'),
    path('accueil/', views.accueil, name='accueil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
