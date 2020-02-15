from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name="accueil"),
    path('resultats/', views.resultats, name='resultats'),
    path('equipes/', views.equipes, name='equipes'),
    path('contact/', views.contact, name='contact'),
    path('participant/', include('participant.urls')),
    path('organisateur/', include('organisateur.urls')),
]
