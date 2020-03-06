from django.shortcuts import render, redirect, get_object_or_404
from participant.models import Participant, Equipe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from django.conf import settings
from .forms import BilletForm
from .models import Billet
from django.http import Http404


def test(request):
    return render(request, 'auth/activate_failed.html')


def accueil(request):
    if request.user.is_authenticated:
        return redirect('participant:profile',username=request.user.username)
    return render(request, 'accueil.html')


def attente(request):
    return render(request, 'attente.html')


def resultats(request):
    equipes = Equipe.objects.all().filter(selectionner=True).order_by('-selectionner','nom')
    equipes_niveau1 = equipes.filter(niveau='Niveau 1')
    equipes_niveau2 = equipes.filter(niveau='Niveau 2')

    return render(request, 'resultats.html', locals())


def is_valid_query_parameter(param):
    return param != '' and param is not None


def equipes(request):

    if request.method == 'GET':
        participants = Participant.objects.all()
        equipes = Equipe.objects.all().order_by('niveau','date_creation')
        equipe_query = request.GET.get('equipe')
        participant_query = request.GET.get('participant')
        niveau_equipe = request.GET.get('niveau')

        if is_valid_query_parameter(niveau_equipe) and niveau_equipe != 'Choisir...':
            equipes = equipes.filter(niveau=niveau_equipe)

        if is_valid_query_parameter(equipe_query):
            equipes = equipes.filter(nom__icontains=equipe_query)

        if is_valid_query_parameter(participant_query):
            participants = participants.filter(user__last_name__icontains=participant_query)
            equipes = [participant.equipe for participant in participants]
            equipes_unique = []
            for equipe in equipes:
                if equipe not in equipes_unique:
                    equipes_unique.append(equipe)
            equipes = equipes_unique

        context = {'equipes': equipes}

        return render(request, 'equipes.html', context)

    context = {'equipes': equipes}
    return render(request, 'equipes.html', context)


def contact(request):

    form = BilletForm(request.POST or None)

    if form.is_valid():

        nom = form.cleaned_data['nom']
        email = form.cleaned_data['email']
        numero = form.cleaned_data['numero']
        sujet = form.cleaned_data['sujet']
        contenu = form.cleaned_data['contenu']

        billet = Billet.objects.create(nom=nom,email=email,numero=numero,sujet=sujet,contenu=contenu)
        billet.save()

        messages.add_message(request, messages.SUCCESS,"Message envoyé. Nous vous contacterons le plus vite possible.", fail_silently=False)

    return render(request, 'contact.html',locals())


def liste_pre_niveau1(request,niveau=""):

    niveaux_label = {
        "niveau1" : "Niveau 1",
        "niveau2" : "Niveau 2",
        "niveau3" : "Niveau 3"
    }

    niveau_salle_config_pre_selection = {
        "niveau1": 4,
        "niveau2": 5,
        "niveau3": 5,
    }

    salles = ["A","B","C","D","E","F","G","H"]

    if not niveau in niveaux_label.keys():
        raise Http404("Niveau incorrecte")

    niveau_key = niveau
    niveau = niveaux_label[niveau]

    equipes_data = Equipe.objects.filter(niveau=niveau).order_by('date_creation')

    nbr_equipe_by_salle = niveau_salle_config_pre_selection[niveau_key]

    equipes = []
    salle_id = 0
    nbr_salle_tmp = 0

    for i, equipe_data in enumerate(equipes_data):

        if nbr_salle_tmp >= nbr_equipe_by_salle:
            nbr_salle_tmp = 0
            salle_id += 1

        equipe = {}
        equipe["nom"] = equipe_data.nom
        equipe["participants"] = equipe_data.participants
        equipe["salle"] = salles[salle_id]
        equipes.append(equipe)

        nbr_salle_tmp += 1

   # print(equipes)

    return render(request,'preselection.html',locals())