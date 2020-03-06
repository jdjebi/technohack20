from django.contrib import admin
from django.urls import path
from . import views
app_name = 'organisateur'
urlpatterns = [
    path('accueil/', views.accueil, name='accueil'),
    path("connexion/", views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),


    path('selectiones/listes/repartition',views.liste_re,name='liste_re'),
    path('selectiones/listes/<str:niveau>/',views.liste_se,name='liste_se'),
    path('preselection/listes/<str:niveau>/',views.liste_pre_niveau1,name='liste_pre'),

  	#path('problemes/inscription/', views.inscription_problemes, name='inscription_problemes'),

    path('equipes/<id>/', views.equipe_profil, name='equipe_profil'),
]
