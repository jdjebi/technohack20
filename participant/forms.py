from django import forms

class RegisterForm(forms.Form):
	nom = forms.CharField(max_length=100)
	password = forms.CharField(min_length=8)
	password2 = forms.CharField()
