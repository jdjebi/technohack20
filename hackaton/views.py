from django.shortcuts import render
from participant.models import Participant, Equipe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from django.conf import settings


def accueil(request):
    return render(request, 'accueil.html')


def attente(request):
    return render(request, 'attente.html')


def resultats(request):
    if request.method == 'GET':
        participants = Participant.objects.all()
        equipes = Equipe.objects.all().order_by('date_creation')
        equipe_query = request.GET.get('equipe')
        participant_query = request.GET.get('participant')
        niveau_equipe = request.GET.get('niveau')
        etat_equipe = request.GET.get('etat')

        if is_valid_query_parameter(niveau_equipe) and niveau_equipe != 'Choisir...':
            equipes = equipes.filter(niveau=niveau_equipe)

        if is_valid_query_parameter(etat_equipe) and etat_equipe != 'Choisir...':
            etat_equipe = True if etat_equipe == "selectionnee" else False
            equipes = equipes.filter(selectionner=etat_equipe)

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

        context = {'equipes': equipes}

        return render(request, 'resultats.html', context)


def is_valid_query_parameter(param):
    return param != '' and param is not None


def equipes(request):
    if request.method == 'GET':
        participants = Participant.objects.all()
        equipes = Equipe.objects.all().order_by('date_creation')
        equipe_query = request.GET.get('equipe')
        participant_query = request.GET.get('participant')
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

        context = {'equipes': equipes}

        return render(request, 'equipes.html', context)

    context = {'equipes': equipes}
    return render(request, 'equipes.html', context)


def contact(request):
    list_sujets = ["Retour d'information",
                   "Rapport de bug", "Demande de fonctionnalité"]

    if request.method == 'POST':

        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        sujet = list_sujets[int(sujet)]
        message = request.POST.get('message')
        send_copie = request.POST.get('send_copie')

        sujet_original = 'Technovor-Hackaton Formulaire de contact | {}'.format(
            sujet)

        sujet_copie = 'Technovor-Hackaton Formulaire de contact (Copie) | {}'.format(
            sujet)

        context = {
            'utilisateur': nom,
            'email': email,
            'message': message
        }

        contact_message = get_template(
            'contact/contact_message.txt').render(context)

        envoyeur = settings.EMAIL_HOST_USER
        receveur = [settings.EMAIL_HOST_USER]

        if send_copie == 'on':
            send_mail(sujet_copie, message, envoyeur,
                      [email], fail_silently=True)

        send_mail(sujet_original, contact_message,
                  envoyeur, receveur, fail_silently=True)

        messages.add_message(request, messages.SUCCESS,
                             "Mail envoyé avec succès", fail_silently=False)

    return render(request, 'contact.html')
