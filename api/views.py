from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from participant.models import Participant
from api.models import Plat, PlatConstante, PlatOrganisation

def check_user_eat1(request,participant_id):

	response = {
		'error': False,
		#'details': None,
		'participant': None
	}

	participant = Participant.objects.filter(id=participant_id)

	if not participant:
		response['error_message'] = 'Identifiant du participant inconnue.'
	else:

		participant = participant.first()

		response['participant'] = {
			"info":{
				'id': participant.id,
				'nom': participant.user.first_name,
				'prenom': participant.user.last_name,
				'username': participant.user.username,
				'numero':participant.numero,
				'email': participant.user.email,
				'equipe': participant.equipe.nom,
				'is_chief': participant.is_chief
			},
			"bilan":{
				"plat_total": Plat.get_total(),
				"plat_conso": Plat.get_conso(),
				"plat_restant": Plat.get_restant(),
				"plat_imprevu": Plat.get_imprevu()
			}
		}
		

	return JsonResponse(response,safe=False)

def check_user_eat2(request,jour,periode,participant_id):

	response = {
		'error': False,
		'error_message': None,
		'can_eat': False,
		'participant': None
	}

	participant = Participant.objects.filter(id=participant_id)

	if not participant:
		response["error"] = True
		response['error_message'] = 'Identifiant du participant inconnue.'
	else:
		participant = participant.filter(equipe__selectionner=True)

		if  not participant:
			participant_not_selected = Participant.objects.filter(id=participant_id).first()
			response['error'] = True
			response['error_message'] = "L'equipe du participant {} n'a pas ete selectionner({}).".format(participant_not_selected,participant_not_selected.equipe)
		else:
			participant = participant.first()
			# Vérifie si le participant peut manger 
			if not (jour,periode) in Plat.periode_authorize:
				response["error"] = True
				response['error_message'] = "la periode ({}/{}) n'est pas autorisée. Periodes autorisées: {}".format(jour,periode,Plat.periode_authorize)
			else:
				plats = Plat.objects.filter(participant=participant,type="repas")
				nbr_plats = plats.count()
				# Si on a pas encore atteint 
				mx_plat = PlatConstante.get_plat_mx()

				if not nbr_plats < mx_plat:
					response['can_eat_message'] = "Le participant {} a consomme tous ses les plats. Restants: {}".format(participant,mx_plat - nbr_plats)
				else:
					plat_de_periode = plats.filter(periode=periode).count()
					if not plat_de_periode < PlatConstante.periodes[periode]:
						response['can_eat_message'] = "Le participant {} n'a plus de plats pour la periode '{}'. Restants: {}".format(participant,periode,PlatConstante.periodes[periode] - plat_de_periode)
					else:
						# On vérifie que le participant n'a pas encore mangé pour cette période de la journnée
						plat_du_momment = plats.filter(periode=periode,jour=jour).count()
						if plat_du_momment >= 1:
							response['can_eat_message'] = "Le participant {} a deja mange pour le {} {}, {} fois".format(participant,jour,periode,plat_du_momment)
						else:
							response['can_eat'] = True
							response['can_eat_message'] = "Le participant {} est autorise a manger pour le {} {}. Restants: {}".format(participant,jour,periode,mx_plat - nbr_plats)

				response['participant'] = {
					"info":{
						'id': participant.id,
						'nom': participant.user.first_name,
						'prenom': participant.user.last_name,
						'username': participant.user.username,
						'numero':participant.numero,
						'email': participant.user.email,
						'equipe': participant.equipe.nom,
						'is_chief': participant.is_chief
					},
					"stats":{
						"plat_total": Plat.get_participant_total(),
						"plat_conso": Plat.get_participant_conso(participant),
						"plat_restant": Plat.get_participant_restant(participant),
						"plat_imprevu": Plat.get_participant_imprevu(participant)
					}
				}

				response['global_stats'] = {
					"plat_total": Plat.get_total(),
					"plat_conso": Plat.get_conso(),
					"plat_restant": Plat.get_restant(),
					"plat_imprevu": Plat.get_imprevu()
				}

	return JsonResponse(response,safe=False)

def set_user_eat1(request,jour,periode,participant_id):

	response = {
		'success': False,
		'message': None,
	}

	participant = Participant.objects.filter(id=participant_id)

	if not participant:
		response['message'] = 'Identifiant du participant inconnue.'
	else:
		participant = participant.filter(equipe__selectionner=True)
		
		if  not participant:
			participant_not_selected = Participant.objects.filter(id=participant_id).first()
			response['message'] = "L'equipe du participant {} n'a pas ete selectionner({}).".format(participant_not_selected,participant_not_selected.equipe)
		else:
			participant = participant.first()
			# Vérifie si le participant peut manger 
			if not (jour,periode) in Plat.periode_authorize:
				response['message'] = "la periode ({}/{}) n'est pas autorisee. Periodes autorisees: {}".format(jour,periode,Plat.periode_authorize)
			else:
				plats = Plat.objects.filter(participant=participant,type="repas")
				nbr_plats = plats.count()
				mx_plat = PlatConstante.get_plat_mx()
				if not nbr_plats < mx_plat:
					response['message'] = "Le participant {} a consomme tous ses les plats".format(participant)
				else:
					plat_de_periode = plats.filter(periode=periode).count()
					if not plat_de_periode < PlatConstante.periodes[periode]:
						response['message'] = "Le participant {} n'a plus de plats pour la periode '{}'.".format(participant,periode)
					else:
						plat_du_momment = plats.filter(periode=periode,jour=jour).count()
						if plat_du_momment >= 1:
							response['message'] = "Le participant {} a deja mange pour le {} {}.".format(participant,jour,periode)
						else:
							response['success'] = True
							response['message'] = "Restauration enregistree."
							Plat.objects.create(participant=participant,jour=jour,periode=periode)


	return JsonResponse(response,safe=False)

