from django.db import models
from participant.models import Participant


class PlatConstante(models.Model):

	periodes = {
		'matin':2,
		'midi':2,
		'soir': 2,
	}

	mx = periodes['matin'] + periodes['midi'] + periodes['soir']

	mx_plat = models.IntegerField(verbose_name="Nombre de plats maximal",default=mx)
	mx_plat_matin = models.IntegerField(verbose_name="Nom de plats maximal du main",default=periodes['matin'])
	mx_plat_midi = models.IntegerField(verbose_name="Nom de plats maximal de midi",default=periodes['midi'])
	mx_plat_midi = models.IntegerField(verbose_name="Nom de plats maximal du soir",default=periodes['soir'])

	@classmethod
	def get_cte(cls):
		constantes = PlatConstante.objects.all()

		if constantes:
			cte = constantes.first()
		else:
			cte = PlatConstante.objects.create()
			cte.save()

		return cte

	@classmethod
	def get_plat_mx(cls):
		cte = PlatConstante.get_cte()
		return cte.mx_plat

	@classmethod
	def get_plat_matin(cls):
		cte = PlatConstante.get_cte()
		return cte.mx_plat_matin

	@classmethod
	def get_plat_midi(cls):
		cte = PlatConstante.get_cte()
		return cte.mx_plat_midi

	@classmethod
	def get_plat_soir(cls):
		cte = PlatConstante.get_cte()
		return cte.mx_plat_soir

""" Api eat - pour la gestion de restauration """
class Plat(models.Model):

	jours_list = ['vendredi','samedi','dimanche']
	periodes_list = ["matin",'midi','soir']

	periode_authorize = [
		('vendredi','soir'),
		('samedi','matin'),
		('samedi','midi'),
		('samedi','soir'),
		('dimanche','matin'),
		('dimanche','midi'),
	]

	jours = [
		("vendredi", "vendredi") ,
		("samedi","samedi") ,
		("dimanche","dimanche") 
	]

	periodes = [
		("matin","matin") ,
		("midi","midi") ,
		("soir","soir") 
	]

	types = [
		("repas","repas") ,
		("boisson","boisson") ,
		("autre","autre") 
	]

	participant = models.ForeignKey(Participant,on_delete=models.CASCADE,related_name="plats")
	jour = models.CharField(choices=jours,default="vendredi",max_length=100)
	periode = models.CharField(choices=periodes,default="soir",max_length=100)
	type = models.CharField(choices=types,default="repas",max_length=100)
	date = models.DateTimeField(verbose_name="Date de restauration",auto_now_add=True)

	@classmethod
	def get_total(cls):
		return PlatConstante.get_plat_mx() * Participant.objects.filter(equipe__selectionner=True).count()

	@classmethod
	def get_conso(cls):
		return Plat.objects.all().count()

	@classmethod
	def get_restant(cls):
		r = Plat.get_total() - Plat.get_conso() 
		if r < 0:
			return 0
		else:
			return r

	@classmethod
	def get_imprevu(cls):
		p = Plat.get_total() - Plat.get_conso() 
		if p < 0:
			p *= -1
		else:
			p = 0
		
		return p

	@classmethod
	def get_participant_total(cls):
		return PlatConstante.get_plat_mx()

	@classmethod
	def get_participant_conso(cls,participant):
		return Plat.objects.filter(participant=participant).count()

	@classmethod
	def get_participant_restant(cls,participant):
		r = Plat.get_participant_total() - Plat.get_participant_conso(participant) 
		if r < 0:
			return 0
		else:
			return r

	@classmethod
	def get_participant_imprevu(cls,participant):
		p = Plat.get_participant_total() - Plat.get_participant_conso(participant) 
		if p < 0:
			p *= -1
		else:
			p = 0
		
		return p

	@classmethod
	def get_plat_for_period(cls,jour,periode):
		return Plat.objects.filter(jour=jour,periode=periode)

	@classmethod
	def get_data_from_periode(cls,jour,periode):

		total = Participant.objects.filter(equipe__selectionner=True).count()
		conso = Plat.get_plat_for_period(jour,periode).count()
		restants = total - conso

		return {
			"total": total,
			"conso": conso,
			"restants": restants
		}

	@classmethod
	def get_dates_data(cls):
		dates = []
		for date in Plat.periode_authorize:
			j = date[0]
			p = date[1]
			dates.append({
				'label': "{} {}".format(j, p),
				'jour': j,
				'periode': p,
				'data': Plat.get_data_from_periode(j, p)
			})
		return dates

class PlatOrganisation(models.Model):

	nom = models.CharField(verbose_name="Organisateur",max_length=100,default="Inconnue")
	vendredi_soir = models.BooleanField(verbose_name="Vendredi Soir",default=False)
	samedi_matin = models.BooleanField(verbose_name="Samedi Matin", default=False)
	samedi_midi = models.BooleanField(verbose_name="Samedi Midi", default=False)
	samedi_soir = models.BooleanField(verbose_name="Samedi Soir", default=False)
	dimanche_matin = models.BooleanField(verbose_name="Dimanche Matin", default=False)
	dimanche_midi = models.BooleanField(verbose_name="Dimanche Soir", default=False)

	date = models.DateTimeField(verbose_name="Date du dernier repas",auto_now=True)