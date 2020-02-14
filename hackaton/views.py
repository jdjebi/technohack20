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
    participants = Participant.objects.all()
    equipes = Equipe.objects.all().order_by('date_creation')

    context = {
        'participants': participants,
        'equipes': equipes
    }
    return render(request, 'resultats.html', context)


def equipes(request):
    equipes = Equipe.objects.all().order_by('date_creation')

    context = {
        'equipes': equipes
    }
    return render(request, 'equipes.html', context)


def contact(request):
    list_sujets = ["Retour d'information",
                   "Rapport de bug", "Demande de fonctionnalité"]

    if request.method == 'POST':

        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        sujet = list_sujets[int(sujet) + 1]
        message = request.POST.get('message')
        send_copie = request.POST.get('send_copie')

        sujet_original = 'Thecnovor-Hackaton Formulaire de contact | {}'.format(
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
