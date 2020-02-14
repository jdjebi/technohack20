from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipe, Participant
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from validate_email import validate_email


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from .chiffrer_password import coder_mdp


def connexion(request):
    context = {
        'data': request.POST,
        'has_error': False
    }
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        #mdp = coder_mdp(password)

        #user = auth.authenticate(username=login, password=mdp)

        #"""
        #Correction 

        user = auth.authenticate(username=login, password=password)

        #"""

        if user is not None:
            auth.login(request, user)
            return redirect('accueil')
        else:
            messages.add_message(request, messages.ERROR,
                                 "Nom d'utilisateur ou mot de passe incorrect")
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'participant/connexion.html', context)

    return render(request, 'participant/connexion.html')


from .forms import RegisterForm

def inscription(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():
        print('Valide')

        data = form.cleaned_data

        data['password_equipe'] = coder_mdp(data['password_equipe'])

       # enregistrer l'équipe
        equipe = Equipe.objects.create(nom=data['nom_equipe'], password= data['password_equipe'])
        equipe.chef = "{} {}".format(data['nomchef'], data['prenomchef'])

         # enregistrer le chef de l'équipe
        chef_equipe = User.objects.create_user(username=data['nom_user_chef'], email=data['emailchef'])
        chef_equipe.set_password(data['password_equipe'])
        chef_equipe.first_name = data['prenomchef']
        chef_equipe.last_name = data['nomchef']
        chef_equipe.is_active = False

        # enregistrer le coéquipier 1
        coep1 = User.objects.create_user(username=data['nom_user_coep1'], email=data['emailcoep1'])
        coep1.set_password(data['password_equipe'])
        coep1.first_name = data['prenomcoep1']
        coep1.last_name = data['nomcoep1']
        coep1.is_active = False

        # enregistrer le coéquipier 2
        coep2 = User.objects.create_user(username=data['nom_user_coep2'], email=data['emailcoep2'])
        coep2.set_password(data['password_equipe'])
        coep2.first_name = data['prenomcoep2']
        coep2.last_name = data['nomcoep2']
        coep2.is_active = False

        # attribution des equipes
        chef_equipe.save()
        coep1.save()
        coep2.save()
        equipe.save()

        liste_participant = [(chef_equipe, data['numerochef']), (coep1, data['numerocoep1']), (coep2, data['numerocoep2'])]

        for i, j in liste_participant:
            participant = Participant.objects.create(user=i, numero=j, equipe=equipe)
            participant.save()

    return render(request, 'participant/inscription.html',{'form':form})


def activate_compte(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        chef_equipe = User.objects.get(pk=uid)
    except Exeception as identifier:
        chef_equipe = None

    if chef_equipe is not None and generate_token.check_token(chef_equipe, token):
        chef_equipe.is_active = True
        chef_equipe.save()
        participants = chef_equipe.participant.equipe.participants.all()
        for participant in participants:
            participant.user.is_active = True
            participant.user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Votre équipe a été activée avec succès')
        return redirect('participant:connexion')

    return render(request, 'auth/activate_failed.html')


@login_required(login_url="participant:connexion")
def profile(request, username):
    if request.method != 'GET':
        user = get_object_or_404(User, username=username)
        context = {
            "user": user
        }
        return render(request, 'participant/profile.html', context)
    return render(request, 'participant/profile.html')
