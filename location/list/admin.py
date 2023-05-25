from django.contrib import admin
from.models import *


class VoitureAdmin(admin.ModelAdmin):
    list_display = ("marque", "model", "disponibilite", "prix_location")


class ClientAdmin(admin.ModelAdmin):
    search_fields = ["nom"]

class PayementAdmin(admin.ModelAdmin):
    list_display = ( 'reservation', 'montant_paye', 'date_payement')


admin.site.register(Client, ClientAdmin)
admin.site.register(Voiture, VoitureAdmin)
admin.site.register(Reservation)
admin.site.register(Paiement)

admin.site.register(Commentaire)