def eat_stats(request,jour="",periode=""):

	#1 Afficher la consommation globale (se baser sur les personnes ayant mangé)
	#2 Afficher la comsommation globale pour le couple jour/periode(comme le premier)

		#3 Afficher la liste personne mangé ou pas dans les deux cas

	if not (jour,periode) in Plat.periode_authorize:
		return redirect('api:global_stats')

	data = Plat.get_data_from_periode(jour,periode)

	nbr_plats_total = data['total']
	nbr_plats_consommes = data['conso']
	nbr_plats_restants = data['restants']

	dates = Plat.get_dates_data()
	momment_label = "{} {}".format(jour,periode)
	periode_url = "{}/{}".format(jour,periode)

	return render(request,"organisateur/statistics.html",locals())

def get_global_eat_stats(request):

	response = {
		'error':False,
		'message':None,
		'data':None
	}

	nbr_plats_total = Plat.get_total()
	nbr_plats_consommes = Plat.get_conso()
	nbr_plats_restants = Plat.get_restant()

	response['data'] = {
		'total':nbr_plats_total,
		'conso':nbr_plats_consommes,
		'restants':nbr_plats_restants
	}

	return JsonResponse(response)

def get_eat_stats(request,jour="",periode=""):

	response = {
		'error':False,
		'message':None,
		'data':None
	}
	if not (jour,periode) in Plat.periode_authorize:
		response['error'] = True
		response['message'] = "La période $(jour)/$(periode) n'est pas prise en charge"

	data = Plat.get_data_from_periode(jour,periode)

	response['data'] = {
		'total':data['total'],
		'conso':data['conso'],
		'restants':data['restants']
	}

	return JsonResponse(response)

def eat_global_stats(request):

	#1 Afficher la consommation globale (se baser sur les personnes ayant mangé)
	#2 Afficher la comsommation globale pour le couple jour/periode(comme le premier)

		#3 Afficher la liste personne mangé ou pas dans les deux cas

	# Nombre de plat total;
	# Nombre de plat consommé;
	# Nombre de plat restant;

	nbr_plats_total = Plat.get_total()
	nbr_plats_consommes = Plat.get_conso()
	nbr_plats_restants = Plat.get_restant()

	dates = Plat.get_dates_data()
	momment_label = "Général"
	periode_url = ""

	return render(request,"organisateur/statistics.html",locals())

def stats_liste(request,jour="",periode=""):

	if not (jour,periode) in Plat.periode_authorize:
		response['error'] = True
		response['message'] = "La période $(jour)/$(periode) n'est pas prise en charge"

	dates = Plat.get_dates_data()
	momment_label = "{} {}".format(jour,periode)

	paricipant_eat = []
	participant_not_eat = []

	for p in Participant.objects.filter(equipe__selectionner=True).order_by('user__last_name','user__first_name'):
		if p.plats.filter(jour=jour,periode=periode):
			paricipant_eat.append(p)
		else:
			participant_not_eat.append(p)

	return render(request,'organisateur/listes_eat.html',locals())

def orga_eat_history(request):

	dates = Plat.get_dates_data()
	momment_label = "Général"

	organisateurs = PlatOrganisation.objects.all()

	# print(organisateurs)

	if request.POST:
		data = request.POST

		print(data)

		if data.get('add') is not None:

			print('ici')

			k1 = "vendredi_soir"
			k2 = "samedi_matin"
			k3 = "samedi_midi"
			k4 = "samedi_soir"
			k5 = "dimanche_matin"
			k6 = "dimanche_midi"
			nom = data.get('orga_name')

			orga = PlatOrganisation.objects.create(nom=nom)

			if data.get(k1) and data.get(k1) == 'on':
				orga.vendredi_soir = True
			else:
				orga.vendredi_soir = False

			if data.get(k2) and data.get(k2) == 'on':
				orga.samedi_matin = True
			else:
				orga.samedi_matin = False

			if data.get(k3) and data.get(k3) == 'on':
				orga.samedi_midi = True
			else:
				orga.samedi_midi = False

			if data.get(k4) and data.get(k4) == 'on':
				orga.samedi_soir = True
			else:
				orga.samedi_soir = False

			if data.get(k5) and data.get(k5) == 'on':
				orga.dimanche_matin = True
			else:
				orga.dimanche_miidi = False

			orga.save()
			redirect('api:orga_eat_history')

		elif data.get('register') is not None:

			for i in range(0, organisateurs.count()):
				k1 = "vendredi_soir_{}".format(i)
				k2 = "samedi_matin_{}".format(i)
				k3 = "samedi_midi_{}".format(i)
				k4 = "samedi_soir_{}".format(i)
				k5 = "dimanche_matin_{}".format(i)
				k6 = "dimanche_midi_{}".format(i)
				k7 = "orga_{}".format(i)

				orga = PlatOrganisation.objects.get(pk=data[k7])

				if data.get(k1) and data.get(k1) == 'on':
					orga.vendredi_soir = True
				else:
					orga.vendredi_soir = False

				if data.get(k2) and data.get(k2) == 'on':
					orga.samedi_matin = True
				else:
					orga.samedi_matin = False

				if data.get(k3) and data.get(k3) == 'on':
					orga.samedi_midi = True
				else:
					orga.samedi_midi = False

				if data.get(k4) and data.get(k4) == 'on':
					orga.samedi_soir = True
				else:
					orga.samedi_soir = False

				if data.get(k5) and data.get(k5) == 'on':
					orga.dimanche_matin = True
				else:
					orga.dimanche_miidi = False

				orga.save()
				redirect('api:orga_eat_history')

	return render(request,"organisateur/history.eat.html",locals())