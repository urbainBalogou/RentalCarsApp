from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


User = get_user_model()

from .models import Voiture, Reservation, Client, Commentaire

# Create your views here.


def index(request):
    cars = Voiture.objects.all()
    return render(request, "list/index.html", context={"cars": cars})


def car_detail(request, slug):
    car = get_object_or_404(Voiture, slug=slug)
    print("car1",car)
    if request.method == 'POST':
        # Récupérer les valeurs entrées dans le formulaire
        avec_chauffeur = request.POST.get('chauffeur')
        #print(avec_chauffeur)
        if avec_chauffeur == "avec chauffeur":
            avec_chauffeur = True
        else:
            avec_chauffeur = False
        region = request.POST.get('region')

        lieu = request.POST.get('lieu')
        date_deb = request.POST.get('date_deb')
        date_fin = request.POST.get('date_fin')
        if date_deb > date_fin or date_fin < date_deb:
            return HttpResponse("Inconformité au niveau de la date! Retournez pour corriger")


        # Créer une instance de modèle Reservation et enregistrer les données
        user = Client(nom=request.user)
        user.save()
        reserve = Reservation(region=region,avec_chauffeur=avec_chauffeur,lieu=lieu, deb_location=date_deb, fin_location=date_fin, client=user, voiture=car)
        send_mail(
            subject="Nouvelle Réservation",
            message=f"Une nouvelle réservation a été effectuée pour la voiture {car.model}. "
                    f"Début : {date_deb}, Fin : {date_fin}, Point de livraison : {lieu}.",
            from_email=f"{request.user.email}",  # Remplacez par une adresse valide
            recipient_list=["elonovacar@gmail.com","urbainbalogou19@gmail.com"],
            fail_silently=False,
        )
        reserve.save()
        return render(request,"list/succes_page.html")

    if request.method == 'GET':
        comment = request.GET.get('commentaire')
        if comment:


            user = Client(nom=request.user)

            commentaire = Commentaire(client=user, voiture=car, content=comment)
            user.save()
            commentaire.save()
            return render(request,'list/detail.html',context={'car': car})

    return render(request, 'list/detail.html', context={'car': car})











# Create your views here.
