from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Client(models.Model):
    nom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=30, blank=True)
    adresse = models.CharField(max_length=30, blank=True)
    numero_tel = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Voiture(models.Model):
    marque = models.CharField(max_length=128)
    model = models.CharField(max_length=30)
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    immatriculation = models.CharField(max_length=20, default="TG-0000-AA")
    nombre_siege = models.PositiveIntegerField(default=5)
    type_carburant = models.CharField(max_length=30)
    tarif_A_B = models.PositiveIntegerField(default=5000)
    prix_location_ville_chauffeur = models.IntegerField(default=0)
    prix_location_ville_sans_chauffeur = models.IntegerField(default=0)
    prix_location_hors_ville_chauffeur = models.IntegerField(default=0)
    prix_location_hors_ville_sans_chauffeur = models.IntegerField(default=0)
    img_vehicule = models.ImageField(upload_to="voitures", blank=True, null=True)
    disponibilite = models.BooleanField(default=True)
    boite = models.CharField(max_length=15, choices=[("Automatique", "Automatique"), ("Manuelle", "Manuelle")], default="Manuelle")
    climatisation = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marque} {self.model}"

    def get_absolute_url(self):
        return reverse('car', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.marque}-{self.model}")
        super(Voiture, self).save(*args, **kwargs)


class Chauffeur(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30, blank=True)
    telephone = models.CharField(max_length=15)
    disponible = models.BooleanField(default=True)
    voiture = models.OneToOneField(Voiture, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Document(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    doc = models.FileField(blank=True, null=True, upload_to="documents/")

    def __str__(self):
        return f"Document pour {self.voiture}"


class Entretien(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date = models.DateField()
    type_entretien = models.CharField(max_length=50)
    commentaire = models.TextField(blank=True)
    cout = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.type_entretien} ({self.date}) - {self.voiture}"


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    avec_chauffeur = models.BooleanField(default=True)
    detail_reservation = models.TextField(blank=True)
    lieu = models.TextField(blank=False)
    region = models.CharField(max_length=20)
    deb_location = models.DateField()
    fin_location = models.DateField()
    montant_facture = models.PositiveIntegerField(default=0)
    est_finalise = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client} - {self.deb_location.strftime('%d/%m/%Y')} - {self.fin_location.strftime('%d/%m/%Y')}"

    def clean(self):
        # Validation de conflit de réservation
        conflits = Reservation.objects.filter(
            voiture=self.voiture,
            fin_location__gte=self.deb_location,
            deb_location__lte=self.fin_location
        ).exclude(id=self.id)

        if conflits.exists():
            raise ValidationError("La voiture est déjà réservée pour cette période.")

    def calcul_montant_facture(self):
        if self.fin_location and self.deb_location:
            nombre_de_jours = (self.fin_location - self.deb_location).days + 1
            if self.avec_chauffeur and self.region == "maritime":
                return self.voiture.prix_location_ville_chauffeur * nombre_de_jours
            elif self.avec_chauffeur and self.region != "maritime":
                return self.voiture.prix_location_hors_ville_chauffeur * nombre_de_jours
            elif not self.avec_chauffeur and self.region == "maritime":
                return self.voiture.prix_location_ville_sans_chauffeur * nombre_de_jours
            else:
                return self.voiture.prix_location_hors_ville_sans_chauffeur * nombre_de_jours
        raise ValidationError("Les dates de réservation ne sont pas valides.")


@receiver(pre_save, sender=Reservation)
def pre_save_update_montant_facture(sender, instance, **kwargs):
    instance.montant_facture = instance.calcul_montant_facture()


class Commentaire(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.content[:30]}... par {self.client}"


class Facture(models.Model):
    reservation = models.ForeignKey(Reservation, default=None, on_delete=models.CASCADE)
    montant_facture = models.IntegerField()
    date_facture = models.DateField(auto_now_add=True)
    est_paye = models.BooleanField(default=False)

    def clean(self):
        self.montant_facture = self.reservation.montant_facture

    def __str__(self):
        return f"Facture N°{self.id} - {self.reservation.client} - {self.montant_facture} FCFA"
