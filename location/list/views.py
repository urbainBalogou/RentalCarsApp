from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Voiture, Reservation, Client, Commentaire

# Create your views here.


def index(request):
    cars = Voiture.objects.all()
    return render(request, "list/index.html", context={"cars": cars})


def car_detail(request, slug):
    car = get_object_or_404(Voiture, slug=slug)
    if request.method == 'POST':
        # Récupérer les valeurs entrées dans le formulaire
        date_deb = request.POST.get('date_deb')
        date_fin = request.POST.get('date_fin')


        # Créer une instance de modèle Reservation et enregistrer les données
        user = Client(nom=request.user)
        user.save()
        reserve = Reservation(deb_location=date_deb, fin_location=date_fin, client=user, voiture=car)
        reserve.save()


        # Rediriger l'utilisateur vers une autre page après l'enregistrement
        return HttpResponse('Reservation effectué avec succès')
    if request.method == 'GET':
        comment = request.GET.get('commentaire')
        user = Client(nom=request.user)
        user.save()
        commentaire = Commentaire(client=user, voiture=car, content=comment)
        commentaire.save()
        return render(request,'list/detail.html',context={'car': car})
    return render(request, 'list/detail.html', context={'car': car})











# Create your views here.
