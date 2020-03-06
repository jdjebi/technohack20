from django import forms
from technohack.models import Billet, list_sujets

class BilletForm(forms.ModelForm):

	numero = forms.CharField(min_length=8,max_length=8,required=True)
	sujet = forms.ChoiceField(choices=list_sujets,required=True)

	class Meta:
		model = Billet
		fields = ('nom', 'email', 'numero', 'sujet','contenu')

