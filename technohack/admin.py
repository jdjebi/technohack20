from django.contrib import admin
from .models import Billet

@admin.register(Billet)
class BilletAdmin(admin.ModelAdmin):
	list_display = ('id','nom','email','sujet','numero','contenu','date_creation','traiter')
	list_filter = ('date_creation','traiter',)