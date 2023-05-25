from django.db import models
from django.urls import reverse

from location.settings import AUTH_USER_MODEL


class Client(models.Model):
    nom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=30, blank=True)
    adresse = models.CharField(max_length=30, blank=True)
    numero_tel = models.IntegerField(blank=True,null=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nom


class Voiture(models.Model):
    marque = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    model = models.CharField(max_length=30)
    type_carburant = models.CharField(max_length=30)
    prix_location = models.IntegerField(default=0)
    img_vehicule = models.ImageField(upload_to="voitures", blank=True, null=True)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return self.marque

    def get_absolute_url(self):
        return reverse('car', kwargs={"slug": self.slug})


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    deb_location = models.DateField()
    fin_location = models.DateField()

    def __str__(self):
        return f"{self.client} - {self.deb_location.strftime('%d/%m/%Y')} - {self.fin_location.strftime('%d/%m/%Y')}"


class Paiement(models.Model):
    reservation = models.ForeignKey(Reservation, default=None, on_delete=models.CASCADE)
    montant_paye = models.IntegerField(default=0)
    date_payement = models.DateField()


class Commentaire(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    note = models.IntegerField(default=0, blank=True,null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.note

