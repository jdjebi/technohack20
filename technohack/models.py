from django.db import models

list_sujets = [
	("0","Retour d'information"),("1","Rapport de bug"), ("2","Demande de fonctionnalité")
]

class Billet(models.Model):
	nom = models.CharField(max_length=150,null=False,blank=False)
	email = models.EmailField(null=False,blank=False)
	numero = models.CharField(max_length=8,null=False,blank=False)
	sujet = models.CharField(max_length=150,choices=list_sujets,null=False,blank=False)
	contenu = models.TextField(null=True,blank=False)
	date_creation = models.DateTimeField('date de création', auto_now_add=True)
	traiter = models.BooleanField(default=False)