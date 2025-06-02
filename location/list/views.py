from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import Voiture, Reservation, Client, Commentaire, Facture

User = get_user_model()


def index(request):
    cars = Voiture.objects.all()
    return render(request, "list/index.html", context={"cars": cars})


def car_detail(request, slug):
    car = get_object_or_404(Voiture, slug=slug)

    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        tel = request.POST.get('tel')
        client_name = request.POST.get('client')
        avec_chauffeur = request.POST.get('chauffeur') == "avec chauffeur"
        region = request.POST.get('region')
        lieu = request.POST.get('lieu')
        date_deb = request.POST.get('date_deb')
        date_fin = request.POST.get('date_fin')
        detail_reservation = request.POST.get('detail_reservation')

        try:
            # Conversion des dates
            date_deb = datetime.strptime(date_deb, "%Y-%m-%d")
            date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "Format de date invalide. Utilisez AAAA-MM-JJ.")
            return render(request, 'list/detail.html', context={'car': car})

        now = datetime.now()
        today = now.date()

        if date_deb.date() > date_fin.date():
            messages.error(request, "La date de début ne peut pas être après la date de fin.")
        elif date_deb.date() < today or date_fin.date() < today:
            messages.error(request, "Les dates doivent être dans le futur.")
        else:
            # Création du client s'il n'existe pas déjà
            # , created = Client.objects.get_or_create(nom=request.user)

            if request.user.is_authenticated:
                user, _ = Client.objects.get_or_create(nom=request.user.username)
            else:
                user, _ = Client.objects.get_or_create(nom=client_name, numero_tel=tel,email = client_name + "created@gmail.com")

            # Création de la réservation
            reserve = Reservation(
                region=region,
                avec_chauffeur=avec_chauffeur,
                lieu=lieu,
                deb_location=date_deb,
                fin_location=date_fin,
                client=user,
                voiture=car,
                detail_reservation=detail_reservation
            )
            reserve.save()

            # Envoi d'un email (désactivé pour l'instant)
            print("Envoi d'email")
            # Envoi de l'email
            send_mail(
                subject="Nouvelle Réservation",
                message=f"Une nouvelle réservation a été effectuée par {client_name} pour la voiture {car.model}. "
                        f"Début : {date_deb}, Fin : {date_fin}, Point de livraison : {lieu}.",
                from_email="elonovacar@site.com",
                recipient_list=["elonovacar@gmail.com", "urbainbalogou19@gmail.com"],
                fail_silently=False,
            )

            return redirect('succes_page')

    elif request.method == 'GET':
        comment = request.GET.get('commentaire')
        if comment:
            user, created = Client.objects.get_or_create(nom=request.user)
            commentaire = Commentaire(client=user, voiture=car, content=comment)
            commentaire.save()
            messages.success(request, "Commentaire ajouté avec succès.")

    return render(request, 'list/detail.html', context={'car': car})


def succes_page(request):
    messages.success(request, "Réservation effectuée avec succès.")
    messages.success(
        request,
        "Souhaitez-vous faire une réservation de longue durée ? "
        "Profitez des avantages en nous écrivant par mail."
    )
    return render(request, "list/succes_page.html")


def reservations(request):
    reservations = Reservation.objects.filter(client__nom=request.user)
    return render(request, 'accounts/show_reservation.html', {'reservations': reservations})
