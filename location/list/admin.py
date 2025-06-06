from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import path
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class EntretienAdmin(admin.ModelAdmin):
    list_display = ("voiture__marque", "type_entretien")
    search_field = ("type_entretien",)
    list_filter = ("date",)


admin.site.register(Entretien, EntretienAdmin)


class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom")
    search_field = ("nom", "prenom")
    list_filter = ("disponible", )


admin.site.register(Chauffeur, ChauffeurAdmin)


class VoitureDocInline(admin.TabularInline):
    model = Document
    extra = 1


class VoitureAdmin(admin.ModelAdmin):
    list_display = ("marque", "model", "nombre_siege", "disponibilite", "climatisation")
    readonly_fields = ('slug',)
    inlines = [VoitureDocInline]


class ClientAdmin(admin.ModelAdmin):
    search_fields = ["nom"]


class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'montant_facture', 'date_facture', 'est_paye']


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
