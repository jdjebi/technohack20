from django import forms
from django.contrib.auth.models import User
from participant.models import Participant
from . import listes

class RegisterForm(forms.Form):

	nom_equipe               = forms.CharField(max_length=150,required=True,initial='')
	password_equipe          = forms.CharField(min_length=8,max_length=2000,required=True,initial='')
	confirm_password_equipe  = forms.CharField(required=True,initial='')

	nomchef     			 = forms.CharField(max_length=150,required=True,initial='')
	nom_user_chef            = forms.CharField(max_length=150,required=True,initial='')
	prenomchef  			 = forms.CharField(max_length=150,required=True,initial='')
	emailchef   			 = forms.EmailField(required=True,initial='')
	numerochef  			 = forms.CharField(max_length=150,required=True,initial='')

	nom_user_coep1           = forms.CharField(max_length=150,required=True,initial='')
	nomcoep1    			 = forms.CharField(max_length=150,required=True,initial='')
	prenomcoep1 			 = forms.CharField(max_length=150,initial='')
	emailcoep1  			 = forms.EmailField(required=True,initial='')
	numerocoep1 			 = forms.CharField(min_length=8,max_length=8,required=True,initial='')

	nom_user_coep2           = forms.CharField(max_length=150,required=True,initial='')
	nomcoep2    			 = forms.CharField(max_length=150,required=True,initial='')
	prenomcoep2 			 = forms.CharField(max_length=150,required=True,initial='')
	emailcoep2  			 = forms.EmailField(required=True,initial='')
	numerocoep2 			 = forms.CharField(min_length=8,max_length=8,required=True,initial='')

	niveau 					 = forms.ChoiceField(choices=listes.niveau,required=True) 

	def clean_nom_user_chef(self):
		username = self.cleaned_data.get('nom_user_chef')
		if User.objects.filter(username=username):
			raise forms.ValidationError("Nom d'utilisateur déjà utilisé.")
		return username

	def clean_nom_user_coep1(self):
		username = self.cleaned_data.get('nom_user_coep1')
		if User.objects.filter(username=username):
			raise forms.ValidationError("Nom d'utilisateur déjà utilisé.")
		return username

	def clean_nom_user_coep2(self):
		username = self.cleaned_data.get('nom_user_coep2')
		if User.objects.filter(username=username):
			raise forms.ValidationError("Nom d'utilisateur déjà utilisé.")
		return username

	def clean_emailchef(self):
		email = self.cleaned_data.get('emailchef')
		if User.objects.filter(email=email):
			raise forms.ValidationError("E-mail déjà utilisée.")
		return email

	def clean_emailcoep1(self):
		email = self.cleaned_data.get('emailcoep1')
		if User.objects.filter(email=email):
			raise forms.ValidationError("E-mail déjà utilisée.")
		return email

	def clean_emailcoep2(self):
		email = self.cleaned_data.get('emailcoep2')
		if User.objects.filter(email=email):
			raise forms.ValidationError("E-mail déjà utilisée.")
		return email

	def clean_numerochef(self):
		numero = self.cleaned_data.get('numerochef')
		if Participant.objects.filter(numero=numero):
			raise forms.ValidationError("Numéro déjà utilisé.")
		return numero

	def clean_numerocoep1(self):
		numero = self.cleaned_data.get('numerocoep1')
		if Participant.objects.filter(numero=numero):
			raise forms.ValidationError("Numéro déjà utilisé.")
		return numero

	def clean_numerocoep2(self):
		numero = self.cleaned_data.get('numerocoep2')
		if Participant.objects.filter(numero=numero):
			raise forms.ValidationError("Numéro déjà utilisé.")
		return numero

	def clean_confirm_password_equipe(self):
		pw = self.cleaned_data.get('password_equipe')

		if pw:
			cpw = self.cleaned_data['confirm_password_equipe']

			if pw != cpw:
				raise forms.ValidationError("Les mots de passes de ne correspondent pas.")

		return cpw

	def clean(self):
		cleaned_data = super().clean()

		nom_user_chef   = cleaned_data.get('nom_user_chef')
		emailchef       = cleaned_data.get('emailchef')
		numerochef      = cleaned_data.get('numerochef')

		nom_user_coep1  = cleaned_data.get('nom_user_coep1')
		emailcoep1      = cleaned_data.get('emailcoep1')
		numerocoep1     = cleaned_data.get('numerocoep1')

		nom_user_coep2  = cleaned_data.get('nom_user_coep2')
		emailcoep2      = cleaned_data.get('emailcoep2')
		numerocoep2     = cleaned_data.get('numerocoep2')

		# Vérification de l'unicité des nom utilisteurs dans le formulire
		numeros = [numerochef,numerocoep1,numerocoep2]

		unique_val = 'unique_val'
		unique_val_error_msg = 'Les noms, E-mails, et numéros des participants doivent être différents.'
		unique_val_validate = True
		# Unicité du nom
		if nom_user_chef:
			if nom_user_chef in [nom_user_coep1,nom_user_coep2]:
				unique_val_validate = False

		elif nom_user_coep1:
			if nom_user_coep1 in [nom_user_chef,nom_user_coep2]:
				unique_val_validate = False

		elif nom_user_coep2:
			if nom_user_coep2 in [nom_user_chef,nom_user_coep1]:
				unique_val_validate = False

		# Unicité de l'email
		if emailchef:
			if emailchef in [emailcoep1,emailcoep2]:
				unique_val_validate = False

		elif emailcoep1:
			if emailcoep1 in [emailcoep2,emailchef]:
				unique_val_validate = False

		elif emailcoep2:
			if emailcoep2 in [emailcoep1,emailchef]:
				unique_val_validate = False

		# Unicité du numéro
		if numerochef:
			if numerochef in [numerocoep1,numerocoep2]:
				unique_val_validate = False

		elif numerocoep1:
			if numerocoep1 in [numerocoep2,numerochef]:
				unique_val_validate = False

		elif numerocoep2:
			if numerocoep2 in [numerocoep1,numerochef]:
				unique_val_validate = False

		if unique_val_validate is False:
			raise forms.ValidationError(unique_val_error_msg)