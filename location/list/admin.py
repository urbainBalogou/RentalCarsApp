from django.contrib import admin
from.models import *
from django.utils.html import format_html
from django.urls import path


class VoitureAdmin(admin.ModelAdmin):
    list_display = ("marque", "model", "disponibilite")


class ClientAdmin(admin.ModelAdmin):
    search_fields = ["nom"]


class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'montant_facture', 'date_facture', 'est_paye']

    # Fonction pour afficher le bouton d'exportation
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_export_button'] = True  # Ajouter une variable de contexte pour afficher le bouton
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    # Action qui déclenche l'exportation
    def export_facture(self, request, facture_id):
        return redirect(f'/admin/list/facture/{facture_id}/export_word/')

    # Configuration de l'URL pour l'exportation
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:facture_id>/export_word/', self.export_facture, name='export_facture_word'),
        ]
        return custom_urls + urls

    # Personnaliser le rendu des boutons dans l'interface d'administration
    def render_change_form(self, request, context, *args, **kwargs):
        obj = context.get('original')  # Accéder à l'objet actuel
        if obj:  # Vérifie si l'objet existe
            context['additional_buttons'] = format_html(
                '<a class="button" href="{}">Exporter en Word</a>',
                f'/admin/list/facture/{obj.id}/export_word/'
            )
        return super().render_change_form(request, context, *args, **kwargs)


admin.site.register(Client, ClientAdmin)
admin.site.register(Voiture, VoitureAdmin)
admin.site.register(Reservation)
admin.site.register(Facture,FactureAdmin)

admin.site.register(Commentaire)
