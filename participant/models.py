from django.db import models
from django.contrib.auth.models import User
from . import listes
from django.utils import timezone


class Equipe(models.Model):
    nom = models.CharField(max_length=150)
    password = models.CharField(max_length=2000)
    salle = models.CharField(
        max_length=20, choices=listes.salles, null=True, blank=True, default="")
    selectionner = models.BooleanField(default=True)
    chef = models.CharField(max_length=150)
    date_creation = models.DateTimeField(
        'date de création', auto_now_add=True)

    niveau = models.CharField(max_length=8, choices=listes.niveau)

    def __str__(self):
        return self.nom


class Participant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='participant')
    numero = models.CharField(max_length=8)
    equipe = models.ForeignKey(
        Equipe, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        self.nom = "{} {}".format(self.user.last_name, self.user.first_name)
        return self.nom
