from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('@c2e/v2/admin/hack20/', admin.site.urls),
    path('', views.accueil, name="accueil"),
    path('resultats/', views.resultats, name='attente'),
    #path('test/resultats/', views.resultats, name='attente'),

    path('equipes/', views.equipes, name='equipes'),
    path('contact/', views.contact, name='contact'),
    path('participant/', include('participant.urls')),
    path('@c2e/v2/orga/app/', include('organisateur.urls')),
	path('preselections/<str:niveau>/',views.liste_pre_niveau1,name='gb_liste_pre'),

    path('api/',include('api.urls'))

    #path('test/',views.test),
]
