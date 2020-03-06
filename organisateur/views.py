from django.shortcuts import render, redirect, get_object_or_404
from .models import Organisateur
from participant.models import Participant, Equipe
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse


niveau_list = ["niveau1","niveau2","niveau3","all"]

niveaux_label = {
    "niveau1" : "Niveau 1",
    "niveau2" : "Niveau 2",
    "niveau3" : "Niveau 3"
}

def get_equipes(equipes_data):
    equipes = []
    j = 1
    for i, e in enumerate(equipes_data):
        equipe = {}
        equipe["nom"] = e.nom
        equipe["niveau"] = e.niveau
        equipe["participants"] = []

        for participant in e.participants.all():

            p = {
                'i': j,
                'pk': participant.id,
                'nom': str(participant)
            }

            j += 1

            equipe["participants"].append(p)

        equipes.append(equipe)

    print(equipes)

    return equipes


@login_required(login_url="organisateur:connexion")
def liste_pre_niveau1(request,niveau=""):

    if not request.user.is_staff:
            return redirect('accueil')

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


   # print(equipes)

    return render(request,'organisateur/liste_participants_niveau1.html',locals())


@login_required(login_url="organisateur:connexion")
def liste_se(request,niveau=""):
    if not request.user.is_staff:
        return redirect('accueil')

    if not niveau in niveau_list:
        raise Http404("Niveau inconnue")

    if niveau != "all":
        niveau = niveaux_label[niveau]
        equipes_data = Equipe.objects.filter(niveau=niveau,selectionner=True).order_by('niveau','nom')

    else:
        niveau = "Tous les niveaux"
        equipes_data = Equipe.objects.filter(selectionner=True).order_by('niveau','nom')

    equipes = get_equipes(equipes_data)

    print(equipes)

    return render(request,'organisateur/liste_selectionnes.html',locals())



def is_valid_query_parameter(param):
    return param != '' and param is not None


@login_required(login_url="organisateur:connexion")
def liste_re(request):
    if not request.user.is_staff:
        return redirect('accueil')

    equipes_n1 = get_equipes(Equipe.objects.filter(niveau="Niveau 1",selectionner=True).order_by('nom'))
    equipes_n2 = get_equipes(Equipe.objects.filter(niveau="Niveau 2",selectionner=True).order_by('nom'))
    equipes_n3 = get_equipes(Equipe.objects.filter(niveau="Niveau 3",selectionner=True).order_by('nom'))

    return render(request,"organisateur/liste_equipes_selectionnees.html",locals())



def is_valid_query_parameter(param):
    return param != '' and param is not None


@login_required(login_url="organisateur:connexion")
def accueil(request):

    if not request.user.is_staff:
        return redirect('accueil')

    equipes = Equipe.objects.all().order_by('niveau','date_creation')

    n1 = equipes.filter(niveau='Niveau 1').count()
    n2 = equipes.filter(niveau='Niveau 2').count()
    n3 = equipes.filter(niveau='Niveau 3').count()
    n  = n1 + n2 + n3

    if request.method == 'GET':
        participants = Participant.objects.all()
        equipe_query = request.GET.get('equipe')
        participant_query = request.GET.get('participant')
        etat_query = request.GET.get('etat')
        niveau_equipe = request.GET.get('niveau')

        if is_valid_query_parameter(niveau_equipe) and niveau_equipe != 'Choisir...':
            equipes = equipes.filter(niveau=niveau_equipe)

        if is_valid_query_parameter(equipe_query):
            equipes = equipes.filter(nom__icontains=equipe_query)

        if is_valid_query_parameter(participant_query):
            participants = participants.filter(
                user__last_name__icontains=participant_query)
            print(participants)
            equipes = [participant.equipe for participant in participants]
            equipes_unique = []
            for equipe in equipes:
                if equipe not in equipes_unique:
                    equipes_unique.append(equipe)
            equipes = equipes_unique

        if is_valid_query_parameter(etat_query) and etat_query != 'Choisir...':
            if etat_query == 'selectionnee':
                equipes = equipes.filter(selectionner=True)
            else:
                equipes = equipes.filter(selectionner=False)

        return render(request, 'organisateur/accueil.html', locals())

    if request.method == 'POST':
        equipes = [equipe for equipe in equipes]

        for equipe in equipes:
            index = equipes.index(equipe)
            selectionneur = "selectionner_{}".format(index + 1)
            if request.POST.get(selectionneur) == 'selectionnee':
                equipe.selectionner = True
            else:
                equipe.selectionner = False
            equipe.save()

        equipes = Equipe.objects.all().order_by('date_creation')

        return render(request, 'organisateur/accueil.html', locals())

    return render(request, 'organisateur/accueil.html', locals())


def connexion(request):
    context = {
        'data': request.POST,
        'has_error': False
    }
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = auth.authenticate(username=login, password=password)

        if user is not None:
            auth.login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('organisateur:accueil')
        else:
            messages.add_message(request, messages.ERROR,
                                 "login ou mot de passe incorrect")
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'connexion.html', context)

    return render(request, 'organisateur/connexion.html')

@login_required(login_url="participant:connexion")
def equipe_profil(request, id):

    if not request.user.is_staff:
        return redirect('accueil')

    equipe = get_object_or_404(Equipe, id=id)

    participants = equipe.participants.all

    return render(request, 'organisateur/equipe.html', locals())


@login_required(login_url="participant:connexion")
def inscription_problemes(request): 

    if not request.user.is_superuser:
        return redirect('accueil')

    users = User.objects.all()
    equipes = Equipe.objects.all()

    fake_users = []
    fake_equipes = []

    for user2 in users:
        try:
            user2.participant
        except:
            fake_users.append(user2)

    for equipe in equipes:
        if equipe.chef == "":
            fake_equipes.append(equipe)

    return render(request,"organisateur/inscription.probs.html",locals())


def deconnexion(request):
    auth.logout(request)
    return redirect('accueil')

