from rest_framework import serializers
from .models import Client, Voiture, Chauffeur, Reservation, Facture, Commentaire, Entretien, Document


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'nom', 'prenom', 'adresse', 'numero_tel', 'email']


class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = [
            'id', 'marque', 'model', 'slug', 'immatriculation',
            'nombre_siege', 'type_carburant', 'tarif_A_B',
            'prix_location_ville_chauffeur', 'prix_location_ville_sans_chauffeur',
            'prix_location_hors_ville_chauffeur', 'prix_location_hors_ville_sans_chauffeur',
            'img_vehicule', 'disponibilite', 'boite', 'climatisation'
        ]


class VoitureListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des voitures"""

    class Meta:
        model = Voiture
        fields = [
            'id', 'marque', 'model', 'slug', 'nombre_siege',
            'type_carburant', 'img_vehicule', 'disponibilite',
            'prix_location_ville_sans_chauffeur', 'boite', 'climatisation'
        ]


class ChauffeurSerializer(serializers.ModelSerializer):
    voiture = VoitureSerializer(read_only=True)

    class Meta:
        model = Chauffeur
        fields = ['id', 'nom', 'prenom', 'telephone', 'disponible', 'voiture']


class ReservationSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    voiture = VoitureSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True)
    voiture_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'client', 'voiture', 'client_id', 'voiture_id',
            'avec_chauffeur', 'detail_reservation', 'lieu', 'region',
            'deb_location', 'fin_location', 'montant_facture', 'est_finalise'
        ]
        read_only_fields = ['montant_facture']

    def validate(self, data):
        """Validation personnalisée pour éviter les conflits de réservation"""
        voiture_id = data.get('voiture_id')
        deb_location = data.get('deb_location')
        fin_location = data.get('fin_location')

        if voiture_id and deb_location and fin_location:
            # Vérifier les conflits de réservation
            conflits = Reservation.objects.filter(
                voiture_id=voiture_id,
                fin_location__gte=deb_location,
                deb_location__lte=fin_location
            )

            # Exclure la réservation actuelle si on est en mode modification
            if self.instance:
                conflits = conflits.exclude(id=self.instance.id)

            if conflits.exists():
                raise serializers.ValidationError(
                    "La voiture est déjà réservée pour cette période."
                )

        return data


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour créer une réservation"""

    class Meta:
        model = Reservation
        fields = [
            'client_id', 'voiture_id', 'avec_chauffeur',
            'detail_reservation', 'lieu', 'region',
            'deb_location', 'fin_location'
        ]


class FactureSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Facture
        fields = ['id', 'reservation', 'montant_facture', 'date_facture', 'est_paye']


class CommentaireSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    voiture = VoitureSerializer(read_only=True)

    class Meta:
        model = Commentaire
        fields = ['id', 'voiture', 'client', 'content']


class EntretienSerializer(serializers.ModelSerializer):
    voiture = VoitureSerializer(read_only=True)

    class Meta:
        model = Entretien
        fields = ['id', 'voiture', 'date', 'type_entretien', 'commentaire', 'cout']


class DocumentSerializer(serializers.ModelSerializer):
    voiture = VoitureSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'voiture', 'doc']