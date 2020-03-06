from django.contrib import admin
from .models import Equipe, Participant

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
	list_display = ('id','nom','chef','niveau','salle','date_creation','selectionner')
	ordering = ('niveau','nom','date_creation')
	list_filter = ('selectionner', 'niveau', 'salle', 'date_creation')

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
	list_display = ('id','nom','prenom','email','numero','nom_equipe','niveau','date_creation_equipe')
	list_filter = ('is_chief','equipe__niveau','equipe__selectionner','equipe__date_creation')


	def nom(self, obj):
		return obj.user.first_name

	def prenom(self, obj):
		return obj.user.last_name

	def email(self, obj):
		return obj.user.email

	def get_user(self,obj):
		return obj.user

	def nom_equipe(self,obj):
		return obj.equipe.nom

	def date_creation_equipe(self,obj):
		return obj.equipe.date_creation

	def niveau(self,obj):
		return obj.equipe.niveau

	ordering = ('equipe__niveau','equipe__nom')