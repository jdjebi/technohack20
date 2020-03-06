from django.contrib import admin
from .models import Plat, PlatConstante, PlatOrganisation

@admin.register(PlatConstante)
class PlatAdmin(admin.ModelAdmin):
	list_display = ('id','mx_plat','mx_plat_matin','mx_plat_midi','mx_plat_midi')


@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
	list_display = ('id','id_participant','participant','jour','periode','equipe','date')
	list_filter = ('date','participant__equipe','jour','periode',)
	ordering = ('date',)

	def id_participant(self, obj):
		return obj.participant.id

	def equipe(self, obj):
		return obj.participant.equipe

@admin.register(PlatOrganisation)
class PlatOrganisationAdmin(admin.ModelAdmin):
	list_display = ('nom','vendredi_soir','samedi_matin','samedi_midi','samedi_soir','dimanche_matin','dimanche_midi','date')
	list_filter = ('date','vendredi_soir','samedi_matin','samedi_midi','samedi_soir','dimanche_matin','dimanche_midi')
	ordering = ('nom',)


