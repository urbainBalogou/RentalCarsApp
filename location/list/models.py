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
    nombre_siege = models.PositiveIntegerField(default=5)
    type_carburant = models.CharField(max_length=30)
    prix_location_ville = models.IntegerField(default=0)
    prix_location_hors_ville = models.IntegerField(default=0)
    img_vehicule = models.ImageField(upload_to="voitures", blank=True, null=True)
    disponibilite = models.BooleanField(default=True)
    climatisation = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.model},{self.marque}"

    def get_absolute_url(self):
        return reverse('car', kwargs={"slug": self.slug})


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    avec_chauffeur = models.BooleanField(default=True)
    detail_reservation = models.TextField(blank=True)
    lieu = models.TextField(blank=False)
    region = models.CharField(max_length=20)
    deb_location = models.DateField()
    fin_location = models.DateField()

    def __str__(self):
        return f"{self.client} - {self.deb_location.strftime('%d/%m/%Y')} - {self.fin_location.strftime('%d/%m/%Y')}"


class Commentaire(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.content} par {self.client}"


class Facture(models.Model):
    reservation = models.ForeignKey(Reservation, default=None, on_delete=models.CASCADE)
    montant_facture = models.IntegerField()
    date_facture = models.DateField(auto_now_add=True)
    est_paye = models.BooleanField(default=False)

    def calcul_montant_facture(self):
        if self.reservation.fin_location and self.reservation.deb_location:
            nombre_de_jours = (self.reservation.fin_location - self.reservation.deb_location).days

            if self.reservation.region == "maritime":
                return self.reservation.voiture.prix_location_ville * nombre_de_jours
            else:
                return self.reservation.voiture.prix_location_hors_ville * nombre_de_jours
        raise ValidationError("Les dates de réservation ne sont pas valides.")

    def clean(self):
        self.montant_facture = self.calcul_montant_facture()

    def __str__(self):
        return f"N°{self.id}-Montant:{self.montant_facture}"



