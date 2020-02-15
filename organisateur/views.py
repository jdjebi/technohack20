from django.shortcuts import render, redirect
from .models import Organisateur
from participant.models import Participant, Equipe
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def is_valid_query_parameter(param):
    return param != '' and param is not None


@login_required(login_url="organisateur:connexion")
def accueil(request):
    if request.method == 'GET':
        participants = Participant.objects.all()
        equipes = Equipe.objects.all().order_by('date_creation')
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

        context = {'equipes': equipes}

        return render(request, 'Organisateur/accueil.html', context)

    if request.method == 'POST':
        equipes = Equipe.objects.all().order_by('date_creation')
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
        context = {'equipes': equipes}
        return render(request, 'Organisateur/accueil.html', context)

    context = {'equipes': equipes}
    return render(request, 'Organisateur/accueil.html', context)


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
                return redirect('accueil')
        else:
            messages.add_message(request, messages.ERROR,
                                 "login ou mot de passe incorrect")
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'connexion.html', context)

    return render(request, 'organisateur/connexion.html')


def deconnexion(request):
    auth.logout(request)
    return redirect('accueil')
